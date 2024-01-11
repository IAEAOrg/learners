#!/bin/sh

# Directory where the certificates and key will be stored
CERT_DIR="/certs"

# File names for the certificate and key
CERT_FILE="$CERT_DIR/learners.crt"
KEY_FILE="$CERT_DIR/learners.key"

# Set default values for environment variables if not set
CA_CN="${CA_CN:-LearnersCA}"
LEARNERS_CN="${LEARNERS_CN:-learners}"
LEARNERS_SAN="${LEARNERS_SAN:-learners}"
DAYS_VALID="${DAYS_VALID:-365}"

# Function to generate a CA, CSR, and sign the CSR
generate_certs() {
    # Generate a private key for CA
    openssl genrsa -out "$CERT_DIR/ca.key" 2048

    # Generate a CA certificate
    openssl req -x509 -new -nodes -key "$CERT_DIR/ca.key" -sha256 -days "$DAYS_VALID" -out "$CERT_DIR/ca.crt" \
        -subj "/CN=$CA_CN"

    # Generate a private key for CSR
    openssl genrsa -out "$KEY_FILE" 2048

    # Generate a CSR configuration file
    cat > "$CERT_DIR/learners_csr.conf" <<-EOF
    [req]
    distinguished_name = req_distinguished_name
    req_extensions = v3_req
    prompt = no

    [req_distinguished_name]
    CN = $LEARNERS_CN

    [v3_req]
    keyUsage = critical, digitalSignature, keyEncipherment
    extendedKeyUsage = serverAuth, clientAuth
    subjectAltName = @alt_names

    [alt_names]
EOF

    # Append SAN entries
    index=1
    OLDIFS=$IFS
    IFS=','
    for san in $LEARNERS_SAN
    do
        echo "DNS.$index = $san" >> "$CERT_DIR/learners_csr.conf"
        index=$((index+1))
    done
    IFS=$OLDIFS

    # Generate a CSR
    openssl req -new -key "$KEY_FILE" -out "$CERT_DIR/learners.csr" -config "$CERT_DIR/learners_csr.conf"

    # Sign the CSR with the CA certificate to generate the certificate
    openssl x509 -req -in "$CERT_DIR/learners.csr" -CA "$CERT_DIR/ca.crt" -CAkey "$CERT_DIR/ca.key" -CAcreateserial \
        -out "$CERT_FILE" -days "$DAYS_VALID" -sha256 -extfile "$CERT_DIR/learners_csr.conf" -extensions v3_req
}

# Check if both the certificate and key files exist
if [ ! -f "$CERT_FILE" ] || [ ! -f "$KEY_FILE" ]; then
    echo "Certificate and/or key file not found. Generating new ones..."

    # Create CERT_DIR if it does not exist
    mkdir -p "$CERT_DIR"

    # Generate the certificates and keys
    generate_certs
else
    echo "Certificate and key files already exist."
fi

# Check again if both the certificate and key files exist after generation
if [ -f "$CERT_FILE" ] && [ -f "$KEY_FILE" ]; then
    echo "Certificate and key files exist. Exiting with success."
    exit 0
else
    echo "Certificate and/or key file generation failed. Exiting with failure."
    exit 1
fi
