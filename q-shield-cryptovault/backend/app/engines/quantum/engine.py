"""Quantum Security Engine (Section 17-19 / Phase 8).

Runs a small LOCAL Qiskit simulation to demonstrate quantum-computing
concepts relevant to cryptographic threat assessment (superposition +
entanglement, the building blocks behind Shor's algorithm's period-finding
subroutine used against RSA/ECC).

IMPORTANT (Section 3 / 75): this is a LOCAL SIMULATION on a few qubits.
It is NOT a real attack against Bitcoin, Ethereum, RSA, or ECC, and it does
not run on real quantum hardware.
"""
from dataclasses import dataclass

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

_QUBIT_COUNT = 4
_SEED = 42

_INTERPRETATION = (
    "Local quantum simulation completed. This simulation demonstrates "
    "superposition and entanglement, the quantum-computing concepts "
    "relevant to Shor's-algorithm-style attacks on classical public-key "
    "cryptography (RSA/ECC). It does not represent a real-world attack "
    "against Bitcoin, Ethereum, or any live cryptographic system."
)

_EXPOSURE_TO_SCORE = {"LOW": 10.0, "MEDIUM": 30.0, "HIGH": 40.0, "CRITICAL": 75.0}
_SCORE_TO_PRIORITY = [(25, "LOW"), (50, "MEDIUM"), (75, "HIGH"), (101, "CRITICAL")]


@dataclass
class QuantumAssessmentResult:
    simulation_status: str
    qubit_count: int
    circuit_depth: int
    simulation_result: dict
    security_interpretation: str
    quantum_score: float
    migration_priority: str


def _run_simulation() -> tuple[str, int, dict]:
    circuit = QuantumCircuit(_QUBIT_COUNT, _QUBIT_COUNT)
    circuit.h(range(_QUBIT_COUNT))
    for qubit in range(_QUBIT_COUNT - 1):
        circuit.cx(qubit, qubit + 1)
    circuit.measure(range(_QUBIT_COUNT), range(_QUBIT_COUNT))

    simulator = AerSimulator(seed_simulator=_SEED)
    job = simulator.run(circuit, shots=512, seed_simulator=_SEED)
    result = job.result()
    counts = result.get_counts()

    return "COMPLETED", circuit.depth(), dict(counts)


def _migration_priority(score: float) -> str:
    for upper_bound, label in _SCORE_TO_PRIORITY:
        if score < upper_bound:
            return label
    return "CRITICAL"


def assess_quantum_exposure(quantum_exposure: str) -> QuantumAssessmentResult:
    status, depth, counts = _run_simulation()
    score = _EXPOSURE_TO_SCORE.get(quantum_exposure, 50.0)

    return QuantumAssessmentResult(
        simulation_status=status,
        qubit_count=_QUBIT_COUNT,
        circuit_depth=depth,
        simulation_result=counts,
        security_interpretation=_INTERPRETATION,
        quantum_score=score,
        migration_priority=_migration_priority(score),
    )
