import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.lattice_crypto import LatticeEncryption


class TestLatticeEncryption:
    @pytest.fixture
    def lattice(self):
        return LatticeEncryption(n=16, q=4093, sigma=1.0)

    def test_keypair_generation(self, lattice):
        public_key, private_key = lattice.generate_keypair()
        A, b = public_key
        assert A.shape == (16, 16)
        assert b.shape == (16,)
        assert private_key.shape == (16,)

    def test_keypair_values_in_range(self, lattice):
        public_key, private_key = lattice.generate_keypair()
        A, b = public_key
        assert np.all(A >= 0) and np.all(A < lattice.q)
        assert np.all(private_key >= 0) and np.all(private_key < lattice.q)

    def test_encrypt_decrypt_bit_zero(self, lattice):
        public_key, private_key = lattice.generate_keypair()
        ct = lattice.encrypt(0, public_key)
        decrypted = lattice.decrypt(ct, private_key)
        assert decrypted == 0

    def test_encrypt_decrypt_bit_one(self, lattice):
        public_key, private_key = lattice.generate_keypair()
        ct = lattice.encrypt(1, public_key)
        decrypted = lattice.decrypt(ct, private_key)
        assert decrypted == 1

    def test_ciphertext_structure(self, lattice):
        public_key, private_key = lattice.generate_keypair()
        u, v = lattice.encrypt(0, public_key)
        assert u.shape == (16,)
        assert isinstance(v, (int, np.integer))

    def test_byte_encryption_short(self, lattice):
        public_key, private_key = lattice.generate_keypair()
        message = b"Test"
        ciphertexts = lattice.encrypt_bytes(message, public_key)
        decrypted = lattice.decrypt_bytes(ciphertexts, private_key)
        assert decrypted == message

    def test_byte_encryption_single_byte(self, lattice):
        public_key, private_key = lattice.generate_keypair()
        message = b"A"
        ciphertexts = lattice.encrypt_bytes(message, public_key)
        assert len(ciphertexts) == 8  # 8 bits per byte
        decrypted = lattice.decrypt_bytes(ciphertexts, private_key)
        assert decrypted == message

    def test_byte_encryption_empty(self, lattice):
        public_key, private_key = lattice.generate_keypair()
        message = b""
        ciphertexts = lattice.encrypt_bytes(message, public_key)
        assert len(ciphertexts) == 0
        decrypted = lattice.decrypt_bytes(ciphertexts, private_key)
        assert decrypted == message

    def test_different_keys_different_ciphertexts(self, lattice):
        pk1, sk1 = lattice.generate_keypair()
        pk2, sk2 = lattice.generate_keypair()
        ct1_u, ct1_v = lattice.encrypt(1, pk1)
        ct2_u, ct2_v = lattice.encrypt(1, pk2)
        # Different keys should (almost certainly) produce different ciphertexts
        assert not np.array_equal(ct1_u, ct2_u) or ct1_v != ct2_v

    def test_default_parameters(self):
        lattice = LatticeEncryption()
        assert lattice.n == 256
        assert lattice.q == 4093
        assert lattice.sigma == 3.2

    def test_custom_parameters(self):
        lattice = LatticeEncryption(n=128, q=2053, sigma=2.0)
        assert lattice.n == 128
        assert lattice.q == 2053
        assert lattice.sigma == 2.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
