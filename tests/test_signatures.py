import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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

    def test_signature_structure(self, signer):
        public_key, private_key = signer.generate_keypair()
        message = b"Test"
        signature = signer.sign(message, private_key)
        assert "signature_elements" in signature
        assert "public_key_elements" in signature
        assert "index" in signature
        assert "message_hash" in signature

    def test_signature_elements_count(self, signer):
        public_key, private_key = signer.generate_keypair()
        message = b"Test"
        signature = signer.sign(message, private_key)
        assert len(signature["signature_elements"]) == 16

    def test_different_messages_different_signatures(self, signer):
        public_key, private_key = signer.generate_keypair()
        sig1 = signer.sign(b"Message 1", private_key)
        sig2 = signer.sign(b"Message 2", private_key)
        assert sig1["message_hash"] != sig2["message_hash"]

    def test_empty_message(self, signer):
        public_key, private_key = signer.generate_keypair()
        message = b""
        signature = signer.sign(message, private_key)
        assert signer.verify(message, signature, public_key)

    def test_long_message(self, signer):
        public_key, private_key = signer.generate_keypair()
        message = b"A" * 10000
        signature = signer.sign(message, private_key)
        assert signer.verify(message, signature, public_key)

    def test_hash_function_selection_256(self):
        signer = HashBasedSignature(security_level=256)
        import hashlib

        assert signer.hash_func == hashlib.sha256

    def test_hash_function_selection_512(self):
        signer = HashBasedSignature(security_level=512)
        import hashlib

        assert signer.hash_func == hashlib.sha512


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
