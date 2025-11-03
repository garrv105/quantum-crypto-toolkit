from typing import List, Tuple
import numpy as np
from typing import Tuple


class LatticeEncryption:
    """
    Learning With Errors (LWE) based encryption.
    Post-quantum secure encryption scheme.
    """
    
    def __init__(self, n: int = 256, q: int = 4093, sigma: float = 3.2):
        """
        Initialize LWE parameters.
        
        Args:
            n: Dimension of lattice
            q: Modulus (prime number)
            sigma: Standard deviation for error distribution
        """
        self.n = n
        self.q = q
        self.sigma = sigma
        
    def generate_keypair(self) -> Tuple[np.ndarray, Tuple[np.ndarray, np.ndarray]]:
        """
        Generate public-private key pair.
        
        Returns:
            (public_key, private_key)
        """
        # Private key: random vector s
        s = np.random.randint(0, self.q, size=self.n)
        
        # Public key: (A, b = As + e)
        A = np.random.randint(0, self.q, size=(self.n, self.n))
        e = np.random.normal(0, self.sigma, size=self.n).astype(int)
        b = (A.dot(s) + e) % self.q
        
        public_key = (A, b)
        private_key = s
        
        return public_key, private_key
    
    def encrypt(self, message: int, public_key: Tuple[np.ndarray, np.ndarray]) -> Tuple[np.ndarray, int]:
        """
        Encrypt a single bit message.
        
        Args:
            message: 0 or 1
            public_key: (A, b) from key generation
            
        Returns:
            Ciphertext (u, v)
        """
        A, b = public_key
        
        # Random vector r
        r = np.random.randint(0, 2, size=self.n)
        
        # Error terms
        e1 = np.random.normal(0, self.sigma, size=self.n).astype(int)
        e2 = int(np.random.normal(0, self.sigma))
        
        # Ciphertext
        u = (A.T.dot(r) + e1) % self.q
        v = (b.dot(r) + e2 + message * (self.q // 2)) % self.q
        
        return u, v
    
    def decrypt(self, ciphertext: Tuple[np.ndarray, int], private_key: np.ndarray) -> int:
        """
        Decrypt ciphertext to recover message.
        
        Args:
            ciphertext: (u, v) from encryption
            private_key: Secret key s
            
        Returns:
            Decrypted message bit
        """
        u, v = ciphertext
        
        # Compute v - s·u
        result = (v - private_key.dot(u)) % self.q
        
        # Round to nearest multiple of q/2
        if result < self.q // 4 or result > 3 * self.q // 4:
            return 0
        else:
            return 1
    
    def encrypt_bytes(self, data: bytes, public_key: Tuple[np.ndarray, np.ndarray]) -> List[Tuple]:
        """Encrypt arbitrary byte data."""
        ciphertexts = []
        
        for byte in data:
            # Encrypt each bit
            for i in range(8):
                bit = (byte >> i) & 1
                ct = self.encrypt(bit, public_key)
                ciphertexts.append(ct)
        
        return ciphertexts
    
    def decrypt_bytes(self, ciphertexts: List[Tuple], private_key: np.ndarray) -> bytes:
        """Decrypt to recover original bytes."""
        result = []
        
        for i in range(0, len(ciphertexts), 8):
            byte_cts = ciphertexts[i:i+8]
            byte_val = 0
            
            for j, ct in enumerate(byte_cts):
                bit = self.decrypt(ct, private_key)
                byte_val |= (bit << j)
            
            result.append(byte_val)
        
        return bytes(result)