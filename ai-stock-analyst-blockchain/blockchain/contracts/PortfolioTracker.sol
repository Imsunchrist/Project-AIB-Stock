// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

contract PortfolioTracker {
    
    struct Investment {
        string company;
        string symbol;
        uint256 shares;
        uint256 purchasePrice;
        uint256 timestamp;
        address investor;
        bool active;
    }
    
    mapping(address => uint256[]) public investmentIds;
    mapping(uint256 => Investment) public investments;
    uint256 public investmentCounter;
    
    event InvestmentAdded(
        address indexed investor,
        uint256 indexed investmentId,
        string company,
        string symbol,
        uint256 shares,
        uint256 price,
        uint256 timestamp
    );
    
    event InvestmentRemoved(
        address indexed investor,
        uint256 indexed investmentId,
        uint256 timestamp
    );
    
    event PortfolioValueUpdated(
        address indexed investor,
        uint256 totalInvestments,
        uint256 timestamp
    );
    
    function addInvestment(
        string memory _company,
        string memory _symbol,
        uint256 _shares,
        uint256 _purchasePrice
    ) public returns (uint256) {
        require(bytes(_company).length > 0, "Company name required");
        require(bytes(_symbol).length > 0, "Symbol required");
        require(_shares > 0, "Shares must be positive");
        require(_purchasePrice > 0, "Price must be positive");
        
        investmentCounter++;
        
        investments[investmentCounter] = Investment({
            company: _company,
            symbol: _symbol,
            shares: _shares,
            purchasePrice: _purchasePrice,
            timestamp: block.timestamp,
            investor: msg.sender,
            active: true
        });
        
        investmentIds[msg.sender].push(investmentCounter);
        
        emit InvestmentAdded(
            msg.sender, 
            investmentCounter, 
            _company, 
            _symbol,
            _shares, 
            _purchasePrice,
            block.timestamp
        );
        
        return investmentCounter;
    }
    
    function removeInvestment(uint256 _investmentId) public {
        require(_investmentId > 0 && _investmentId <= investmentCounter, "Invalid investment ID");
        require(investments[_investmentId].investor == msg.sender, "Not your investment");
        require(investments[_investmentId].active, "Already removed");
        
        investments[_investmentId].active = false;
        
        emit InvestmentRemoved(msg.sender, _investmentId, block.timestamp);
    }
    
    function getInvestment(uint256 _investmentId) 
        public 
        view 
        returns (
            string memory company,
            string memory symbol,
            uint256 shares,
            uint256 purchasePrice,
            uint256 timestamp,
            bool active
        ) 
    {
        require(_investmentId > 0 && _investmentId <= investmentCounter, "Invalid ID");
        Investment memory inv = investments[_investmentId];
        require(inv.investor == msg.sender, "Not your investment");
        
        return (
            inv.company, 
            inv.symbol, 
            inv.shares, 
            inv.purchasePrice, 
            inv.timestamp, 
            inv.active
        );
    }
    
    function getMyInvestmentIds() public view returns (uint256[] memory) {
        return investmentIds[msg.sender];
    }
    
    function getActiveInvestmentCount() public view returns (uint256) {
        uint256 count = 0;
        uint256[] memory ids = investmentIds[msg.sender];
        
        for (uint256 i = 0; i < ids.length; i++) {
            if (investments[ids[i]].active) {
                count++;
            }
        }
        return count;
    }
    
    function getTotalInvested() public view returns (uint256) {
        uint256 total = 0;
        uint256[] memory ids = investmentIds[msg.sender];
        
        for (uint256 i = 0; i < ids.length; i++) {
            if (investments[ids[i]].active) {
                Investment memory inv = investments[ids[i]];
                total += inv.shares * inv.purchasePrice;
            }
        }
        return total;
    }
    
    function getAllMyInvestments() 
        public 
        view 
        returns (
            uint256[] memory ids,
            string[] memory companies,
            string[] memory symbols,
            uint256[] memory shares,
            uint256[] memory prices,
            uint256[] memory timestamps,
            bool[] memory activeStatuses
        ) 
    {
        uint256[] memory myIds = investmentIds[msg.sender];
        uint256 activeCount = getActiveInvestmentCount();
        
        ids = new uint256[](activeCount);
        companies = new string[](activeCount);
        symbols = new string[](activeCount);
        shares = new uint256[](activeCount);
        prices = new uint256[](activeCount);
        timestamps = new uint256[](activeCount);
        activeStatuses = new bool[](activeCount);
        
        uint256 index = 0;
        for (uint256 i = 0; i < myIds.length; i++) {
            Investment memory inv = investments[myIds[i]];
            if (inv.active) {
                ids[index] = myIds[i];
                companies[index] = inv.company;
                symbols[index] = inv.symbol;
                shares[index] = inv.shares;
                prices[index] = inv.purchasePrice;
                timestamps[index] = inv.timestamp;
                activeStatuses[index] = inv.active;
                index++;
            }
        }
        
        return (ids, companies, symbols, shares, prices, timestamps, activeStatuses);
    }
}
