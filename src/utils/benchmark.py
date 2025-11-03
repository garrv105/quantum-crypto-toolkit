import time
from typing import Callable, Dict


class CryptoBenchmark:
    """Benchmark quantum-resistant cryptographic operations."""
    
    @staticmethod
    def measure_time(func: Callable, *args, **kwargs) -> Tuple[float, any]:
        """
        Measure execution time of a function.
        
        Returns:
            (execution_time_ms, result)
        """
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        
        return (end - start) * 1000, result
    
    @staticmethod
    def benchmark_keygen(crypto_system) -> Dict:
        """Benchmark key generation."""
        times = []
        
        for _ in range(10):
            exec_time, _ = CryptoBenchmark.measure_time(crypto_system.generate_keypair)
            times.append(exec_time)
        
        return {
            'mean_time_ms': np.mean(times),
            'std_time_ms': np.std(times),
            'min_time_ms': np.min(times),
            'max_time_ms': np.max(times)
        }
    
    @staticmethod
    def benchmark_encryption(crypto_system, public_key, data) -> Dict:
        """Benchmark encryption operation."""
        times = []
        
        for _ in range(10):
            exec_time, _ = CryptoBenchmark.measure_time(
                crypto_system.encrypt, data, public_key
            )
            times.append(exec_time)
        
        return {
            'mean_time_ms': np.mean(times),
            'throughput_kb_s': len(data) / (np.mean(times) / 1000) / 1024
        }