import numpy as np
import hashlib
from typing import Tuple, List


class HashBasedSignature:
    """
    Simplified hash-based signature scheme (inspired by SPHINCS+).
    Quantum-resistant digital signatures using hash functions.
    """
    
    def __init__(self, security_level: int = 256):
        """
        Initialize signature scheme.
        
        Args:
            security_level: Security parameter in bits (128, 192, 256)
        """
        self.security_level = security_level
        self.hash_func = hashlib.sha256 if security_level <= 256 else hashlib.sha512
        
    def generate_keypair(self) -> Tuple[bytes, bytes]:
        """
        Generate signing key pair.
        
        Returns:
            (public_key, private_key)
        """
        # Private key: random seed
        private_key = np.random.bytes(self.security_level // 8)
        
        # Public key: hash of private key
        public_key = self.hash_func(private_key).digest()
        
        return public_key, private_key
    
    def _hash(self, data: bytes) -> bytes:
        """Internal hash function."""
        return self.hash_func(data).digest()
    
    def _generate_one_time_keypair(self, seed: bytes, index: int) -> Tuple[List[bytes], List[bytes]]:
        """Generate Winternitz one-time signature keypair."""
        w = 16  # Winternitz parameter
        
        # Generate private key elements
        sk_elements = []
        for i in range(w):
            element = self._hash(seed + index.to_bytes(4, 'big') + i.to_bytes(4, 'big'))
            sk_elements.append(element)
        
        # Generate public key elements (hash chain)
        pk_elements = []
        for sk in sk_elements:
            pk = sk
            for _ in range(256):  # Hash chain length
                pk = self._hash(pk)
            pk_elements.append(pk)
        
        return sk_elements, pk_elements
    
    def sign(self, message: bytes, private_key: bytes) -> dict:
        """
        Sign a message.
        
        Args:
            message: Message to sign
            private_key: Secret signing key
            
        Returns:
            Signature dictionary
        """
        # Hash message
        msg_hash = self._hash(message)
        
        # Generate one-time keypair for this signature
        index = int.from_bytes(msg_hash[:4], 'big')
        sk_elements, pk_elements = self._generate_one_time_keypair(private_key, index)
        
        # Create signature components
        signature_elements = []
        for i, byte in enumerate(msg_hash[:16]):  # Use first 16 bytes
            # Sign by revealing part of hash chain
            chain_pos = byte
            sig_elem = sk_elements[i]
            
            # Compute forward in hash chain
            for _ in range(chain_pos):
                sig_elem = self._hash(sig_elem)
            
            signature_elements.append(sig_elem)
        
        signature = {
            'signature_elements': signature_elements,
            'public_key_elements': pk_elements,
            'index': index,
            'message_hash': msg_hash
        }
        
        return signature
    
    def verify(self, message: bytes, signature: dict, public_key: bytes) -> bool:
        """
        Verify a signature.
        
        Args:
            message: Original message
            signature: Signature dictionary
            public_key: Public verification key
            
        Returns:
            True if signature is valid
        """
        # Hash message
        msg_hash = self._hash(message)
        
        if msg_hash != signature['message_hash']:
            return False
        
        # Verify each signature element
        sig_elements = signature['signature_elements']
        pk_elements = signature['public_key_elements']
        
        for i, (sig_elem, pk_elem) in enumerate(zip(sig_elements, pk_elements)):
            # Compute forward to public key
            byte_val = msg_hash[i]
            remaining = 256 - byte_val
            
            computed = sig_elem
            for _ in range(remaining):
                computed = self._hash(computed)
            
            if computed != pk_elem:
                return False
        
        return True