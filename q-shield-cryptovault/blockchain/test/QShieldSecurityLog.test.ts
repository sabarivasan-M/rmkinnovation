import { expect } from "chai";
import { ethers } from "hardhat";
import { anyValue } from "@nomicfoundation/hardhat-chai-matchers/withArgs";

describe("QShieldSecurityLog", function () {
  async function deployFixture() {
    const Factory = await ethers.getContractFactory("QShieldSecurityLog");
    const contract = await Factory.deploy();
    await contract.waitForDeployment();
    return contract;
  }

  it("deploys with zero records", async function () {
    const contract = await deployFixture();
    expect(await contract.getRecordCount()).to.equal(0n);
  });

  it("records a security decision and can retrieve it by transaction id", async function () {
    const contract = await deployFixture();

    const tx = await contract.recordSecurityDecision("TX-QS-2026-0001", 82, "REJECT");
    await tx.wait();

    expect(await contract.getRecordCount()).to.equal(1n);

    const record = await contract.getRecordByTransactionId("TX-QS-2026-0001");
    expect(record.transactionId).to.equal("TX-QS-2026-0001");
    expect(record.riskScore).to.equal(82n);
    expect(record.decision).to.equal("REJECT");
  });

  it("rejects a risk score above 100", async function () {
    const contract = await deployFixture();
    await expect(contract.recordSecurityDecision("TX-QS-2026-0002", 150, "REJECT")).to.be.revertedWith(
      "riskScore must be 0-100"
    );
  });

  it("rejects a duplicate transaction id", async function () {
    const contract = await deployFixture();
    await (await contract.recordSecurityDecision("TX-QS-2026-0003", 10, "APPROVE")).wait();
    await expect(contract.recordSecurityDecision("TX-QS-2026-0003", 20, "FLAG")).to.be.revertedWith(
      "transactionId already recorded"
    );
  });

  it("emits SecurityDecisionRecorded on write", async function () {
    const contract = await deployFixture();
    await expect(contract.recordSecurityDecision("TX-QS-2026-0004", 30, "FLAG"))
      .to.emit(contract, "SecurityDecisionRecorded")
      .withArgs("TX-QS-2026-0004", 30n, "FLAG", anyValue, 0n);
  });
});
