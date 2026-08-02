# Certificates

This directory contains helper scripts and guidance for generating local certificate materials for development and testing.

## Purpose
- `ca-cert/` - certificate authority artifacts.
- `server-cert/` - server TLS certificates for HRMS services.
- `client-cert/` - client certificates for mutual TLS or service authentication.

## Usage
1. Install OpenSSL.
2. Run `./generate_certs.sh` on Linux/macOS or `.uild\generate_certs.ps1` on Windows.
3. Copy generated certificates into a protected keystore or secret store.

> Do not commit private keys or production certificate secrets into source control.
