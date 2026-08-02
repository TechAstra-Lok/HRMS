param()

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

New-Item -ItemType Directory -Force -Path ca, server, client | Out-Null

Write-Host "Generating root CA..."
openssl genrsa -out ca/ca.key 4096
openssl req -x509 -new -nodes -key ca/ca.key -sha256 -days 3650 -subj "/CN=hrms-root-ca" -out ca/ca.crt

Write-Host "Generating server certificate..."
openssl genrsa -out server/server.key 4096
openssl req -new -key server/server.key -subj "/CN=hrms-server" -out server/server.csr
openssl x509 -req -in server/server.csr -CA ca/ca.crt -CAkey ca/ca.key -CAcreateserial -out server/server.crt -days 825 -sha256

Write-Host "Generating client certificate..."
openssl genrsa -out client/client.key 4096
openssl req -new -key client/client.key -subj "/CN=hrms-client" -out client/client.csr
openssl x509 -req -in client/client.csr -CA ca/ca.crt -CAkey ca/ca.key -CAcreateserial -out client/client.crt -days 825 -sha256

Write-Host "Certificates generated in security/certificates/{ca,server,client}."