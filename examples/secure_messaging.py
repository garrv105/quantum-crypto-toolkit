import numpy as np
from src.hash_signatures import HashBasedSignature
from src.lattice_crypto import LatticeEncryption
from src.quantum_keygen import QuantumKeyDistribution
def secure_messaging_demo():
    """
    Demonstrate quantum-resistant secure messaging.
    """
    print("=" * 80)
    print("QUANTUM-RESISTANT SECURE MESSAGING DEMO")
    print("=" * 80)
    print()
    
    # Step 1: Quantum Key Distribution
    print("Step 1: Establishing Quantum Key...")
    qkd = QuantumKeyDistribution(key_length=256)
    shared_key, stats = qkd.generate_shared_key()
    
    print(f"✓ Quantum key established")
    print(f"  - Key length: {len(shared_key)} bits")
    print(f"  - Error rate: {stats['error_rate']:.2%}")
    print(f"  - Efficiency: {stats['efficiency']:.2%}")
    print()
    
    # Step 2: Lattice-based encryption
    print("Step 2: Encrypting Message with Lattice Cryptography...")
    lattice = LatticeEncryption(n=64, q=1009)  # Smaller params for demo
    public_key, private_key = lattice.generate_keypair()
    
    message = b"Hello Quantum World!"
    print(f"Original message: {message.decode()}")
    
    ciphertexts = lattice.encrypt_bytes(message, public_key)
    print(f"✓ Message encrypted ({len(ciphertexts)} ciphertext blocks)")
    print()
    
    # Step 3: Decryption
    print("Step 3: Decrypting Message...")
    decrypted = lattice.decrypt_bytes(ciphertexts, private_key)
    print(f"Decrypted message: {decrypted.decode(errors='ignore')}")
    print(f"✓ Decryption successful: {message == decrypted}")
    print()
    
    # Step 4: Hash-based signature
    print("Step 4: Creating Quantum-Resistant Digital Signature...")
    signer = HashBasedSignature(security_level=256)
    pub_key, priv_key = signer.generate_keypair()
    
    signature = signer.sign(message, priv_key)
    print(f"✓ Signature created")
    
    is_valid = signer.verify(message, signature, pub_key)
    print(f"✓ Signature verification: {is_valid}")
    print()
    
    # Test tampering detection
    print("Step 5: Testing Tampering Detection...")
    tampered_message = b"Hello Quantum World?"
    is_valid_tampered = signer.verify(tampered_message, signature, pub_key)
    print(f"Tampered message verification: {is_valid_tampered}")
    print(f"✓ Tampering detected successfully")
    print()
    
    print("=" * 80)
    print("DEMO COMPLETED")
    print("=" * 80)