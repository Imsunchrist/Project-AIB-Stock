const hre = require("hardhat");
const fs = require("fs");
const path = require("path");

async function main() {
  console.log("\n🚀 Starting PortfolioTracker Deployment...\n");
  
  const [deployer] = await ethers.getSigners();
  const network = hre.network.name;
  
  console.log("═══════════════════════════════════════");
  console.log("📋 Deployment Information");
  console.log("═══════════════════════════════════════");
  console.log("Network:", network);
  console.log("Deployer:", deployer.address);
  
  const balance = await ethers.provider.getBalance(deployer.address);
  console.log("Balance:", ethers.formatEther(balance), "ETH");
  console.log("═══════════════════════════════════════\n");
  
  if (parseFloat(ethers.formatEther(balance)) < 0.01) {
    console.log("⚠️  Warning: Low balance. Deployment may fail.");
  }
  
  console.log("⏳ Deploying PortfolioTracker contract...");
  
  const PortfolioTracker = await ethers.getContractFactory("PortfolioTracker");
  const portfolioTracker = await PortfolioTracker.deploy();
  
  await portfolioTracker.waitForDeployment();
  
  const contractAddress = await portfolioTracker.getAddress();
  
  console.log("\n✅ PortfolioTracker deployed successfully!");
  console.log("═══════════════════════════════════════");
  console.log("📍 Contract Address:", contractAddress);
  console.log("═══════════════════════════════════════\n");
  
  const deploymentInfo = {
    network: network,
    contractAddress: contractAddress,
    deployer: deployer.address,
    deploymentTime: new Date().toISOString(),
    blockNumber: await ethers.provider.getBlockNumber(),
    chainId: (await ethers.provider.getNetwork()).chainId.toString()
  };
  
  const deploymentDir = path.join(__dirname, "../deployments");
  if (!fs.existsSync(deploymentDir)) {
    fs.mkdirSync(deploymentDir, { recursive: true });
  }
  
  const deploymentPath = path.join(deploymentDir, `${network}-deployment.json`);
  fs.writeFileSync(deploymentPath, JSON.stringify(deploymentInfo, null, 2));
  console.log("💾 Deployment info saved to:", deploymentPath);
  
  const artifactPath = path.join(
    __dirname, 
    "../../artifacts/contracts/PortfolioTracker.sol/PortfolioTracker.json"
  );
  
  if (fs.existsSync(artifactPath)) {
    const artifact = JSON.parse(fs.readFileSync(artifactPath, "utf8"));
    
    const backendDir = path.join(__dirname, "../../backend");
    if (!fs.existsSync(backendDir)) {
      fs.mkdirSync(backendDir, { recursive: true });
    }
    
    const abiPath = path.join(backendDir, "contract_abi.json");
    fs.writeFileSync(abiPath, JSON.stringify(artifact.abi, null, 2));
    console.log("📋 Contract ABI copied to:", abiPath);
    
    const contractInfoPath = path.join(backendDir, "contract_info.json");
    fs.writeFileSync(contractInfoPath, JSON.stringify({
      address: contractAddress,
      network: network,
      abi: artifact.abi
    }, null, 2));
    console.log("📄 Contract info saved to:", contractInfoPath);
  } else {
    console.log("⚠️  Artifact not found. Run 'npm run compile' first.");
  }
  
  const envBackendPath = path.join(__dirname, "../../backend/.env");
  let envContent = "";
  
  if (fs.existsSync(envBackendPath)) {
    envContent = fs.readFileSync(envBackendPath, "utf8");
    
    if (envContent.includes("CONTRACT_ADDRESS=")) {
      envContent = envContent.replace(
        /CONTRACT_ADDRESS=.*/,
        `CONTRACT_ADDRESS=${contractAddress}`
      );
    } else {
      envContent += `\nCONTACT_ADDRESS=${contractAddress}\n`;
    }
  } else {
    envContent = `CONTRACT_ADDRESS=${contractAddress}\n`;
  }
  
  fs.writeFileSync(envBackendPath, envContent);
  console.log("🔧 Backend .env updated with contract address\n");
  
  console.log("═══════════════════════════════════════");
  console.log("✅ Deployment Complete!");
  console.log("═══════════════════════════════════════");
  console.log("\n📝 Next Steps:");
  console.log("   1. Update backend/.env with RPC_URL");
  console.log("   2. Add your WALLET_PRIVATE_KEY to backend/.env");
  console.log("   3. Run: cd ../backend && python app.py\n");
  
  if (network === "sepolia" || network === "mainnet") {
    console.log("🔍 Verify on Etherscan:");
    console.log(`   npx hardhat verify --network ${network} ${contractAddress}\n`);
  }
  
  return contractAddress;
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("\n❌ Deployment Failed:");
    console.error(error);
    process.exit(1);
  });
