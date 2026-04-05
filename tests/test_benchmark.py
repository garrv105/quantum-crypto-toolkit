import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.hash_signatures import HashBasedSignature
from src.lattice_crypto import LatticeEncryption
from src.utils.benchmark import CryptoBenchmark


class TestCryptoBenchmark:
    def test_measure_time_returns_result(self):
        elapsed, result = CryptoBenchmark.measure_time(lambda: 42)
        assert result == 42
        assert elapsed >= 0

    def test_measure_time_with_args(self):
        elapsed, result = CryptoBenchmark.measure_time(lambda x, y: x + y, 3, 4)
        assert result == 7

    def test_benchmark_keygen_lattice(self):
        lattice = LatticeEncryption(n=32, q=521)
        stats = CryptoBenchmark.benchmark_keygen(lattice)
        assert "mean_time_ms" in stats
        assert "std_time_ms" in stats
        assert "min_time_ms" in stats
        assert "max_time_ms" in stats
        assert stats["mean_time_ms"] >= 0

    def test_benchmark_keygen_signatures(self):
        signer = HashBasedSignature(security_level=256)
        stats = CryptoBenchmark.benchmark_keygen(signer)
        assert stats["mean_time_ms"] >= 0

    def test_benchmark_encryption(self):
        lattice = LatticeEncryption(n=32, q=521)
        pub, priv = lattice.generate_keypair()
        stats = CryptoBenchmark.benchmark_encryption(lattice, pub, 0)
        assert "mean_time_ms" in stats
        assert "throughput_kb_s" in stats


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
