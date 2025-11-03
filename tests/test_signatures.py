import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.hash_signatures import HashBasedSignature


class TestHashBasedSignature:
    
    @pytest.fixture
    def signer(self):
        return HashBasedSignature(security_level=256)
    
    def test_keypair_generation(self, signer):
        public_key, private_key = signer.generate_keypair()
        
        assert len(public_key) == 32  # SHA256 output
        assert len(private_key) == 32
    
    def test_sign_verify(self, signer):
        public_key, private_key = signer.generate_keypair()
        
        message = b"Test message"
        signature = signer.sign(message, private_key)
        
        is_valid = signer.verify(message, signature, public_key)
        assert is_valid
    
    def test_tamper_detection(self, signer):
        public_key, private_key = signer.generate_keypair()
        
        message = b"Original message"
        signature = signer.sign(message, private_key)
        
        tampered = b"Tampered message"
        is_valid = signer.verify(tampered, signature, public_key)
        assert not is_valid


if __name__ == '__main__':
    pytest.main([__file__, '-v'])