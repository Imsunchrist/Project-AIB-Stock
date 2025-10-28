const hre = require("hardhat");
const fs = require("fs");
const path = require("path");

async function main() {
  console.log("\n🔗 PortfolioTracker Interaction Script\n");
  
  const deploymentPath = path.join(
    __dirname, 
    `../deployments/${hre.network.name}-deployment.json`
  );
  
  if (!fs.existsSync(deploymentPath)) {
    console.log("❌ No deployment found for", hre.network.name);
    console.log("   Run deployment first: npm run deploy:local");
    return;
  }
  
  const deployment = JSON.parse(fs.readFileSync(deploymentPath, "utf8"));
  const contractAddress = deployment.contractAddress;
  
  console.log("Network:", hre.network.name);
  console.log("Contract:", contractAddress);
  console.log("═══════════════════════════════════════\n");
  
  const [owner, user1, user2] = await ethers.getSigners();
  console.log("Owner:", owner.address);
  console.log("User1:", user1.address);
  console.log("User2:", user2.address, "\n");
  
  const PortfolioTracker = await ethers.getContractFactory("PortfolioTracker");
  const portfolioTracker = PortfolioTracker.attach(contractAddress);
  
  console.log("📊 Testing Contract Functions\n");
  
  console.log("1️⃣ Adding investment for User1...");
  const tx1 = await portfolioTracker.connect(user1).addInvestment(
    "Apple Inc.",
    "AAPL",
    ethers.parseUnits("10", 2),
    ethers.parseUnits("175.50", 2)
  );
  await tx1.wait();
  console.log("   ✅ Investment added. TX:", tx1.hash);
  
  console.log("\n2️⃣ Adding another investment for User1...");
  const tx2 = await portfolioTracker.connect(user1).addInvestment(
    "Microsoft Corporation",
    "MSFT",
    ethers.parseUnits("5", 2),
    ethers.parseUnits("380.25", 2)
  );
  await tx2.wait();
  console.log("   ✅ Investment added. TX:", tx2.hash);
  
  console.log("\n3️⃣ Getting User1's investment IDs...");
  const ids = await portfolioTracker.connect(user1).getMyInvestmentIds();
  console.log("   Investment IDs:", ids.map(id => id.toString()));
  
  console.log("\n4️⃣ Getting investment details...");
  for (let id of ids) {
    const inv = await portfolioTracker.connect(user1).getInvestment(id);
    console.log(`\n   Investment #${id}:`);
    console.log(`   Company: ${inv[0]}`);
    console.log(`   Symbol: ${inv[1]}`);
    console.log(`   Shares: ${ethers.formatUnits(inv[2], 2)}`);
    console.log(`   Price: $${ethers.formatUnits(inv[3], 2)}`);
    console.log(`   Timestamp: ${new Date(Number(inv[4]) * 1000).toISOString()}`);
    console.log(`   Active: ${inv[5]}`);
  }
  
  console.log("\n5️⃣ Getting active investment count...");
  const activeCount = await portfolioTracker.connect(user1).getActiveInvestmentCount();
  console.log("   Active investments:", activeCount.toString());
  
  console.log("\n6️⃣ Getting total invested amount...");
  const totalInvested = await portfolioTracker.connect(user1).getTotalInvested();
  console.log("   Total invested: $", ethers.formatUnits(totalInvested, 4));
  
  console.log("\n7️⃣ Removing first investment...");
  const tx3 = await portfolioTracker.connect(user1).removeInvestment(ids[0]);
  await tx3.wait();
  console.log("   ✅ Investment removed. TX:", tx3.hash);
  
  console.log("\n8️⃣ Checking active count after removal...");
  const newActiveCount = await portfolioTracker.connect(user1).getActiveInvestmentCount();
  console.log("   Active investments:", newActiveCount.toString());
  
  console.log("\n9️⃣ Getting all investments (batch)...");
  const allInvestments = await portfolioTracker.connect(user1).getAllMyInvestments();
  console.log(`   Found ${allInvestments[0].length} active investments`);
  
  for (let i = 0; i < allInvestments[0].length; i++) {
    console.log(`\n   Investment #${allInvestments[0][i]}:`);
    console.log(`   Company: ${allInvestments[1][i]}`);
    console.log(`   Symbol: ${allInvestments[2][i]}`);
    console.log(`   Shares: ${ethers.formatUnits(allInvestments[3][i], 2)}`);
    console.log(`   Price: $${ethers.formatUnits(allInvestments[4][i], 2)}`);
  }
  
  console.log("\n🔟 Testing with User2...");
  const tx4 = await portfolioTracker.connect(user2).addInvestment(
    "Tesla Inc.",
    "TSLA",
    ethers.parseUnits("3", 2),
    ethers.parseUnits("245.80", 2)
  );
  await tx4.wait();
  console.log("   ✅ User2 investment added. TX:", tx4.hash);
  
  const user2Count = await portfolioTracker.connect(user2).getActiveInvestmentCount();
  console.log("   User2 active investments:", user2Count.toString());
  
  console.log("\n═══════════════════════════════════════");
  console.log("✅ All tests completed successfully!");
  console.log("═══════════════════════════════════════\n");
  
  console.log("📊 Final Summary:");
  console.log("   User1 active investments:", newActiveCount.toString());
  console.log("   User2 active investments:", user2Count.toString());
  console.log("   Total counter:", (await portfolioTracker.investmentCounter()).toString());
  console.log("");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("\n❌ Interaction Failed:");
    console.error(error);
    process.exit(1);
  });
