"""Cryptographic Security Assessment (Section 16 / Phase 7).

Identifies the cryptographic profile associated with a wallet/transaction
and rates its exposure. This is an ASSESSMENT of cryptographic properties,
not a claim that any cryptocurrency has been broken.
"""
from dataclasses import dataclass

_PROFILES = {
    # crypto_score reflects this profile's contribution to the unified risk score
    # (Section 19) - NOT a claim that the algorithm is currently broken. Classical
    # ECDSA/RSA remain cryptographically sound today; the score captures their
    # long-term quantum-readiness posture, which is why it stays moderate rather
    # than critical for the algorithms every mainstream chain uses today.
    "ECDSA-secp256k1": {
        "key_type": "Classical Public-Key (Elliptic Curve)",
        "signature_type": "ECDSA",
        "security_category": "128-bit classical security",
        "quantum_exposure": "HIGH",
        "migration_status": "NOT MIGRATED",
        "crypto_score": 35.0,
    },
    "RSA-2048": {
        "key_type": "Classical Public-Key (Integer Factorization)",
        "signature_type": "RSA-PSS",
        "security_category": "112-bit classical security",
        "quantum_exposure": "CRITICAL",
        "migration_status": "NOT MIGRATED",
        "crypto_score": 55.0,
    },
    "ML-DSA-65": {
        "key_type": "Post-Quantum Lattice-Based",
        "signature_type": "ML-DSA (Dilithium)",
        "security_category": "NIST Level 3 PQC",
        "quantum_exposure": "LOW",
        "migration_status": "MIGRATED (PQC)",
        "crypto_score": 10.0,
    },
}

_DEFAULT_ALGORITHM = "ECDSA-secp256k1"


@dataclass
class CryptoAssessmentResult:
    algorithm: str
    key_type: str
    signature_type: str
    security_category: str
    quantum_exposure: str
    migration_status: str
    crypto_score: float


def assess_crypto_profile(algorithm: str | None) -> CryptoAssessmentResult:
    profile = _PROFILES.get(algorithm or _DEFAULT_ALGORITHM, _PROFILES[_DEFAULT_ALGORITHM])
    resolved_algorithm = algorithm if algorithm in _PROFILES else _DEFAULT_ALGORITHM
    return CryptoAssessmentResult(algorithm=resolved_algorithm, **profile)
