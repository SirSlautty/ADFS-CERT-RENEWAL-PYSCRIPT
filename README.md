# ADFS-CERT-RENEWAL-PYSCRIPT
ADFS Cert renewal py script

**READ ME**

This is a fast attempt at developing a python script that automatically renews AD FS environment certificates 

**THIS IS A WORK IN PROGRESS, ANY FEEDBACK OR POINTERS ARE MUCH APPRECIATED**

developing a custom python script that automates token renewals in an AD FS environment

-Use the AD FS Management module for Windows PowerShell to gather the necessary information about the existing token-signing and token-decrypting certificates.

-Use the cryptography library in Python to generate new self-signed certificates for token-signing and token-decrypting.

-Use the AD FS Management module for Windows PowerShell to import the new certificates and set them as the primary token-signing and token-decrypting certificates.

-Use a scheduling tool, such as schedule or cron, to run the script on a regular basis to automatically renew the certificates before they expire.

>>>It's also important to consider the security aspect while creating the script. Here are a few best practices to follow:<<<

-Properly validate and sanitize user input to prevent injection attacks.

-Securely store and transmit sensitive information, such as passwords and private keys.

-Use secure coding practices to prevent common vulnerabilities, such as buffer overflows and SQL injection.

-Limit the permissions of the script's execution environment as much as possible to prevent privilege escalation.
