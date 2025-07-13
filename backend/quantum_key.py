from qiskit import QuantumCircuit
from qiskit_aer.primitives import SamplerV2

def simulate_qkd_key(length=128):
    qc = QuantumCircuit(length)
    qc.h(range(length))
    qc.measure_all()

    sampler = SamplerV2()
    result = sampler.run([qc], shots=1).result()

    counts = result[0].data.meas.get_counts()
    key_str = list(counts.keys())[0]  # Like '100101...'
    return key_str
