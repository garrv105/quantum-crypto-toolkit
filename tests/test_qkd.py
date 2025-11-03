import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.quantum_keygen import QuantumKeyDistribution


class TestQuantumKeyDistribution:
    
    @pytest.fixture
    def qkd(self):
        return QuantumKeyDistribution(key_length=128)
    
    def test_initialization(self, qkd):
        assert qkd.key_length == 128
        assert qkd.bases == {0: 'rectilinear', 1: 'diagonal'}
    
    def test_random_bit_generation(self, qkd):
        bits = qkd.generate_random_bits(100)
        assert len(bits) == 100
        assert all(b in [0, 1] for b in bits)
    
    def test_qubit_encoding(self, qkd):
        bits = [0, 1, 0, 1]
        bases = [0, 0, 1, 1]
        qubits = qkd.encode_qubits(bits, bases)
        
        assert len(qubits) == 4
        assert qubits[0]['state'] == '|0⟩'
        assert qubits[1]['state'] == '|1⟩'
        assert qubits[2]['state'] == '|+⟩'
        assert qubits[3]['state'] == '|-⟩'
    
    def test_key_generation(self, qkd):
        shared_key, stats = qkd.generate_shared_key()
        
        assert len(shared_key) == 128
        assert stats['error_rate'] < 0.11
        assert stats['final_key_length'] == 128


if __name__ == '__main__':
    pytest.main([__file__, '-v'])