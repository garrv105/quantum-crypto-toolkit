import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.quantum_keygen import QuantumKeyDistribution, SecurityError


class TestQuantumKeyDistribution:
    @pytest.fixture
    def qkd(self):
        return QuantumKeyDistribution(key_length=128)

    def test_initialization(self, qkd):
        assert qkd.key_length == 128
        assert qkd.bases == {0: "rectilinear", 1: "diagonal"}

    def test_random_bit_generation(self, qkd):
        bits = qkd.generate_random_bits(100)
        assert len(bits) == 100
        assert all(b in [0, 1] for b in bits)

    def test_random_bit_generation_single(self, qkd):
        bits = qkd.generate_random_bits(1)
        assert len(bits) == 1
        assert bits[0] in [0, 1]

    def test_random_bases_generation(self, qkd):
        bases = qkd.generate_random_bases(100)
        assert len(bases) == 100
        assert all(b in [0, 1] for b in bases)

    def test_qubit_encoding(self, qkd):
        bits = [0, 1, 0, 1]
        bases = [0, 0, 1, 1]
        qubits = qkd.encode_qubits(bits, bases)
        assert len(qubits) == 4
        assert qubits[0]["state"] == "|0⟩"
        assert qubits[1]["state"] == "|1⟩"
        assert qubits[2]["state"] == "|+⟩"
        assert qubits[3]["state"] == "|-⟩"

    def test_qubit_encoding_preserves_basis(self, qkd):
        bits = [0, 1]
        bases = [0, 1]
        qubits = qkd.encode_qubits(bits, bases)
        assert qubits[0]["basis"] == 0
        assert qubits[1]["basis"] == 1

    def test_measurement_same_basis_deterministic(self, qkd):
        bits = [0, 1, 0, 1]
        bases = [0, 0, 1, 1]
        qubits = qkd.encode_qubits(bits, bases)
        # Measure with same bases -> should get same bits
        measured = qkd.measure_qubits(qubits, bases)
        assert measured == bits

    def test_key_sifting(self, qkd):
        alice_bits = [0, 1, 0, 1]
        bob_bits = [0, 1, 1, 0]
        alice_bases = [0, 1, 0, 1]
        bob_bases = [0, 1, 1, 0]
        alice_sifted, bob_sifted = qkd.sift_key(alice_bits, bob_bits, alice_bases, bob_bases)
        # Matching bases at indices 0 and 1
        assert alice_sifted == [0, 1]
        assert bob_sifted == [0, 1]

    def test_key_sifting_no_match(self, qkd):
        alice_bits = [0, 1]
        bob_bits = [1, 0]
        alice_bases = [0, 1]
        bob_bases = [1, 0]
        alice_sifted, bob_sifted = qkd.sift_key(alice_bits, bob_bits, alice_bases, bob_bases)
        assert alice_sifted == []
        assert bob_sifted == []

    def test_eavesdropping_detection_secure(self, qkd):
        # Identical keys -> no eavesdropping
        key = [0, 1, 0, 1, 1, 0, 0, 1, 1, 0] * 10
        is_secure, error_rate = qkd.detect_eavesdropping(key, key, sample_size=20)
        assert is_secure is True
        assert error_rate == 0.0

    def test_eavesdropping_detection_insecure(self, qkd):
        # Very different keys -> eavesdropping detected
        alice_key = [0] * 100
        bob_key = [1] * 100
        is_secure, error_rate = qkd.detect_eavesdropping(alice_key, bob_key, sample_size=50)
        assert is_secure is False
        assert error_rate > 0.11

    def test_full_key_generation(self, qkd):
        shared_key, stats = qkd.generate_shared_key()
        assert len(shared_key) == 128
        assert stats["error_rate"] < 0.11
        assert stats["final_key_length"] == 128
        assert "initial_bits" in stats
        assert "sifted_bits" in stats
        assert "efficiency" in stats

    def test_key_generation_different_length(self):
        qkd = QuantumKeyDistribution(key_length=64)
        shared_key, stats = qkd.generate_shared_key()
        assert len(shared_key) == 64

    def test_security_error_exists(self):
        with pytest.raises(SecurityError):
            raise SecurityError("test")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
