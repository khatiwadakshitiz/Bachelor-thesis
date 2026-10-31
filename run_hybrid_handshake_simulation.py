import time
import random
import oqs
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization

def simulate_network_transmission(payload_bytes, base_latency_ms=15, packet_loss_rate=0.0):
    """
    Simulates sending data over a network with configurable latency and packet loss.
    Returns transmission time in milliseconds and success status.
    """
    if random.random() < packet_loss_rate:
        # Packet lost! Retransmission penalty
        return base_latency_ms * 3, False
    
    # Standard MTU is ~1500 bytes. Check for fragmentation.
    mtu = 1500
    fragments = (len(payload_bytes) + mtu - 1) // mtu
    
    jitter = random.uniform(-2.0, 2.0)
    transmission_time = (base_latency_ms * fragments) + jitter
    
    return max(1.0, transmission_time), True

def run_hybrid_handshake_simulation(network_profile="Standard 4G"):
    if network_profile == "Local Wi-Fi":
        latency, loss = 5.0, 0.00
    elif network_profile == "Standard 4G":
        latency, loss = 45.0, 0.02
    elif network_profile == "High-Latency / Lossy":
        latency, loss = 120.0, 0.08
    else:
        latency, loss = 15.0, 0.00

    start_time = time.perf_counter()

    # 1. Key Generation Phase
    alice_private_x = x25519.X25519PrivateKey.generate()
    alice_public_x = alice_private_x.public_key()
    
    alg_name = "ML-KEM-768"
    with oqs.KeyEncapsulation(alg_name) as bob_kem:
        bob_pq_public_key = bob_kem.generate_keypair()
        
        # Message 1: Client -> Server (Client sends X25519 public key - 32 raw bytes)
        msg1_bytes = alice_public_x.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        
        t1, success1 = simulate_network_transmission(msg1_bytes, base_latency_ms=latency, packet_loss_rate=loss)
        if not success1:
            return {"status": "Failed (Packet Loss on Msg 1)", "total_time_ms": None}

        # Server responds
        bob_private_x = x25519.X25519PrivateKey.generate()
        bob_public_x = bob_private_x.public_key()
        
        bob_pub_bytes = bob_public_x.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        
        ciphertext, alice_pq_secret = bob_kem.encap_secret(bob_pq_public_key)
        
        # Message 2: Server -> Client (Server X25519 pub [32 bytes] + ML-KEM Ciphertext [1088 bytes])
        msg2_bytes = bob_pub_bytes + ciphertext
        t2, success2 = simulate_network_transmission(msg2_bytes, base_latency_ms=latency, packet_loss_rate=loss)
        if not success2:
            return {"status": "Failed (Packet Loss on Msg 2)", "total_time_ms": None}

        # Cryptographic Derivation
        alice_classical_secret = alice_private_x.exchange(bob_public_x)
        bob_pq_secret = bob_kem.decap_secret(ciphertext)
        
        combined_secret = alice_classical_secret + alice_pq_secret
        derived_session_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'thesis-salt',
            info=b'handshake',
        ).derive(combined_secret)

    end_time = time.perf_counter()
    total_duration_ms = (end_time - start_time) * 1000.0 + t1 + t2

    return {
        "status": "Success",
        "total_time_ms": round(total_duration_ms, 2),
        "msg1_size_bytes": len(msg1_bytes),
        "msg2_size_bytes": len(msg2_bytes),
        "profile": network_profile
    }

# Test a single run
result = run_hybrid_handshake_simulation("Standard 4G")
print("Simulation Result:", result)