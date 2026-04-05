import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class TestExampleImports:
    def test_import_file_encryption(self):
        from examples.file_encryption import decrypt_file, encrypt_file

        assert callable(encrypt_file)
        assert callable(decrypt_file)

    def test_import_secure_messaging(self):
        from examples.secure_messaging import secure_messaging_demo

        assert callable(secure_messaging_demo)


class TestExampleModules:
    def test_file_encryption_roundtrip(self, tmp_path):

        from src.lattice_crypto import LatticeEncryption

        lattice = LatticeEncryption(n=16, q=4093, sigma=1.0)
        public_key, private_key = lattice.generate_keypair()

        # Write test file
        input_file = tmp_path / "test_input.txt"
        input_file.write_text("Hello quantum!")

        # Encrypt
        with open(input_file, "rb") as f:
            data = f.read()

        ciphertexts = lattice.encrypt_bytes(data, public_key)
        decrypted = lattice.decrypt_bytes(ciphertexts, private_key)
        assert decrypted == data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
