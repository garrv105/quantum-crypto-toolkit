"""
File encryption example using lattice-based cryptography.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.lattice_crypto import LatticeEncryption
import numpy as np


def encrypt_file(input_file: str, output_file: str, public_key):
    """Encrypt a file using lattice cryptography."""
    print(f"Encrypting {input_file}...")
    
    lattice = LatticeEncryption(n=64, q=1009)
    
    # Read file
    with open(input_file, 'rb') as f:
        data = f.read()
    
    print(f"  File size: {len(data)} bytes")
    
    # Encrypt
    ciphertexts = lattice.encrypt_bytes(data, public_key)
    
    # Save encrypted data
    np.save(output_file, ciphertexts)
    
    print(f"✓ Encrypted file saved to {output_file}")
    return len(ciphertexts)


def decrypt_file(input_file: str, output_file: str, private_key):
    """Decrypt a file."""
    print(f"Decrypting {input_file}...")
    
    lattice = LatticeEncryption(n=64, q=1009)
    
    # Load encrypted data
    ciphertexts = np.load(input_file, allow_pickle=True)
    
    print(f"  Ciphertext blocks: {len(ciphertexts)}")
    
    # Decrypt
    data = lattice.decrypt_bytes(ciphertexts, private_key)
    
    # Save decrypted file
    with open(output_file, 'wb') as f:
        f.write(data)
    
    print(f"✓ Decrypted file saved to {output_file}")


if __name__ == "__main__":
    print("=" * 60)
    print("QUANTUM-RESISTANT FILE ENCRYPTION")
    print("=" * 60)
    print()
    
    # Generate keys
    lattice = LatticeEncryption(n=64, q=1009)
    public_key, private_key = lattice.generate_keypair()
    print("✓ Keys generated")
    print()
    
    # Create test file
    test_file = "test_message.txt"
    with open(test_file, 'w') as f:
        f.write("This is a secret message protected by quantum-resistant cryptography!")
    
    # Encrypt
    encrypted_file = "test_message.encrypted"
    encrypt_file(test_file, encrypted_file, public_key)
    print()
    
    # Decrypt
    decrypted_file = "test_message_decrypted.txt"
    decrypt_file(encrypted_file, decrypted_file, private_key)
    print()
    
    # Verify
    with open(test_file, 'r') as f:
        original = f.read()
    with open(decrypted_file, 'r') as f:
        decrypted = f.read()
    
    print(f"Verification: {original == decrypted}")
    print()
    print("=" * 60)