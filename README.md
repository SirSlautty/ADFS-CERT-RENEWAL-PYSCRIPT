# AD FS Certificate Renewal Toolkit

Python wrappers for inspecting and rotating certificates on Windows Server AD FS farms. The commands are intentionally explicit: inspection is the default, and certificate-changing operations require `--apply`.

> [!CAUTION]
> Test certificate rotation in a non-production farm first. Token-signing certificate changes can require federation partners to refresh metadata. Service communication/SSL certificates normally need a publicly trusted certificate and coordinated WAP updates; a self-signed certificate is rarely appropriate.

## Requirements

- Windows Server with the AD FS PowerShell module
- Python 3.9+
- An elevated PowerShell session on the primary AD FS server
- A current farm backup and a rollback plan

## Inspect the farm

```powershell
py adfs_certificates.py inventory
```

## Rotate a token-signing certificate

Preview the command:

```powershell
py adfs_certificates.py rotate-token-signing
```

Apply it after validating federation metadata monitoring and partner requirements:

```powershell
py adfs_certificates.py rotate-token-signing --apply
```

AD FS automatic certificate rollover is the preferred mechanism for token-signing and token-decrypting certificates in most environments. Urgent rotation is intended for compromise or a controlled maintenance event.

## Validate an SSL certificate before assignment

This toolkit does not generate a production SSL certificate. It validates an existing Local Computer certificate and prints the `Set-AdfsSslCertificate` command:

```powershell
py adfs_certificates.py validate-ssl --thumbprint THUMBPRINT
py adfs_certificates.py validate-ssl --thumbprint THUMBPRINT --apply
```

The certificate must have a private key, include Server Authentication EKU, be currently valid, and contain the federation service name in its DNS names.

## Safety model

- No secret or private-key material is read by Python.
- PowerShell is invoked without `shell=True`.
- Thumbprints accept hexadecimal characters only.
- Mutating commands are dry runs unless `--apply` is supplied.
- Errors and PowerShell exit codes are propagated to automation.

The original prototype files remain for historical context. New automation should use `adfs_certificates.py`.
