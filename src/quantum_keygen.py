import numpy as np
from typing import Tuple, List
import random


class QuantumKeyDistribution:
    """
    Implementation of BB84 Quantum Key Distribution Protocol.
    Simulates quantum key exchange resistant to eavesdropping.
    """
    
    def __init__(self, key_length: int = 256):
        """
        Initialize QKD system.
        
        Args:
            key_length: Desired length of the quantum key
        """
        self.key_length = key_length
        self.bases = {0: 'rectilinear', 1: 'diagonal'}
        
    def generate_random_bits(self, n: int) -> List[int]:
        """Generate random bits for Alice."""
        return [random.randint(0, 1) for _ in range(n)]
    
    def generate_random_bases(self, n: int) -> List[int]:
        """Generate random measurement bases."""
        return [random.randint(0, 1) for _ in range(n)]
    
    def encode_qubits(self, bits: List[int], bases: List[int]) -> List[dict]:
        """
        Encode classical bits into quantum states.
        
        Args:
            bits: Classical bit values
            bases: Measurement bases (0=rectilinear, 1=diagonal)
            
        Returns:
            List of quantum states
        """
        qubits = []
        for bit, basis in zip(bits, bases):
            if basis == 0:  # Rectilinear: |0⟩ or |1⟩
                state = '|0⟩' if bit == 0 else '|1⟩'
            else:  # Diagonal: |+⟩ or |-⟩
                state = '|+⟩' if bit == 0 else '|-⟩'
            qubits.append({'state': state, 'basis': basis})
        return qubits
    
    def measure_qubits(self, qubits: List[dict], bases: List[int]) -> List[int]:
        """
        Bob measures received qubits.
        
        Args:
            qubits: Quantum states from Alice
            bases: Bob's measurement bases
            
        Returns:
            Measured bit values
        """
        measurements = []
        for qubit, basis in zip(qubits, bases):
            alice_basis = qubit['basis']
            
            if basis == alice_basis:
                # Same basis: deterministic result
                if qubit['state'] in ['|0⟩', '|+⟩']:
                    measurements.append(0)
                else:
                    measurements.append(1)
            else:
                # Different basis: random result (50/50)
                measurements.append(random.randint(0, 1))
        
        return measurements
    
    def sift_key(self, alice_bits: List[int], bob_bits: List[int],
                 alice_bases: List[int], bob_bases: List[int]) -> Tuple[List[int], List[int]]:
        """
        Perform basis reconciliation to extract matching bits.
        
        Returns:
            Tuple of (alice_sifted_key, bob_sifted_key)
        """
        alice_sifted = []
        bob_sifted = []
        
        for i in range(len(alice_bases)):
            if alice_bases[i] == bob_bases[i]:
                alice_sifted.append(alice_bits[i])
                bob_sifted.append(bob_bits[i])
        
        return alice_sifted, bob_sifted
    
    def detect_eavesdropping(self, alice_key: List[int], bob_key: List[int],
                            sample_size: int = 50) -> Tuple[bool, float]:
        """
        Check for eavesdropping by comparing sample bits.
        
        Returns:
            Tuple of (is_secure, error_rate)
        """
        if len(alice_key) < sample_size:
            sample_size = len(alice_key) // 2
        
        # Sample random positions
        sample_indices = random.sample(range(len(alice_key)), sample_size)
        
        errors = sum(1 for i in sample_indices if alice_key[i] != bob_key[i])
        error_rate = errors / sample_size
        
        # Threshold: typically 11% for BB84
        is_secure = error_rate < 0.11
        
        return is_secure, error_rate
    
    def generate_shared_key(self) -> Tuple[List[int], dict]:
        """
        Complete QKD protocol execution.
        
        Returns:
            Tuple of (shared_key, protocol_stats)
        """
        # Generate enough bits (compensate for sifting)
        n_bits = self.key_length * 4
        
        # Step 1: Alice generates random bits and bases
        alice_bits = self.generate_random_bits(n_bits)
        alice_bases = self.generate_random_bases(n_bits)
        
        # Step 2: Alice encodes qubits
        qubits = self.encode_qubits(alice_bits, alice_bases)
        
        # Step 3: Bob chooses random bases and measures
        bob_bases = self.generate_random_bases(n_bits)
        bob_bits = self.measure_qubits(qubits, bob_bases)
        
        # Step 4: Basis reconciliation (public channel)
        alice_sifted, bob_sifted = self.sift_key(
            alice_bits, bob_bits, alice_bases, bob_bases
        )
        
        # Step 5: Eavesdropping detection
        is_secure, error_rate = self.detect_eavesdropping(alice_sifted, bob_sifted)
        
        if not is_secure:
            raise SecurityError(f"Eavesdropping detected! Error rate: {error_rate:.2%}")
        
        # Step 6: Privacy amplification (keep remaining bits)
        final_key = alice_sifted[50:][:self.key_length]
        
        stats = {
            'initial_bits': n_bits,
            'sifted_bits': len(alice_sifted),
            'final_key_length': len(final_key),
            'error_rate': error_rate,
            'efficiency': len(final_key) / n_bits
        }
        
        return final_key, stats


class SecurityError(Exception):
    """Custom exception for security violations."""
    pass