from setuptools import setup, find_packages

setup(
    name="quantum-crypto-toolkit",
    version="1.0.0",
    author="Garrv Sipani",
    author_email="fgarrvs1@jh.edu",
    description="Post-Quantum Cryptography Toolkit",
    url="https://github.com/garrv105/quantum-crypto-toolkit",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        "numpy>=1.24.3",
        "pyyaml>=6.0.1",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "ruff>=0.4.0",
            "black>=24.0.0",
            "isort>=5.12.0",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Security :: Cryptography",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
