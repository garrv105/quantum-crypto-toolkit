[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)]()
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)]()
[![Quantum Safe](https://img.shields.io/badge/quantum-safe-brightgreen.svg)]()

A practical implementation of post-quantum cryptographic algorithms designed to resist attacks from quantum computers. This toolkit provides secure encryption, digital signatures, and key distribution protocols that remain secure in the quantum era.
🎯 Why Quantum-Resistant Cryptography?
Current cryptographic systems (RSA, ECC, Diffie-Hellman) will be vulnerable to quantum computers running Shor's algorithm. This project implements NIST Post-Quantum Cryptography standards to ensure long-term security.
The Quantum Threat Timeline

2019: Google achieves quantum supremacy (53 qubits)
2023: IBM reaches 433 qubits
2030s: Cryptographically-relevant quantum computers expected
Now: Harvest now, decrypt later attacks are already happening

✨ Features
🔑 Quantum Key Distribution (QKD)

BB84 Protocol: Provably secure key exchange
Eavesdropping Detection: Automatic detection of quantum channel compromise
Key Rate: ~50% efficiency with error correction

🏗️ Lattice-Based Encryption

Learning With Errors (LWE): NIST-approved post-quantum encryption
Security: Based on hard lattice problems (SVP/CVP)
Performance: Efficient encryption/decryption

✍️ Hash-Based Signatures

SPHINCS+ Inspired: Quantum-resistant digital signatures
Security: Based only on hash function security
Stateless: No state management required (unlike XMSS)

📊 Performance Benchmarking

Execution time measurements
Throughput analysis
Comparison with classical algorithms

🚀 Quick Start
Installation
bash# Clone repository
git clone https://github.com/yourusername/quantum-crypto-toolkit.git
cd quantum-crypto-toolkit

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install package
pip install -e .
Basic Usage
1. Quantum Key Distribution
pythonfrom src.quantum_keygen import QuantumKeyDistribution

# Initialize QKD system
qkd = QuantumKeyDistribution(key_length=256)

# Generate shared quantum key
shared_key, stats = qkd.generate_shared_key()

print(f"Shared key: {shared_key[:16]}...")  # First 16 bits
print(f"Error rate: {stats['error_rate']:.2%}")
print(f"Key efficiency: {stats['efficiency']:.2%}")
2. Lattice-Based Encryption
pythonfrom src.lattice_crypto import LatticeEncryption

# Initialize encryption system
lattice = LatticeEncryption(n=256, q=4093)

# Generate keys
public_key, private_key = lattice.generate_keypair()

# Encrypt message
message = b"Secret quantum message"
ciphertexts = lattice.encrypt_bytes(message, public_key)

# Decrypt message
decrypted = lattice.decrypt_bytes(ciphertexts, private_key)
print(decrypted.decode())  # "Secret quantum message"
3. Hash-Based Digital Signatures
pythonfrom src.hash_signatures import HashBasedSignature

# Initialize signature system
signer = HashBasedSignature(security_level=256)

# Generate keypair
public_key, private_key = signer.generate_keypair()

# Sign message
message = b"Important document"
signature = signer.sign(message, private_key)

# Verify signature
is_valid = signer.verify(message, signature, public_key)
print(f"Signature valid: {is_valid}")
Run Complete Demo
bashpython examples/secure_messaging.py
Output:
================================================================================
QUANTUM-RESISTANT SECURE MESSAGING DEMO
================================================================================

Step 1: Establishing Quantum Key...
✓ Quantum key established
  - Key length: 256 bits
  - Error rate: 2.00%
  - Efficiency: 6.25%

Step 2: Encrypting Message with Lattice Cryptography...
Original message: Hello Quantum World!
✓ Message encrypted (160 ciphertext blocks)

Step 3: Decrypting Message...
Decrypted message: Hello Quantum World!
✓ Decryption successful: True

Step 4: Creating Quantum-Resistant Digital Signature...
✓ Signature created
✓ Signature verification: True

Step 5: Testing Tampering Detection...
Tampered message verification: False
✓ Tampering detected successfully
📊 Algorithm Comparison
AlgorithmTypeSecurity BasisKey SizePerformanceBB84Key ExchangeQuantum Physics256-bitFastLWEEncryptionLattice Problems~2KBMediumSPHINCS+SignatureHash Functions~1KBSlowerRSA-2048EncryptionFactoring2048-bit⚠️ Quantum VulnerableECDSASignatureDiscrete Log256-bit⚠️ Quantum Vulnerable
🔬 Technical Details
BB84 Protocol Flow
Alice                    Quantum Channel                    Bob
  |                                                          |
  | Generate random bits & bases                            |
  | [0,1,1,0...] x [R,D,R,D...]                            |
  |                                                          |
  | Encode as qubits: |0⟩,|+⟩,|1⟩,|0⟩...                   |
  |------------------------Qubits-------------------------->|
  |                                                          | Choose random bases
  |                                                          | Measure qubits
  |                                                          |
  |<------------------Announce Bases------------------------|
  | Compare bases                                            |
  |                                                          |
  | Discard mismatched                                       | Discard mismatched
  | Keep matched ~50%                                        | Keep matched ~50%
  |                                                          |
  |<---------------Sample Comparison--------------------->  |
  | Error rate < 11%? ✓ Secure                              |
  |                                                          |
  | Final Key: [1,0,1,1,0...]                               | Final Key: [1,0,1,1,0...]
LWE Security
The Learning With Errors problem:
Given: (A, b = As + e mod q)
Find: Secret s

Where:
- A: random n×n matrix
- s: secret vector
- e: small error vector
- q: large prime modulus
Hardness: Best known attacks require 2^(n/2) operations (classical) and 2^(n/3) (quantum).
Hash-Based Signatures
Uses Winternitz One-Time Signatures with Merkle trees:

Security: Relies only on collision-resistant hash functions
Post-quantum: Hash functions remain secure against quantum attacks
Stateless: Each signature independent (unlike XMSS)

🧪 Running Tests
bash# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test
pytest tests/test_crypto.py::test_qkd_key_generation -v
📈 Performance Benchmarks
Run benchmarks:
bashpython src/utils/benchmark.py
Expected results (on modern CPU):
Quantum Key Distribution (256-bit):  ~5-10ms
Lattice Encryption (per bit):        ~0.5ms
Lattice Decryption (per bit):        ~0.3ms
Hash Signature (256-bit):            ~15-20ms
Signature Verification:               ~10-15ms
🎓 Educational Use
This toolkit is designed for:

Learning: Understanding post-quantum cryptography
Research: Experimenting with quantum-safe protocols
Development: Building quantum-resistant applications
Teaching: Demonstrating cryptographic concepts

Example Jupyter Notebooks
bashjupyter notebook notebooks/quantum_threat_analysis.ipynb
Notebooks include:

Introduction to quantum computing threats
BB84 protocol visualization
Lattice problem hardness analysis
Signature scheme comparisons

🔒 Security Considerations
✅ Quantum-Safe

All algorithms resistant to Shor's algorithm
Based on NIST PQC recommendations
No reliance on integer factorization or discrete logarithms

⚠️ Important Notes

Educational Implementation: Not for production use without audit
Key Management: Implement proper key storage
Side-Channel Attacks: Constant-time operations needed in production
Random Number Generation: Use cryptographically secure RNG

📚 References
NIST Post-Quantum Cryptography

NIST PQC Standardization
CRYSTALS-Kyber (Lattice-based)
SPHINCS+ (Hash-based)

Research Papers

Bennett & Brassard (1984) - BB84 Protocol
Regev (2005) - Learning With Errors
Bernstein et al. (2015) - SPHINCS+

Quantum Computing

IBM Quantum
Google Quantum AI

🛠️ Project Structure
quantum-crypto-toolkit/
├── README.md
├── requirements.txt
├── setup.py
├── config.yaml
├── src/
│   ├── __init__.py
│   ├── quantum_keygen.py      # BB84 implementation
│   ├── lattice_crypto.py      # LWE encryption
│   ├── hash_signatures.py     # SPHINCS+ inspired
│   └── utils/
│       ├── __init__.py
│       └── benchmark.py
├── examples/
│   ├── secure_messaging.py    # End-to-end demo
│   └── file_encryption.py     # File encryption example
├── tests/
│   ├── __init__.py
│   ├── test_qkd.py
│   ├── test_lattice.py
│   └── test_signatures.py
├── notebooks/
│   └── quantum_threat_analysis.ipynb
└── docs/
    ├── algorithms.md
    └── api_reference.md
🤝 Contributing
Contributions welcome! Areas for improvement:

 Code-based cryptography (McEliece)
 Multivariate cryptography
 Isogeny-based cryptography
 Hardware acceleration
 Additional NIST PQC algorithms

📄 License
MIT License - see LICENSE file for details.
🙏 Acknowledgments

NIST Post-Quantum Cryptography Project
IBM Quantum Research
Academic cryptography community

📧 Contact
Your Name - Cybersecurity Researcher

Email: your.email@university.edu
LinkedIn: your-profile
GitHub: @yourusername


⭐ If you find this project useful for learning quantum-resistant cryptography, please give it a star!
Keywords: Post-Quantum Cryptography, Quantum Computing, BB84, Lattice-Based Encryption, Hash-Based Signatures, NIST PQC, Quantum Key Distribution, LWE, SPHINCS+, Cybersecurity# quantum-crypto-toolkit
Post-Quantum Cryptography Implementation: BB84, Lattice-Based Encryption, Hash Signatures
