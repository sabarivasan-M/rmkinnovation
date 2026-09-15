import { artifacts, ethers } from "hardhat";
import * as fs from "fs";
import * as path from "path";

async function main() {
  const [deployer] = await ethers.getSigners();

  const Factory = await ethers.getContractFactory("QShieldSecurityLog");
  const contract = await Factory.deploy();
  await contract.waitForDeployment();

  const address = await contract.getAddress();
  const artifact = await artifacts.readArtifact("QShieldSecurityLog");

  const deployment = {
    address,
    deployerAddress: deployer.address,
    abi: artifact.abi,
    network: "localhost",
    deployedAt: new Date().toISOString(),
  };

  const outPath = path.join(__dirname, "..", "deployment.json");
  fs.writeFileSync(outPath, JSON.stringify(deployment, null, 2));

  console.log("QShieldSecurityLog deployed to:", address);
  console.log("Deployment info written to:", outPath);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
