import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.lattice_crypto import LatticeEncryption


class TestLatticeEncryption:
    
    @pytest.fixture
    def lattice(self):
        return LatticeEncryption(n=64, q=1009)
    
    def test_keypair_generation(self, lattice):
        public_key, private_key = lattice.generate_keypair()
        A, b = public_key
        
        assert A.shape == (64, 64)
        assert b.shape == (64,)
        assert private_key.shape == (64,)
    
    def test_encryption_decryption(self, lattice):
        public_key, private_key = lattice.generate_keypair()
        
        # Test bit 0
        ct = lattice.encrypt(0, public_key)
        decrypted = lattice.decrypt(ct, private_key)
        assert decrypted == 0
        
        # Test bit 1
        ct = lattice.encrypt(1, public_key)
        decrypted = lattice.decrypt(ct, private_key)
        assert decrypted == 1
    
    def test_byte_encryption(self, lattice):
        public_key, private_key = lattice.generate_keypair()
        
        message = b"Test"
        ciphertexts = lattice.encrypt_bytes(message, public_key)
        decrypted = lattice.decrypt_bytes(ciphertexts, private_key)
        
        assert decrypted == message


if __name__ == '__main__':
    pytest.main([__file__, '-v'])