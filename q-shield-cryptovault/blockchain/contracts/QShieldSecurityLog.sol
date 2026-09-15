// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title QShieldSecurityLog
/// @notice Tamper-resistant demonstration log of Q-Shield security decisions.
/// @dev This contract demonstrates blockchain-backed audit logging for a
/// security decision layer. It does NOT make any wallet "quantum-safe" and
/// is intended to run on a local Hardhat network for this prototype.
contract QShieldSecurityLog {
    struct SecurityRecord {
        string transactionId;
        uint256 riskScore;
        string decision;
        uint256 timestamp;
        address submittedBy;
    }

    SecurityRecord[] private records;
    mapping(string => uint256) private transactionIdToIndex;
    mapping(string => bool) private transactionExists;

    event SecurityDecisionRecorded(
        string indexed transactionId,
        uint256 riskScore,
        string decision,
        uint256 timestamp,
        uint256 recordIndex
    );

    function recordSecurityDecision(
        string calldata transactionId,
        uint256 riskScore,
        string calldata decision
    ) external returns (uint256 recordIndex) {
        require(bytes(transactionId).length > 0, "transactionId required");
        require(riskScore <= 100, "riskScore must be 0-100");
        require(!transactionExists[transactionId], "transactionId already recorded");

        records.push(
            SecurityRecord({
                transactionId: transactionId,
                riskScore: riskScore,
                decision: decision,
                timestamp: block.timestamp,
                submittedBy: msg.sender
            })
        );

        recordIndex = records.length - 1;
        transactionIdToIndex[transactionId] = recordIndex;
        transactionExists[transactionId] = true;

        emit SecurityDecisionRecorded(transactionId, riskScore, decision, block.timestamp, recordIndex);
    }

    function getRecordCount() external view returns (uint256) {
        return records.length;
    }

    function getRecordByIndex(uint256 index) external view returns (SecurityRecord memory) {
        require(index < records.length, "index out of range");
        return records[index];
    }

    function getRecordByTransactionId(string calldata transactionId) external view returns (SecurityRecord memory) {
        require(transactionExists[transactionId], "transactionId not found");
        return records[transactionIdToIndex[transactionId]];
    }
}
