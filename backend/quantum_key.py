# quantum_key.py

from qiskit import QuantumCircuit
import random

def simulate_qkd_key(length=128):
    # Simulate QKD-style binary key using randomness
    key = ''
    for _ in range(length):
        bit = random.choice(['0', '1'])
        key += bit
    return key
