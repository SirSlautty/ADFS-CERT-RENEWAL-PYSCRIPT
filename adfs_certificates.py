"""Conservative AD FS certificate inventory and rotation helpers."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys


def run_powershell(script: str) -> str:
    result = subprocess.run(
        ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", script],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "PowerShell command failed")
    return result.stdout.strip()


def inventory() -> str:
    return run_powershell(
        "Get-AdfsCertificate | Select-Object CertificateType, IsPrimary, "
        "@{N='Thumbprint';E={$_.Certificate.Thumbprint}}, "
        "@{N='NotAfter';E={$_.Certificate.NotAfter}} | Format-Table -AutoSize"
    )


def rotate_token_signing(apply: bool) -> str:
    command = "Update-AdfsCertificate -CertificateType Token-Signing -Urgent"
    if not apply:
        return f"DRY RUN: {command}"
    return run_powershell(command) or "Token-signing rotation command completed."


def validate_ssl(thumbprint: str, apply: bool) -> str:
    normalized = re.sub(r"\s+", "", thumbprint).upper()
    if not re.fullmatch(r"[0-9A-F]{40,64}", normalized):
        raise ValueError("Thumbprint must contain 40-64 hexadecimal characters")

    assignment = f"Set-AdfsSslCertificate -Thumbprint '{normalized}'"
    script = rf"""
$cert = Get-Item 'Cert:\LocalMachine\My\{normalized}' -ErrorAction Stop
if (-not $cert.HasPrivateKey) {{ throw 'Certificate has no private key.' }}
if ($cert.NotBefore -gt (Get-Date) -or $cert.NotAfter -le (Get-Date)) {{ throw 'Certificate is not currently valid.' }}
$serverAuth = $cert.EnhancedKeyUsageList | Where-Object {{ $_.ObjectId.Value -eq '1.3.6.1.5.5.7.3.1' }}
if (-not $serverAuth) {{ throw 'Certificate is missing the Server Authentication EKU.' }}
$cert | Select-Object Subject, Thumbprint, NotBefore, NotAfter, HasPrivateKey | Format-List
"""
    details = run_powershell(script)
    if not apply:
        return f"{details}\n\nDRY RUN: {assignment}"
    run_powershell(assignment)
    return f"{details}\n\nAD FS SSL certificate assignment completed."


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("inventory", help="List AD FS certificates")
    rotate = subparsers.add_parser("rotate-token-signing", help="Urgently rotate token signing")
    rotate.add_argument("--apply", action="store_true", help="Execute the change")
    ssl = subparsers.add_parser("validate-ssl", help="Validate and optionally assign an SSL certificate")
    ssl.add_argument("--thumbprint", required=True)
    ssl.add_argument("--apply", action="store_true", help="Execute the change")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "inventory":
            output = inventory()
        elif args.command == "rotate-token-signing":
            output = rotate_token_signing(args.apply)
        else:
            output = validate_ssl(args.thumbprint, args.apply)
        print(output)
        return 0
    except (RuntimeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
