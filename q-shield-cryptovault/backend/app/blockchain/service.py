"""Blockchain audit logging service (Section 24-25 / Phase 10).

Talks to a LOCAL Hardhat Ethereum-compatible node over JSON-RPC via web3.py
and writes security decisions to the QShieldSecurityLog contract.

Fail-safe policy (Section 53): if the blockchain is unavailable, this
service NEVER fabricates a confirmation. It reports blockchain_status as
UNAVAILABLE and lets the rest of the pipeline (transaction analysis,
decision) continue to work and remain visible.
"""
import json
import logging
from dataclasses import dataclass
from pathlib import Path

from app.core.config import get_settings

logger = logging.getLogger("qshield.blockchain")

_DEPLOYMENT_PATH = Path(__file__).resolve().parents[3] / "blockchain" / "deployment.json"

_web3_client = None
_contract = None
_account = None
_load_attempted = False


@dataclass
class BlockchainWriteResult:
    status: str  # CONFIRMED | UNAVAILABLE
    tx_hash: str
    block_number: int
    network: str


def _ensure_loaded() -> bool:
    global _web3_client, _contract, _account, _load_attempted
    if _contract is not None:
        return True
    if _load_attempted:
        return False
    _load_attempted = True

    settings = get_settings()
    if not settings.blockchain_enabled:
        logger.warning("Blockchain logging disabled via configuration")
        return False

    try:
        from web3 import Web3

        if not _DEPLOYMENT_PATH.exists():
            logger.warning("Blockchain deployment info not found at %s", _DEPLOYMENT_PATH)
            return False

        deployment = json.loads(_DEPLOYMENT_PATH.read_text())
        w3 = Web3(Web3.HTTPProvider(settings.blockchain_rpc_url, request_kwargs={"timeout": 3}))
        if not w3.is_connected():
            logger.warning("Local Hardhat blockchain not reachable at %s", settings.blockchain_rpc_url)
            return False

        contract = w3.eth.contract(address=deployment["address"], abi=deployment["abi"])
        account = deployment["deployerAddress"]

        _web3_client, _contract, _account = w3, contract, account
        logger.info("Connected to local blockchain, contract at %s", deployment["address"])
        return True
    except Exception as exc:  # noqa: BLE001 - any RPC/deployment issue means "unavailable"
        logger.warning("Blockchain connection failed: %s", exc)
        return False


def record_security_decision(transaction_id: str, risk_score: float, decision: str) -> BlockchainWriteResult:
    if not _ensure_loaded():
        return BlockchainWriteResult(status="UNAVAILABLE", tx_hash="", block_number=0, network="LOCAL HARDHAT")

    try:
        tx_hash = _contract.functions.recordSecurityDecision(
            transaction_id, int(risk_score), decision
        ).transact({"from": _account})
        receipt = _web3_client.eth.wait_for_transaction_receipt(tx_hash, timeout=10)
        return BlockchainWriteResult(
            status="CONFIRMED",
            tx_hash=receipt["transactionHash"].hex(),
            block_number=receipt["blockNumber"],
            network="LOCAL HARDHAT",
        )
    except Exception as exc:  # noqa: BLE001
        logger.error("Blockchain write failed: %s", exc)
        return BlockchainWriteResult(status="UNAVAILABLE", tx_hash="", block_number=0, network="LOCAL HARDHAT")


def get_blockchain_status() -> dict:
    connected = _ensure_loaded()
    settings = get_settings()
    return {
        "status": "ONLINE" if connected else "UNAVAILABLE",
        "network": "LOCAL HARDHAT",
        "rpc_url": settings.blockchain_rpc_url,
        "contract_address": _DEPLOYMENT_PATH.exists() and json.loads(_DEPLOYMENT_PATH.read_text()).get("address", "") or "",
    }
