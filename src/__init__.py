"""
Quantum-Resistant Cryptography Toolkit
Post-quantum secure encryption and signatures
"""

__version__ = "1.0.0"
__author__ = "Your Name"

from .quantum_keygen import QuantumKeyDistribution
from .lattice_crypto import LatticeEncryption
from .hash_signatures import HashBasedSignature

__all__ = [
    'QuantumKeyDistribution',
    'LatticeEncryption',
    'HashBasedSignature'
]