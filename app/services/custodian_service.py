from datetime import datetime
from typing import Dict, List, Optional, Any
from bson import ObjectId
from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.custodian import (
    CustodianInDB,
    PortfolioInDB,
    AccountInDB,
    PositionInDB,
    TransactionInDB
)
from app.schemas.custodian import (
    CustodianCreate,
    CustodianUpdate,
    PortfolioCreate,
    PortfolioUpdate,
    AccountCreate,
    AccountUpdate,
    PositionCreate,
    PositionUpdate,
    TransactionCreate,
    TransactionUpdate
)

class CustodianService:
    """
    Service for custodian operations implementing OpenWealth standards.
    """
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.custodian_collection = db.custodians
        self.portfolio_collection = db.portfolios
        self.account_collection = db.accounts
        self.position_collection = db.positions
        self.transaction_collection = db.transactions

    # Helper methods
    def _convert_object_id(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """Convert MongoDB ObjectId to string."""
        if obj and "_id" in obj:
            obj["_id"] = str(obj["_id"])
        return obj

    # Custodian methods
    async def create_custodian(self, custodian: CustodianCreate) -> CustodianInDB:
        """Create a new custodian."""
        custodian_dict = custodian.model_dump()
        custodian_dict["created_at"] = datetime.utcnow()
        custodian_dict["updated_at"] = custodian_dict["created_at"]
        
        result = await self.custodian_collection.insert_one(custodian_dict)
        
        created_custodian = await self.custodian_collection.find_one({"_id": result.inserted_id})
        created_custodian = self._convert_object_id(created_custodian)
        
        return CustodianInDB(**created_custodian)

    async def get_custodians(self, skip: int = 0, limit: int = 100) -> List[CustodianInDB]:
        """Get all custodians."""
        custodians = []
        cursor = self.custodian_collection.find().skip(skip).limit(limit)
        
        async for custodian in cursor:
            custodian = self._convert_object_id(custodian)
            custodians.append(CustodianInDB(**custodian))
            
        return custodians

    async def get_custodian(self, custodian_id: str) -> Optional[CustodianInDB]:
        """Get a custodian by ID."""
        try:
            custodian = await self.custodian_collection.find_one({"_id": ObjectId(custodian_id)})
            if custodian:
                custodian = self._convert_object_id(custodian)
                return CustodianInDB(**custodian)
        except Exception:
            return None
        
        return None

    async def update_custodian(self, custodian_id: str, custodian_update: CustodianUpdate) -> Optional[CustodianInDB]:
        """Update a custodian."""
        try:
            update_data = custodian_update.model_dump(exclude_unset=True)
            if update_data:
                update_data["updated_at"] = datetime.utcnow()
                
                await self.custodian_collection.update_one(
                    {"_id": ObjectId(custodian_id)},
                    {"$set": update_data}
                )
                
                return await self.get_custodian(custodian_id)
        except Exception:
            return None
        
        return None

    async def delete_custodian(self, custodian_id: str) -> bool:
        """Delete a custodian."""
        try:
            result = await self.custodian_collection.delete_one({"_id": ObjectId(custodian_id)})
            return result.deleted_count > 0
        except Exception:
            return False

    # Portfolio methods
    async def get_portfolios(self, custodian_id: str) -> List[PortfolioInDB]:
        """Get all portfolios for a custodian."""
        portfolios = []
        cursor = self.portfolio_collection.find({"custodian_id": custodian_id})
        
        async for portfolio in cursor:
            portfolio = self._convert_object_id(portfolio)
            portfolios.append(PortfolioInDB(**portfolio))
            
        return portfolios

    async def create_portfolio(self, portfolio: PortfolioCreate) -> PortfolioInDB:
        """Create a new portfolio."""
        portfolio_dict = portfolio.model_dump()
        portfolio_dict["created_at"] = datetime.utcnow()
        portfolio_dict["updated_at"] = portfolio_dict["created_at"]
        
        result = await self.portfolio_collection.insert_one(portfolio_dict)
        
        created_portfolio = await self.portfolio_collection.find_one({"_id": result.inserted_id})
        created_portfolio = self._convert_object_id(created_portfolio)
        
        return PortfolioInDB(**created_portfolio)

    # Account methods
    async def get_accounts(self, custodian_id: str, portfolio_id: Optional[str] = None) -> List[AccountInDB]:
        """Get all accounts for a custodian, optionally filtered by portfolio."""
        query = {"custodian_id": custodian_id}
        if portfolio_id:
            query["portfolio_id"] = portfolio_id
            
        accounts = []
        cursor = self.account_collection.find(query)
        
        async for account in cursor:
            account = self._convert_object_id(account)
            accounts.append(AccountInDB(**account))
            
        return accounts

    async def create_account(self, account: AccountCreate) -> AccountInDB:
        """Create a new account."""
        account_dict = account.model_dump()
        account_dict["created_at"] = datetime.utcnow()
        account_dict["updated_at"] = account_dict["created_at"]
        
        result = await self.account_collection.insert_one(account_dict)
        
        created_account = await self.account_collection.find_one({"_id": result.inserted_id})
        created_account = self._convert_object_id(created_account)
        
        return AccountInDB(**created_account)

    # Position methods
    async def get_positions(
        self, 
        custodian_id: str, 
        account_id: Optional[str] = None, 
        portfolio_id: Optional[str] = None
    ) -> List[PositionInDB]:
        """Get all positions for a custodian, optionally filtered by account or portfolio."""
        query = {"custodian_id": custodian_id}
        if account_id:
            query["account_id"] = account_id
        if portfolio_id:
            query["portfolio_id"] = portfolio_id
            
        positions = []
        cursor = self.position_collection.find(query)
        
        async for position in cursor:
            position = self._convert_object_id(position)
            positions.append(PositionInDB(**position))
            
        return positions

    async def create_position(self, position: PositionCreate) -> PositionInDB:
        """Create a new position."""
        position_dict = position.model_dump()
        position_dict["created_at"] = datetime.utcnow()
        position_dict["updated_at"] = position_dict["created_at"]
        
        result = await self.position_collection.insert_one(position_dict)
        
        created_position = await self.position_collection.find_one({"_id": result.inserted_id})
        created_position = self._convert_object_id(created_position)
        
        return PositionInDB(**created_position)

    # Transaction methods
    async def get_transactions(
        self, 
        custodian_id: str, 
        account_id: Optional[str] = None, 
        portfolio_id: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
    ) -> List[TransactionInDB]:
        """Get all transactions for a custodian, optionally filtered by account, portfolio, or date range."""
        query = {"custodian_id": custodian_id}
        if account_id:
            query["account_id"] = account_id
        if portfolio_id:
            query["portfolio_id"] = portfolio_id
            
        # Add date range filter if provided
        if from_date or to_date:
            query["trade_date"] = {}
            if from_date:
                query["trade_date"]["$gte"] = datetime.fromisoformat(from_date)
            if to_date:
                query["trade_date"]["$lte"] = datetime.fromisoformat(to_date)
            
        transactions = []
        cursor = self.transaction_collection.find(query)
        
        async for transaction in cursor:
            transaction = self._convert_object_id(transaction)
            transactions.append(TransactionInDB(**transaction))
            
        return transactions

    async def create_transaction(self, transaction: TransactionCreate) -> TransactionInDB:
        """Create a new transaction."""
        transaction_dict = transaction.model_dump()
        transaction_dict["created_at"] = datetime.utcnow()
        transaction_dict["updated_at"] = transaction_dict["created_at"]
        
        result = await self.transaction_collection.insert_one(transaction_dict)
        
        created_transaction = await self.transaction_collection.find_one({"_id": result.inserted_id})
        created_transaction = self._convert_object_id(created_transaction)
        
        return TransactionInDB(**created_transaction)