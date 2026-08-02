#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

mkdir -p ca server client

# Generate root CA key and certificate
openssl genrsa -out ca/ca.key 4096
openssl req -x509 -new -nodes -key ca/ca.key -sha256 -days 3650 -subj "/CN=hrms-root-ca" -out ca/ca.crt

# Generate server key and CSR
openssl genrsa -out server/server.key 4096
openssl req -new -key server/server.key -subj "/CN=hrms-server" -out server/server.csr
openssl x509 -req -in server/server.csr -CA ca/ca.crt -CAkey ca/ca.key -CAcreateserial -out server/server.crt -days 825 -sha256

# Generate client key and CSR
openssl genrsa -out client/client.key 4096
openssl req -new -key client/client.key -subj "/CN=hrms-client" -out client/client.csr
openssl x509 -req -in client/client.csr -CA ca/ca.crt -CAkey ca/ca.key -CAcreateserial -out client/client.crt -days 825 -sha256

echo "Certificates generated in security/certificates/{ca,server,client}."
