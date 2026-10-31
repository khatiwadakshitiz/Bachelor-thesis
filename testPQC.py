import oqs

def test_mlkem():
    # Check available KEM algorithms in liboqs using the correct function name
    print("Supported KEM mechanisms in liboqs:")
    kem_list = oqs.get_enabled_kem_mechanisms()
    for alg in kem_list:
        if "ML-KEM" in alg or "Kyber" in alg:
            print(f" - {alg}")

    # Select ML-KEM-768
    alg_name = "ML-KEM-768" if "ML-KEM-768" in kem_list else "Kyber768"
    print(f"\nUsing algorithm: {alg_name}")

    # Initialize client (initiator) and server (responder)
    with oqs.KeyEncapsulation(alg_name) as client_kem:
        with oqs.KeyEncapsulation(alg_name) as server_kem:
            
            # 1. Client generates keypair (or server does, depending on protocol roles)
            public_key = client_kem.generate_keypair()
            print(f"Public key size: {len(public_key)} bytes")

            # 2. Server encapsulates a shared secret using client's public key
            ciphertext, server_shared_secret = server_kem.encap_secret(public_key)
            print(f"Ciphertext size: {len(ciphertext)} bytes")

            # 3. Client decapsulates the ciphertext to recover the shared secret
            client_shared_secret = client_kem.decap_secret(ciphertext)

            # 4. Verify both secrets match
            assert client_shared_secret == server_shared_secret, "Shared secrets do not match!"
            print("\nSuccess! Key exchange completed successfully.")
            print(f"Shared Secret (hex): {client_shared_secret.hex()[:32]}...")

if __name__ == "__main__":
    test_mlkem()