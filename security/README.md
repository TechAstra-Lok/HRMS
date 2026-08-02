# Security Assets

This directory stores security policies, audit artifacts, certificate generation helpers, and key management guidance for the HRMS system.

Structure:
- `audit/` - incident tracking, security log seeds, and report templates.
- `certificates/` - certificate usage guidance and generation helpers.
- `keys/` - API key, encryption key, and signing key policy artifacts and seed metadata.
- `policies/` - formal policies for data classification, encryption, and RBAC.

> Sensitive values such as private keys, real certificates, and production secrets must never be committed to this repository.
