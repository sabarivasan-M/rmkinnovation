# Q-Shield CryptoVault
## Post-Quantum Secure Cryptocurrency Wallet & Blockchain Security System

**Team:** Team E.D.I.T.H  
**Project Type:** Cybersecurity + Blockchain + Quantum Computing / Post-Quantum Cryptography  
**Document Type:** Master Project Documentation  
**Document Status:** Engineering specification and project documentation  
**Presentation Baseline:** Current 7-slide Q-Shield CryptoVault presentation

---

## 1. Executive Summary

Q-Shield CryptoVault is a security decision and monitoring system designed around a simple problem:

> Cryptocurrency security has both a **present-day cyber-risk problem** and a **future cryptographic/quantum-risk problem**, but these risks are commonly considered as separate concerns.

The project proposes a unified security layer that evaluates a cryptocurrency transaction using multiple signals:

1. Transaction authentication
2. Transaction behaviour
3. Anomaly detection
4. Cybersecurity signals
5. Cryptographic security information
6. Quantum exposure / quantum-readiness
7. Security decision and blockchain logging

The system converts these signals into an explainable risk assessment and produces a decision such as:

- **APPROVE**
- **FLAG FOR VERIFICATION**
- **REJECT**

The central innovation is **not simply combining blockchain, AI and quantum computing**. The innovation is the connection between **current cyber/behavioural risk and future quantum-readiness into one security decision layer**.

The project also introduces a migration-awareness component. Instead of claiming that an entire cryptocurrency ecosystem can immediately be converted to post-quantum cryptography, Q-Shield focuses on identifying potentially vulnerable cryptographic profiles and assigning migration priority.

---

# 2. Problem Definition

## 2.1 Exact Problem

Cryptocurrency transactions depend on cryptographic mechanisms for authentication and transaction integrity. At the same time, cryptocurrency wallets and transaction systems face conventional security threats such as:

- Unauthorized transactions
- Fraudulent transactions
- Phishing
- Stolen wallet credentials
- Abnormal transaction behaviour
- Suspicious destination wallets
- Repeated authentication failures

There is also an emerging long-term concern: sufficiently capable quantum computers could threaten some public-key cryptographic assumptions used by existing systems.

The problem is therefore two-dimensional:

### Present

A transaction may be dangerous because of its current behaviour or cybersecurity context.

### Future

A cryptographic profile may eventually become vulnerable as quantum computing capabilities develop.

A security platform that only checks transaction behaviour can miss cryptographic exposure. A cryptographic assessment system alone cannot determine whether a transaction is currently suspicious.

Q-Shield addresses this separation by creating a common decision layer.

---

# 3. Existing Gap

The project identifies the following conceptual separation:

| Security Area | What It Typically Examines |
|---|---|
| Transaction monitoring | Transaction amount, frequency and behaviour |
| Cybersecurity monitoring | Authentication/security events and suspicious activity |
| Blockchain monitoring | Blockchain transactions, wallets and ledger activity |
| Cryptographic assessment | Algorithms and cryptographic assumptions |
| Post-quantum research | Quantum-resistant migration strategies |

The project gap is:

> These signals are not naturally connected into a single transaction-level security decision.

Q-Shield therefore proposes:

**Cyber Risk + Behavioural Risk + Cryptographic Risk + Quantum Readiness → Unified Security Decision**

---

# 4. Target Users

## 4.1 Primary Users

### Cryptocurrency Wallet Users

Users who need an additional security layer before approving sensitive transactions.

Relevant use cases:

- High-value transfers
- Transfers to unfamiliar destinations
- Unusual transaction frequency
- Suspicious authentication activity
- Security review before approval

### Security Analysts

Security personnel who need a centralized view of:

- Suspicious transactions
- Wallet behaviour
- Authentication anomalies
- Risk explanations
- Cryptographic exposure
- Quantum-readiness status

### Digital Asset / Blockchain Security Teams

Teams responsible for monitoring blockchain-connected applications and wallet activity.

---

# 5. Threat Model

Q-Shield considers two broad classes of threats.

## 5.1 Present-Day Cybersecurity Threats

### Credential Compromise

An attacker obtains wallet credentials or authentication information.

Potential consequence:

- Unauthorized transaction
- Unauthorized wallet access

### Phishing

A user is deceived into interacting with a malicious destination or providing sensitive credentials.

Potential consequence:

- Credential theft
- Fraudulent transaction
- Malicious destination interaction

### Abnormal Transaction Behaviour

A transaction differs significantly from the wallet's normal activity.

Examples:

- Sudden high-value transfer
- Unusual transaction frequency
- Unusual destination
- Behavioural deviation

### Suspicious Destination

A destination wallet or address may have characteristics that increase transaction risk.

### Authentication Anomalies

Examples:

- Repeated failed authentication attempts
- Unusual authentication pattern
- Authentication activity inconsistent with expected behaviour

---

# 6. Quantum Security Problem

## 6.1 Why Quantum Computing Matters

Modern cryptocurrency systems use cryptographic mechanisms to provide authentication and transaction integrity.

Some widely used public-key cryptographic assumptions may be threatened by sufficiently capable quantum computers.

The important distinction is:

> Q-Shield does not claim that a real quantum computer is currently breaking cryptocurrency transactions.

Instead, the quantum component is used to:

1. Explain the cryptographic vulnerability concept.
2. Simulate quantum-computing concepts locally.
3. Identify cryptographic exposure.
4. Translate that exposure into a readiness/migration assessment.

---

# 7. Proposed Solution

## 7.1 Core Pipeline

```text
TRANSACTION REQUEST
        ↓
AUTHENTICATION
        ↓
BEHAVIOUR ANALYSIS
        ↓
ANOMALY DETECTION
        ↓
CRYPTOGRAPHIC ASSESSMENT
        ↓
QUANTUM EXPOSURE ASSESSMENT
        ↓
UNIFIED RISK ENGINE
        ↓
RISK SCORE + EXPLANATION
        ↓
APPROVE / FLAG / REJECT
        ↓
BLOCKCHAIN SECURITY LOG
```

## 7.2 Core Processing Model

Q-Shield follows:

**CAPTURE → ANALYSE → QUANTIFY → DECIDE → LOG**

### Capture

Collect transaction and wallet-security information.

### Analyse

Evaluate behavioural, authentication, cybersecurity and cryptographic signals.

### Quantify

Convert relevant signals into interpretable risk factors.

### Decide

Generate a security outcome.

### Log

Store the decision and relevant event information for auditability.

---

# 8. Core Innovation

## Innovation Statement

> Q-Shield connects present-day cyber and behavioural risk with future quantum-readiness into one security decision layer.

The innovation consists of three primary ideas.

## 8.1 Unified Quantum-Cyber Risk Assessment

Instead of presenting separate dashboards for:

- Cybersecurity
- Transaction behaviour
- Cryptography
- Quantum exposure

Q-Shield combines their relevant signals.

## 8.2 Security Decision Before Approval

The system is designed around a decision:

```text
Transaction
    ↓
Risk Analysis
    ↓
Security Decision
    ↓
Approve / Flag / Reject
```

This moves the concept from passive monitoring toward decision support.

## 8.3 Quantum-Readiness Awareness

The system identifies profiles that may require greater attention because of their cryptographic exposure.

The intended progression is:

```text
ASSESS
   ↓
IDENTIFY EXPOSURE
   ↓
PRIORITIZE
   ↓
RECOMMEND
   ↓
CONTROLLED MIGRATION
```

---

# 9. System Objectives

## Primary Objectives

1. Detect suspicious transaction behaviour.
2. Identify abnormal wallet activity.
3. Incorporate cybersecurity signals into transaction risk.
4. Assess cryptographic exposure.
5. Introduce quantum-readiness assessment.
6. Produce an explainable security decision.
7. Maintain security decision history.
8. Provide migration-priority awareness for post-quantum readiness.

## Secondary Objectives

- Provide a centralized security dashboard.
- Reduce fragmented manual assessment.
- Make risk factors understandable to users.
- Demonstrate quantum concepts without requiring physical quantum hardware.
- Provide a modular architecture that can be expanded.

---

# 10. Functional Requirements

## FR-01 — Transaction Capture

The system shall accept transaction information such as:

- Sender/wallet identifier
- Destination
- Transaction value
- Transaction frequency
- Authentication context
- Relevant security metadata

## FR-02 — Authentication Assessment

The system shall evaluate available authentication-related signals.

Examples:

- Successful authentication
- Failed authentication attempts
- Repeated failures
- Unusual authentication pattern

## FR-03 — Behaviour Analysis

The system shall compare transaction characteristics with expected wallet behaviour.

Possible features:

- Transaction amount
- Transaction frequency
- Destination familiarity
- Time/activity pattern
- Behavioural deviation

## FR-04 — Anomaly Detection

The system shall identify transactions that exhibit abnormal patterns.

The prototype may use a Python-based anomaly detection component.

## FR-05 — Cryptographic Assessment

The system shall associate a transaction/wallet profile with relevant cryptographic information and determine whether the cryptographic profile requires additional security attention.

## FR-06 — Quantum Exposure Assessment

The system shall provide a quantum-readiness assessment based on cryptographic exposure.

## FR-07 — Risk Quantification

The system shall combine the selected risk factors into an interpretable risk assessment.

## FR-08 — Decision

The system shall generate one of:

- APPROVE
- FLAG
- REJECT

The final decision must be explainable.

## FR-09 — Blockchain Logging

Relevant transaction/security decisions shall be logged in the blockchain development environment or associated blockchain layer used by the prototype.

## FR-10 — Persistent Storage

Transaction/security records shall be persisted using PostgreSQL or SQLite depending on deployment mode.

---

# 11. Risk Scoring Model

## 11.1 Purpose

The risk engine converts multiple security signals into a single interpretable assessment.

The project presentation describes the concept as a:

**Unified Quantum-Cyber Risk Score**

## 11.2 Candidate Risk Factors

The system can consider:

- Transaction value
- Destination history
- Transaction frequency
- Behavioural anomaly
- Authentication events
- Cryptographic vulnerability
- Quantum exposure

## 11.3 Recommended Explainable Model

A deterministic weighted model is appropriate for the prototype because it is:

- Reproducible
- Easy to explain
- Easy to test
- Less dependent on opaque AI output
- Suitable for a student prototype

Conceptually:

```text
Overall Risk =
    Behaviour Risk
  + Transaction Risk
  + Authentication Risk
  + Cyber Risk
  + Cryptographic Risk
  + Quantum Exposure
```

Each factor should be normalized before aggregation.

A configurable implementation can use:

```text
Risk Score = Σ(weight_i × normalized_factor_i)
```

The exact weights must be documented and tested rather than presented as arbitrary numbers.

## 11.4 Explainability Requirement

The interface should not only show:

```text
Risk = 82
```

It should show:

```text
Risk = HIGH

Reasons:
- Transaction amount is significantly above normal
- Destination is unfamiliar
- Authentication failures detected
- Behavioural anomaly detected
- Cryptographic profile requires quantum-readiness review
```

This makes the decision auditable.

---

# 12. Decision Policy

A prototype decision policy can be configured using thresholds.

Example architecture:

```text
LOW RISK
    ↓
APPROVE

MEDIUM RISK
    ↓
FLAG FOR VERIFICATION

HIGH RISK
    ↓
REJECT / BLOCK PENDING REVIEW
```

The actual threshold values should be treated as configurable engineering parameters and validated through testing.

The project should never claim that a threshold mathematically guarantees security.

---

# 13. Artificial Intelligence / Machine Learning Component

## 13.1 Role

The project presentation identifies:

- Python feature processing
- Anomaly detection
- Deterministic risk-scoring engine

The AI/ML component should therefore be positioned primarily around **anomaly detection and feature analysis**, not as a vague claim that “AI secures the blockchain.”

## 13.2 Suitable Input Features

Potential features include:

- Transaction value
- Transaction frequency
- Historical destination interaction
- Time-based activity
- Authentication failure count
- Wallet behaviour deviation

## 13.3 Output

The anomaly detector can produce:

```text
Normal
OR
Anomalous
```

or an anomaly score.

That result then becomes one input to the deterministic risk engine.

## 13.4 Recommended Architecture

```text
Transaction Data
      ↓
Feature Engineering
      ↓
Anomaly Detector
      ↓
Anomaly Signal
      ↓
Unified Risk Engine
```

The anomaly model and its evaluation metrics must be documented separately once the implementation is finalized.

---

# 14. Quantum Computing Component

## 14.1 Technology

**Qiskit**

The project uses local quantum simulation rather than requiring physical quantum hardware.

## 14.2 Why Simulation?

A student prototype does not require access to physical quantum hardware to demonstrate the computational concept.

The simulation provides a controlled environment for demonstrating quantum circuits and cryptographic concepts.

## 14.3 Intended Quantum Flow

```text
Cryptographic Assumption
        ↓
Quantum Algorithm Concept
        ↓
Qiskit Circuit
        ↓
Local Simulation
        ↓
Interpretation
        ↓
Quantum Exposure / Readiness Indicator
```

## 14.4 Important Technical Boundary

The project should not claim:

- That the prototype has broken Bitcoin.
- That the prototype has broken Ethereum.
- That current cryptocurrency cryptography is already practically broken.
- That a simulator represents the performance of a future fault-tolerant quantum computer.

The correct claim is:

> The prototype uses quantum simulation to demonstrate the relevant quantum-computing concept and connect cryptographic exposure to a quantum-readiness assessment.

---

# 15. Post-Quantum Cryptography Layer

## 15.1 Purpose

The post-quantum component addresses the question:

> What should a system do when its current cryptographic assumptions require migration because of future quantum risk?

## 15.2 Migration Model

```text
CLASSICAL CRYPTOGRAPHY
        ↓
VULNERABILITY ASSESSMENT
        ↓
QUANTUM EXPOSURE
        ↓
MIGRATION PRIORITY
        ↓
PQC RECOMMENDATION
        ↓
CONTROLLED MIGRATION
```

## 15.3 Relevant PQC Standards

The project references NIST standards including:

- FIPS 203 — ML-KEM
- FIPS 204 — ML-DSA
- FIPS 205 — SLH-DSA

These standards should be treated as reference technologies for post-quantum migration planning.

## 15.4 Prototype Boundary

The prototype should distinguish between:

### Implemented

- Assessment
- Risk classification
- Quantum-readiness awareness
- Migration-priority recommendation

### Not automatically claimed as implemented

- Complete conversion of a production blockchain to PQC
- Automatic migration of real cryptocurrency wallets
- Universal multi-chain PQC compatibility
- Production-grade key migration

---

# 16. Blockchain Layer

## 16.1 Technology

- Ethereum-compatible development environment
- Solidity
- Hardhat

## 16.2 Role of Blockchain

Blockchain is used for:

- Transaction representation
- Wallet/contract interaction in the controlled environment
- Security-event logging
- Tamper-resistant history within the demonstration architecture

## 16.3 Why Blockchain Is Used

The blockchain layer provides a verifiable record of relevant security events and transaction decisions.

The important architecture is:

```text
Transaction
   ↓
Security Analysis
   ↓
Decision
   ↓
Security Event
   ↓
Blockchain Log
```

The project should clearly distinguish a local development/test blockchain from a production public blockchain.

---

# 17. Proposed Software Architecture

```text
┌─────────────────────────────────────────────┐
│                USER / WALLET                │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│            TRANSACTION REQUEST              │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│             FASTAPI BACKEND                 │
└──────────────────────┬──────────────────────┘
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
┌──────────────┐ ┌─────────────┐ ┌──────────────┐
│ Cyber /      │ │ Behaviour & │ │ Crypto /     │
│ Auth Signals │ │ Anomaly     │ │ Quantum      │
│              │ │ Detection   │ │ Assessment   │
└──────┬───────┘ └──────┬──────┘ └──────┬───────┘
       └─────────────────┼───────────────┘
                         ▼
              ┌─────────────────────┐
              │   UNIFIED RISK      │
              │      ENGINE         │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │ RISK + EXPLANATION  │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │ APPROVE / FLAG /    │
              │ REJECT              │
              └───────┬─────────────┘
                      │
            ┌─────────┴─────────┐
            ▼                   ▼
┌────────────────────┐ ┌───────────────────┐
│ Blockchain Logging │ │ Database          │
│ Solidity/Hardhat   │ │ PostgreSQL/SQLite │
└────────────────────┘ └───────────────────┘
```

---

# 18. Technology Stack

## Frontend

| Technology | Purpose |
|---|---|
| React | Web application UI |
| TypeScript | Type-safe frontend development |
| Tailwind CSS | Interface styling |

## Backend

| Technology | Purpose |
|---|---|
| Python | Security/risk processing |
| FastAPI | Backend API layer |

## Security and AI

| Technology | Purpose |
|---|---|
| Python feature processing | Transaction/security feature preparation |
| Anomaly detection | Detection of unusual transaction behaviour |
| Deterministic risk engine | Explainable risk aggregation |

## Quantum

| Technology | Purpose |
|---|---|
| Qiskit | Quantum circuit development |
| Local quantum simulation | Demonstration of quantum-computing concepts |

## Blockchain

| Technology | Purpose |
|---|---|
| Ethereum-compatible environment | Blockchain demonstration environment |
| Solidity | Smart-contract development |
| Hardhat | Blockchain development/testing |

## Database

| Technology | Purpose |
|---|---|
| PostgreSQL | Persistent application storage |
| SQLite | Lightweight/local deployment |

---

# 19. API Layer

The backend should expose modular endpoints.

Recommended API structure:

```text
/api/v1/transactions
/api/v1/transactions/{id}
/api/v1/risk/analyse
/api/v1/risk/{transaction_id}
/api/v1/wallets
/api/v1/wallets/{id}
/api/v1/quantum/assess
/api/v1/crypto/assess
/api/v1/anomalies
/api/v1/security/events
/api/v1/decisions
```

Example transaction analysis flow:

```text
POST /api/v1/risk/analyse
        ↓
Validate request
        ↓
Extract features
        ↓
Run anomaly analysis
        ↓
Run cryptographic assessment
        ↓
Run quantum-readiness assessment
        ↓
Calculate risk
        ↓
Generate explanation
        ↓
Return decision
```

---

# 20. Suggested Data Model

## Wallet

```text
Wallet
- wallet_id
- address
- profile_status
- transaction_count
- average_transaction_value
- known_destinations
- cryptographic_profile
- quantum_readiness_status
- created_at
```

## Transaction

```text
Transaction
- transaction_id
- sender
- destination
- amount
- timestamp
- authentication_status
- anomaly_score
- cyber_risk
- crypto_risk
- quantum_risk
- overall_risk
- decision
```

## Security Event

```text
SecurityEvent
- event_id
- wallet_id
- transaction_id
- event_type
- severity
- description
- timestamp
```

## Risk Assessment

```text
RiskAssessment
- assessment_id
- transaction_id
- transaction_risk
- behaviour_risk
- authentication_risk
- cyber_risk
- crypto_risk
- quantum_risk
- total_risk
- explanation
- decision
- timestamp
```

---

# 21. Dashboard Requirements

The dashboard should prioritize decisions rather than decoration.

## Main Dashboard

Display:

- Total transactions analysed
- Low-risk transactions
- Flagged transactions
- High-risk transactions
- Quantum-exposure profiles
- Recent security events

## Transaction Detail

For every transaction:

```text
Transaction ID
Sender
Destination
Value
Behaviour Status
Authentication Status
Anomaly Score
Cryptographic Status
Quantum Exposure
Overall Risk
Decision
Reasons
```

## Risk Explanation

Example:

```text
HIGH RISK — FLAG

Primary contributors:
1. Unusual transaction value
2. New destination
3. Abnormal transaction frequency
4. Repeated authentication failures

Quantum readiness:
Cryptographic profile requires migration review.
```

---

# 22. Security Decision Example

## Scenario A — Normal Transaction

```text
Known destination
Normal transaction value
Normal frequency
Successful authentication
No significant anomaly
No immediate cryptographic concern
```

Expected:

**APPROVE**

---

## Scenario B — Suspicious Transaction

```text
Unfamiliar destination
Transaction value above normal
Repeated authentication failures
Behavioural anomaly detected
```

Expected:

**FLAG**

Explanation should identify the contributing factors.

---

## Scenario C — High-Risk Transaction

```text
Unusual transaction value
Suspicious destination
Major behavioural deviation
Authentication anomalies
High security risk
```

Expected:

**REJECT / BLOCK PENDING REVIEW**

The exact implementation should define whether REJECT means hard rejection or a security hold.

---

# 23. Project Planner Bandwidth / Process Transformation

## Before Q-Shield

```text
Transaction
    ↓
Check transaction
    ↓
Check wallet activity
    ↓
Review security alerts
    ↓
Check cryptographic information
    ↓
Manual risk assessment
    ↓
Decision
```

## With Q-Shield

```text
Transaction
    ↓
Unified Security Analysis
    ↓
Risk Score + Explanation
    ↓
Prioritized Decision
    ↓
APPROVE / FLAG / REJECT
```

## Operational Impact

The intended improvement is not “remove humans.”

The system is better described as:

> Reduce fragmented investigation and give the user/security analyst a prioritized, explainable decision.

---

# 24. Benefits

## Security Benefits

- Earlier identification of suspicious transaction behaviour
- Better visibility of abnormal wallet activity
- Centralized view of cryptographic exposure
- Quantum-readiness awareness
- Explainable risk decisions

## Operational Benefits

- Reduced manual investigation
- Faster prioritization of high-risk transactions
- Centralized security information
- Consistent risk assessment

## Financial Benefits

Potentially:

- Reduced exposure to fraudulent transfers
- Faster response to suspicious activity
- Reduced investigation effort

These are expected benefits, not guaranteed measured outcomes until validated experimentally.

## Strategic Benefits

- Cybersecurity resilience
- Digital asset security monitoring
- Post-quantum readiness awareness
- Secure digital-financial infrastructure planning

---

# 25. Technical Feasibility

The architecture is feasible as a software prototype because it can use controlled development environments.

| Requirement | Implementation Approach |
|---|---|
| Web interface | React |
| API | FastAPI |
| Security processing | Python |
| Anomaly detection | Python |
| Risk engine | Deterministic Python engine |
| Quantum demonstration | Qiskit local simulation |
| Blockchain | Solidity + Hardhat |
| Persistent storage | PostgreSQL |
| Lightweight local storage | SQLite |

No physical quantum computer is required for the prototype.

---

# 26. Scalability Strategy

The system is designed as modular components.

```text
Frontend
   ↓
API Layer
   ↓
Risk Engine
   ├── Security Analysis
   ├── Behaviour Analysis
   ├── Anomaly Detection
   ├── Crypto Assessment
   └── Quantum Assessment
   ↓
Decision Layer
   ↓
Logging + Database
```

This separation allows components to be upgraded independently.

Possible engineering improvements later include:

- More sophisticated anomaly models
- Additional blockchain networks
- External threat intelligence
- Stronger identity/authentication
- Production-grade key management
- Enterprise-scale event streaming

These are architectural extension possibilities, not current implementation claims.

---

# 27. Challenges and Mitigation

## Challenge 1 — Quantum Hardware Availability

### Problem

Physical quantum hardware may not be available for a student prototype.

### Mitigation

Use Qiskit local simulation to demonstrate quantum-computing concepts.

---

## Challenge 2 — Risk Score May Appear Arbitrary

### Problem

A single number without an explanation is difficult to trust.

### Mitigation

Expose:

- Individual risk factors
- Normalized values
- Weights
- Thresholds
- Decision rationale

---

## Challenge 3 — PQC Migration Complexity

### Problem

Migrating a real cryptocurrency ecosystem to post-quantum cryptography is a complex systems problem.

### Mitigation

The prototype focuses on:

**ASSESS → PRIORITIZE → RECOMMEND**

rather than claiming automatic ecosystem-wide migration.

---

## Challenge 4 — Limited Real-World Transaction Data

### Problem

A student prototype may not have access to representative private wallet-security datasets.

### Mitigation

Use reproducible synthetic/demo transaction data and clearly label it as such.

Any model evaluation must report the actual dataset and methodology used.

---

## Challenge 5 — False Positives

### Problem

Aggressive security thresholds can incorrectly flag legitimate transactions.

### Mitigation

Combine multiple signals instead of relying on one feature.

Provide explainable reasons and allow human verification for flagged cases.

---

## Challenge 6 — Security Decisions Require Trust

### Problem

Users should not blindly trust an unexplained AI score.

### Mitigation

Use deterministic risk aggregation and provide a reason breakdown.

---

# 28. Testing Strategy

## 28.1 Unit Testing

Test independently:

- Risk-factor normalization
- Risk calculation
- Threshold logic
- Decision logic
- Transaction validation
- Quantum assessment mapping

## 28.2 Integration Testing

Test:

```text
Frontend
   ↓
FastAPI
   ↓
Risk Engine
   ↓
Database
```

and:

```text
Risk Engine
   ↓
Blockchain Logging
```

## 28.3 Scenario Testing

At minimum test:

1. Normal transaction
2. High-value transaction
3. New destination
4. Repeated authentication failures
5. Abnormal frequency
6. Multiple simultaneous risk signals
7. Quantum-vulnerable cryptographic profile
8. Low-risk profile

## 28.4 Performance Metrics

The prototype can report:

- Risk-analysis latency
- Decision latency
- Number of transactions processed
- Detection rate
- False-positive rate
- Risk-score consistency
- Number of profiles requiring quantum-readiness review

Do not publish numerical performance claims until the tests have actually been executed.

---

# 29. Evaluation Metrics

## Security Metrics

### Detection Rate

Percentage of known suspicious cases correctly identified.

### False Positive Rate

Percentage of legitimate transactions incorrectly flagged.

### Precision

How many flagged transactions are actually suspicious.

### Recall

How many suspicious transactions are successfully detected.

## System Metrics

### Decision Latency

Time between transaction submission and risk decision.

### Processing Throughput

Transactions processed per unit time.

### Reliability

Percentage of test cases completed without system failure.

## Explainability Metrics

Evaluate whether users can identify why a transaction received its decision.

---

# 30. Prototype Demonstration Plan

The strongest demonstration should focus on a visible security decision.

## Demo Sequence

### Step 1 — Normal Transaction

Submit a normal transaction.

Show:

```text
LOW RISK
APPROVE
```

### Step 2 — Suspicious Transaction

Change:

- Transaction amount
- Destination
- Frequency
- Authentication failures

Show the risk contributors.

Result:

```text
HIGHER RISK
FLAG
```

### Step 3 — Cryptographic / Quantum Assessment

Show a cryptographic profile and its quantum-readiness classification.

### Step 4 — Qiskit Demonstration

Show the quantum circuit/simulation component and explain what it demonstrates.

### Step 5 — Final Decision

Return:

```text
APPROVE / FLAG / REJECT
```

### Step 6 — Security Log

Show the decision/event recorded in the blockchain development environment.

---

# 31. Recommended 2-Minute Jury Explanation

## Opening

> “Cryptocurrency security has two problems: what can attack a transaction today, and what could threaten its cryptography tomorrow.”

## Problem

> “Today we have phishing, stolen credentials, abnormal transactions and suspicious wallets. At the same time, future quantum computers may threaten some public-key cryptographic assumptions.”

## Solution

> “Q-Shield connects these signals into one security decision layer.”

## Flow

> “For every transaction, we capture authentication and transaction information, analyse behaviour and anomalies, assess cryptographic and quantum exposure, calculate an explainable risk score, and produce approve, flag or reject.”

## Innovation

> “Our innovation is not simply using blockchain, AI and quantum computing together. It is connecting present-day cyber risk with future quantum-readiness in the same decision.”

## Close

> “Q-Shield helps protect today's transactions while preparing for tomorrow's cryptographic threat.”

---

# 32. Research Foundation

The presentation references research and standards related to blockchain quantum attacks, post-quantum blockchain migration, quantum-resistant signatures and Qiskit.

## Referenced Research

### A Novel Transition Protocol to Post-Quantum Cryptocurrency Blockchains

Authors:

- Almuhammadi
- Alghamdi

Year referenced in presentation:

**2025**

Relevance:

- Post-quantum transition
- Cryptocurrency blockchain migration

---

### Vulnerability of Blockchain Technologies to Quantum Attacks

Authors:

- Kearney
- Perez-Delgado

Year referenced in presentation:

**2021**

Relevance:

- Quantum threats against blockchain technologies

---

### A Blockchain System Based on Quantum-Resistant Digital Signature

Authors:

- Zhang et al.

Year referenced in presentation:

**2021**

Relevance:

- Quantum-resistant blockchain signatures

---

# 33. Standards and Technical References

The presentation references NIST Post-Quantum Cryptography standards:

- **FIPS 203 — ML-KEM — 2024**
- **FIPS 204 — ML-DSA — 2024**
- **FIPS 205 — SLH-DSA — 2024**

Additional technical references listed in the presentation:

- IBM Quantum — Qiskit Tutorials
- IBM Quantum — Getting Started with Qiskit
- Ethereum — Transactions resources

Before final submission, the team should maintain a bibliography containing the exact official URLs, paper DOI/arXiv information where applicable, access dates and complete citation format.

---

# 34. Project Terminology

| Term | Meaning in Q-Shield |
|---|---|
| Cyber Risk | Risk arising from security events, authentication and suspicious behaviour |
| Behavioural Risk | Risk derived from deviation from expected wallet/transaction behaviour |
| Anomaly | Transaction/activity pattern that differs from expected behaviour |
| Cryptographic Risk | Exposure associated with cryptographic mechanisms or assumptions |
| Quantum Exposure | Degree to which the cryptographic profile requires quantum-readiness attention |
| PQC | Post-Quantum Cryptography |
| Risk Engine | Component that combines normalized risk signals |
| Decision Layer | Component that maps risk assessment to approve/flag/reject |
| Security Event | Recorded security-related activity |
| Quantum Simulation | Classical simulation of quantum circuits/concepts |
| Wallet Profile | Security/behavioural/cryptographic representation of a wallet |
| Migration Priority | Relative urgency for post-quantum readiness |

---

# 35. What Q-Shield Is NOT

To maintain technical credibility, the project must avoid overclaiming.

Q-Shield is **not**:

- A replacement for the entire blockchain protocol.
- A guarantee of cryptocurrency security.
- A system that currently breaks real-world cryptocurrency cryptography.
- A claim that quantum computers can already steal cryptocurrency at scale.
- A complete production post-quantum migration platform.
- A replacement for secure wallet/key management.
- A system that automatically prevents every fraudulent transaction.
- Proof that a synthetic dataset represents all real-world cryptocurrency behaviour.

The prototype demonstrates the proposed architecture and security decision concept.

---

# 36. Implementation Status Framework

For project development and presentation, every feature should be classified as one of the following:

### IMPLEMENTED

The feature works in the current prototype and can be demonstrated.

### SIMULATED

The feature is represented using controlled/synthetic data or local simulation.

### INTEGRATED

The feature is connected to another working system/component.

### CONCEPTUAL

The feature is architecturally designed but not implemented.

This distinction is essential when discussing quantum computing, PQC migration and blockchain integration with judges.

---

# 37. Recommended Repository Structure

```text
q-shield-cryptovault/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── hooks/
│   │   ├── types/
│   │   └── utils/
│   ├── package.json
│   └── README.md
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── risk_engine/
│   │   ├── anomaly/
│   │   ├── crypto/
│   │   └── quantum/
│   ├── tests/
│   ├── requirements.txt
│   └── README.md
│
├── blockchain/
│   ├── contracts/
│   ├── scripts/
│   ├── test/
│   ├── hardhat.config.*
│   └── README.md
│
├── data/
│   ├── sample/
│   ├── synthetic/
│   └── schemas/
│
├── docs/
│   ├── architecture/
│   ├── research/
│   └── diagrams/
│
├── .env.example
├── README.md
└── LICENSE
```

---

# 38. Configuration Principles

Sensitive information must never be hardcoded.

Use environment variables for:

```text
DATABASE_URL
API_BASE_URL
BLOCKCHAIN_RPC_URL
PRIVATE_KEY
CONTRACT_ADDRESS
```

The `.env` file must not be committed to version control.

Use `.env.example` for documentation.

---

# 39. Security Requirements for the Prototype

Even though this is an academic prototype, the following practices should be followed:

- Never store real private keys in source code.
- Never use real wallet credentials in demonstrations.
- Use test accounts and local development networks.
- Validate all API inputs.
- Avoid exposing sensitive wallet information unnecessarily.
- Keep blockchain test credentials separate from production credentials.
- Log security decisions without storing secrets.
- Use HTTPS when deployed.
- Apply authentication and authorization to administrative endpoints.

---

# 40. Important Design Principle

The project should follow:

> **Deterministic where decisions must be trusted; intelligent where patterns must be discovered.**

Therefore:

### Anomaly Detection

Can use ML/statistical methods.

### Risk Aggregation

Should remain deterministic and explainable.

### Quantum Component

Should demonstrate and interpret quantum concepts rather than make unsupported claims.

### Final Decision

Should have transparent rules and reasons.

---

# 41. Project Architecture in One View

```text
                 ┌───────────────────────┐
                 │      USER / WALLET    │
                 └───────────┬───────────┘
                             │
                             ▼
                 ┌───────────────────────┐
                 │  TRANSACTION REQUEST │
                 └───────────┬───────────┘
                             │
                             ▼
                 ┌───────────────────────┐
                 │      FASTAPI API      │
                 └───────────┬───────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          ▼                  ▼                  ▼
   Authentication      Behaviour/AI       Crypto/Quantum
   & Cyber Signals      Analysis           Assessment
          │                  │                  │
          └──────────────────┼──────────────────┘
                             ▼
                 ┌───────────────────────┐
                 │    UNIFIED RISK      │
                 │       ENGINE         │
                 └───────────┬───────────┘
                             │
                             ▼
                 ┌───────────────────────┐
                 │ RISK + EXPLANATION   │
                 └───────────┬───────────┘
                             │
                             ▼
                 ┌───────────────────────┐
                 │ APPROVE / FLAG /     │
                 │ REJECT               │
                 └───────────┬───────────┘
                             │
                   ┌─────────┴─────────┐
                   ▼                   ▼
          ┌─────────────────┐  ┌─────────────────┐
          │ Blockchain Log  │  │ PostgreSQL /    │
          │ Solidity/Hardhat│  │ SQLite          │
          └─────────────────┘  └─────────────────┘
```

---

# 42. Final Project Definition

## One-Line Definition

> **Q-Shield CryptoVault is a unified security decision layer that combines transaction behaviour, cybersecurity signals, cryptographic exposure and quantum-readiness assessment to produce explainable cryptocurrency transaction decisions.**

## Three-Word Architecture

**DETECT → QUANTIFY → PREPARE**

### DETECT

Identify suspicious transaction and cybersecurity behaviour.

### QUANTIFY

Convert multiple signals into an explainable risk assessment.

### PREPARE

Identify quantum exposure and provide post-quantum migration awareness.

---

# 43. Final Conclusion

Q-Shield CryptoVault addresses a security gap created by the separation of conventional cryptocurrency security monitoring and emerging post-quantum readiness.

The proposed system combines transaction analysis, authentication signals, behavioural anomaly detection, cryptographic assessment and quantum-readiness into a unified decision layer.

Its strongest engineering characteristic is the separation between:

- **Detection**
- **Risk quantification**
- **Security decision**
- **Quantum-readiness assessment**
- **Blockchain logging**

The project should be presented as a practical security decision system rather than as a claim to have solved post-quantum cryptocurrency security completely.

The final message of the project is:

> **Protect today's transactions while preparing for tomorrow's cryptographic threat.**

---

# 44. Presentation-to-Implementation Traceability

| Presentation Area | Implementation Component |
|---|---|
| Problem | Threat model + security requirements |
| Unified risk | Risk engine |
| Behaviour analysis | Feature processing + anomaly detection |
| Cybersecurity | Authentication/security-event processing |
| Cryptographic assessment | Crypto assessment service |
| Quantum component | Qiskit module |
| PQC readiness | Migration assessment/recommendation module |
| Decision | Decision engine |
| Blockchain | Solidity + Hardhat |
| Database | PostgreSQL/SQLite |
| Dashboard | React + TypeScript + Tailwind |
| Feasibility | Modular software architecture |
| Impact | Decision-time/investigation-effort evaluation |
| Research | NIST + academic + IBM Quantum + Ethereum references |

---

# 45. Documentation Rule for the Team

Before the final demonstration, update this master document with actual implementation evidence.

For every major component, record:

```text
Feature
├── What it does
├── Input
├── Processing
├── Output
├── Technology
├── Implemented / Simulated / Conceptual
├── Test case
└── Measured result
```

This prevents the presentation from claiming capabilities that the prototype cannot demonstrate.

**End of Master Project Documentation**

