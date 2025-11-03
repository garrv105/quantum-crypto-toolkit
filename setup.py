from setuptools import setup, find_packages

setup(
    name="quantum-crypto-toolkit",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@university.edu",
    description="Post-Quantum Cryptography Toolkit",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.24.3",
        "scipy>=1.11.2",
        "matplotlib>=3.7.2",
        "pyyaml>=6.0.1",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Security :: Cryptography",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
)