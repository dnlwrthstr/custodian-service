from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class CustodianInDB(BaseModel):
    """
    Custodian model for database operations.
    """
    id: Optional[str] = Field(None, alias="_id")
    name: str
    code: str
    description: Optional[str] = None
    contact_info: Dict[str, str] = {}
    api_credentials: Dict[str, str] = {}
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }

class PortfolioInDB(BaseModel):
    """
    Portfolio model for database operations.
    """
    id: Optional[str] = Field(None, alias="_id")
    custodian_id: str
    portfolio_id: str  # External ID from the custodian
    name: str
    description: Optional[str] = None
    currency: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }

class AccountInDB(BaseModel):
    """
    Account model for database operations.
    """
    id: Optional[str] = Field(None, alias="_id")
    custodian_id: str
    portfolio_id: str
    account_id: str  # External ID from the custodian
    name: str
    account_type: str
    currency: str
    balance: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }

class PositionInDB(BaseModel):
    """
    Position model for database operations.
    """
    id: Optional[str] = Field(None, alias="_id")
    custodian_id: str
    portfolio_id: str
    account_id: str
    position_id: str  # External ID from the custodian
    security_id: str
    security_type: str
    quantity: float
    market_value: float
    currency: str
    cost_basis: Optional[float] = None
    unrealized_pl: Optional[float] = None
    as_of_date: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }

class TransactionInDB(BaseModel):
    """
    Transaction model for database operations.
    """
    id: Optional[str] = Field(None, alias="_id")
    custodian_id: str
    portfolio_id: str
    account_id: str
    transaction_id: str  # External ID from the custodian
    transaction_type: str
    security_id: Optional[str] = None
    security_type: Optional[str] = None
    quantity: Optional[float] = None
    price: Optional[float] = None
    amount: float
    currency: str
    trade_date: datetime
    settlement_date: Optional[datetime] = None
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }