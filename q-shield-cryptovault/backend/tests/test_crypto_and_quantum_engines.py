from app.engines.crypto.engine import assess_crypto_profile
from app.engines.quantum.engine import assess_quantum_exposure


def test_ecdsa_profile_has_high_quantum_exposure():
    result = assess_crypto_profile("ECDSA-secp256k1")
    assert result.quantum_exposure == "HIGH"
    assert result.migration_status == "NOT MIGRATED"


def test_unknown_algorithm_falls_back_to_default():
    result = assess_crypto_profile("SOME-UNKNOWN-ALGO")
    assert result.algorithm == "ECDSA-secp256k1"


def test_pqc_profile_has_low_quantum_exposure():
    result = assess_crypto_profile("ML-DSA-65")
    assert result.quantum_exposure == "LOW"
    assert result.migration_status == "MIGRATED (PQC)"


def test_quantum_simulation_runs_locally_and_is_labelled_simulation():
    result = assess_quantum_exposure("HIGH")
    assert result.simulation_status == "COMPLETED"
    assert result.qubit_count > 0
    assert "local" in result.security_interpretation.lower()
    assert "not represent a real-world attack" in result.security_interpretation


def test_quantum_score_reflects_crypto_exposure():
    low = assess_quantum_exposure("LOW")
    critical = assess_quantum_exposure("CRITICAL")
    assert low.quantum_score < critical.quantum_score
    assert critical.migration_priority in ("HIGH", "CRITICAL")
