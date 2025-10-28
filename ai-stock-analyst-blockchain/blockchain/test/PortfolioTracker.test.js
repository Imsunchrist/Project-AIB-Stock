const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("PortfolioTracker", function () {
  let portfolioTracker;
  let owner;
  let user1;
  let user2;

  beforeEach(async function () {
    [owner, user1, user2] = await ethers.getSigners();
    
    const PortfolioTracker = await ethers.getContractFactory("PortfolioTracker");
    portfolioTracker = await PortfolioTracker.deploy();
    await portfolioTracker.waitForDeployment();
  });

  describe("Deployment", function () {
    it("Should deploy with investment counter at 0", async function () {
      expect(await portfolioTracker.investmentCounter()).to.equal(0);
    });
  });

  describe("Adding Investments", function () {
    it("Should add investment successfully", async function () {
      await portfolioTracker.connect(user1).addInvestment(
        "Apple Inc.",
        "AAPL",
        ethers.parseUnits("10", 2),
        ethers.parseUnits("175.50", 2)
      );
      
      expect(await portfolioTracker.investmentCounter()).to.equal(1);
      
      const ids = await portfolioTracker.connect(user1).getMyInvestmentIds();
      expect(ids.length).to.equal(1);
    });

    it("Should emit InvestmentAdded event", async function () {
      await expect(
        portfolioTracker.connect(user1).addInvestment(
          "Microsoft",
          "MSFT",
          ethers.parseUnits("5", 2),
          ethers.parseUnits("380.25", 2)
        )
      ).to.emit(portfolioTracker, "InvestmentAdded");
    });

    it("Should revert with empty company name", async function () {
      await expect(
        portfolioTracker.connect(user1).addInvestment(
          "",
          "AAPL",
          ethers.parseUnits("10", 2),
          ethers.parseUnits("175", 2)
        )
      ).to.be.revertedWith("Company name required");
    });

    it("Should revert with zero shares", async function () {
      await expect(
        portfolioTracker.connect(user1).addInvestment(
          "Apple",
          "AAPL",
          0,
          ethers.parseUnits("175", 2)
        )
      ).to.be.revertedWith("Shares must be positive");
    });
  });

  describe("Getting Investments", function () {
    beforeEach(async function () {
      await portfolioTracker.connect(user1).addInvestment(
        "Apple Inc.",
        "AAPL",
        ethers.parseUnits("10", 2),
        ethers.parseUnits("175.50", 2)
      );
    });

    it("Should retrieve investment details", async function () {
      const inv = await portfolioTracker.connect(user1).getInvestment(1);
      
      expect(inv[0]).to.equal("Apple Inc.");
      expect(inv[1]).to.equal("AAPL");
      expect(inv[2]).to.equal(ethers.parseUnits("10", 2));
      expect(inv[3]).to.equal(ethers.parseUnits("175.50", 2));
      expect(inv[5]).to.equal(true);
    });

    it("Should not allow other users to view investment", async function () {
      await expect(
        portfolioTracker.connect(user2).getInvestment(1)
      ).to.be.revertedWith("Not your investment");
    });
  });

  describe("Removing Investments", function () {
    beforeEach(async function () {
      await portfolioTracker.connect(user1).addInvestment(
        "Apple Inc.",
        "AAPL",
        ethers.parseUnits("10", 2),
        ethers.parseUnits("175.50", 2)
      );
    });

    it("Should remove investment successfully", async function () {
      await portfolioTracker.connect(user1).removeInvestment(1);
      
      const inv = await portfolioTracker.connect(user1).getInvestment(1);
      expect(inv[5]).to.equal(false);
    });

    it("Should emit InvestmentRemoved event", async function () {
      await expect(
        portfolioTracker.connect(user1).removeInvestment(1)
      ).to.emit(portfolioTracker, "InvestmentRemoved");
    });

    it("Should not allow other users to remove investment", async function () {
      await expect(
        portfolioTracker.connect(user2).removeInvestment(1)
      ).to.be.revertedWith("Not your investment");
    });

    it("Should not allow removing already removed investment", async function () {
      await portfolioTracker.connect(user1).removeInvestment(1);
      
      await expect(
        portfolioTracker.connect(user1).removeInvestment(1)
      ).to.be.revertedWith("Already removed");
    });
  });

  describe("Portfolio Statistics", function () {
    beforeEach(async function () {
      await portfolioTracker.connect(user1).addInvestment(
        "Apple Inc.",
        "AAPL",
        ethers.parseUnits("10", 2),
        ethers.parseUnits("175.50", 2)
      );
      
      await portfolioTracker.connect(user1).addInvestment(
        "Microsoft",
        "MSFT",
        ethers.parseUnits("5", 2),
        ethers.parseUnits("380.25", 2)
      );
    });

    it("Should return correct active count", async function () {
      const count = await portfolioTracker.connect(user1).getActiveInvestmentCount();
      expect(count).to.equal(2);
    });

    it("Should return correct total invested", async function () {
      const total = await portfolioTracker.connect(user1).getTotalInvested();
      
      const expected = 
        ethers.parseUnits("10", 2) * ethers.parseUnits("175.50", 2) +
        ethers.parseUnits("5", 2) * ethers.parseUnits("380.25", 2);
      
      expect(total).to.equal(expected);
    });

    it("Should update count after removal", async function () {
      await portfolioTracker.connect(user1).removeInvestment(1);
      
      const count = await portfolioTracker.connect(user1).getActiveInvestmentCount();
      expect(count).to.equal(1);
    });
  });

  describe("Batch Operations", function () {
    beforeEach(async function () {
      await portfolioTracker.connect(user1).addInvestment(
        "Apple",
        "AAPL",
        ethers.parseUnits("10", 2),
        ethers.parseUnits("175", 2)
      );
      
      await portfolioTracker.connect(user1).addInvestment(
        "Microsoft",
        "MSFT",
        ethers.parseUnits("5", 2),
        ethers.parseUnits("380", 2)
      );
      
      await portfolioTracker.connect(user1).addInvestment(
        "Tesla",
        "TSLA",
        ethers.parseUnits("3", 2),
        ethers.parseUnits("245", 2)
      );
    });

    it("Should return all active investments", async function () {
      const all = await portfolioTracker.connect(user1).getAllMyInvestments();
      
      expect(all[0].length).to.equal(3);
      expect(all[1][0]).to.equal("Apple");
      expect(all[1][1]).to.equal("Microsoft");
      expect(all[1][2]).to.equal("Tesla");
    });

    it("Should exclude removed investments from batch", async function () {
      await portfolioTracker.connect(user1).removeInvestment(2);
      
      const all = await portfolioTracker.connect(user1).getAllMyInvestments();
      expect(all[0].length).to.equal(2);
    });
  });

  describe("Multi-user Isolation", function () {
    it("Should keep users' portfolios separate", async function () {
      await portfolioTracker.connect(user1).addInvestment(
        "Apple",
        "AAPL",
        ethers.parseUnits("10", 2),
        ethers.parseUnits("175", 2)
      );
      
      await portfolioTracker.connect(user2).addInvestment(
        "Tesla",
        "TSLA",
        ethers.parseUnits("5", 2),
        ethers.parseUnits("245", 2)
      );
      
      const user1Ids = await portfolioTracker.connect(user1).getMyInvestmentIds();
      const user2Ids = await portfolioTracker.connect(user2).getMyInvestmentIds();
      
      expect(user1Ids.length).to.equal(1);
      expect(user2Ids.length).to.equal(1);
      expect(user1Ids[0]).to.not.equal(user2Ids[0]);
    });
  });
});
