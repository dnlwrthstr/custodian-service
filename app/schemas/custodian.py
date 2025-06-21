from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

# Custodian schemas
class CustodianBase(BaseModel):
    """Base schema for custodian data."""
    name: str
    code: str
    description: Optional[str] = None
    contact_info: Dict[str, str] = {}

class CustodianCreate(CustodianBase):
    """Schema for creating a custodian."""
    api_credentials: Dict[str, str] = {}

class CustodianUpdate(BaseModel):
    """Schema for updating a custodian."""
    name: Optional[str] = None
    description: Optional[str] = None
    contact_info: Optional[Dict[str, str]] = None
    api_credentials: Optional[Dict[str, str]] = None

class CustodianResponse(CustodianBase):
    """Schema for custodian response."""
    id: str
    api_credentials: Dict[str, str] = {}
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Portfolio schemas
class PortfolioBase(BaseModel):
    """Base schema for portfolio data."""
    portfolio_id: str
    name: str
    description: Optional[str] = None
    currency: str

class PortfolioCreate(PortfolioBase):
    """Schema for creating a portfolio."""
    custodian_id: str

class PortfolioUpdate(BaseModel):
    """Schema for updating a portfolio."""
    name: Optional[str] = None
    description: Optional[str] = None
    currency: Optional[str] = None

class PortfolioResponse(PortfolioBase):
    """Schema for portfolio response."""
    id: str
    custodian_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Account schemas
class AccountBase(BaseModel):
    """Base schema for account data."""
    account_id: str
    name: str
    account_type: str
    currency: str
    balance: float = 0.0

class AccountCreate(AccountBase):
    """Schema for creating an account."""
    custodian_id: str
    portfolio_id: str

class AccountUpdate(BaseModel):
    """Schema for updating an account."""
    name: Optional[str] = None
    account_type: Optional[str] = None
    currency: Optional[str] = None
    balance: Optional[float] = None

class AccountResponse(AccountBase):
    """Schema for account response."""
    id: str
    custodian_id: str
    portfolio_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Position schemas
class PositionBase(BaseModel):
    """Base schema for position data."""
    position_id: str
    security_id: str
    security_type: str
    quantity: float
    market_value: float
    currency: str
    cost_basis: Optional[float] = None
    unrealized_pl: Optional[float] = None
    as_of_date: datetime

class PositionCreate(PositionBase):
    """Schema for creating a position."""
    custodian_id: str
    portfolio_id: str
    account_id: str

class PositionUpdate(BaseModel):
    """Schema for updating a position."""
    quantity: Optional[float] = None
    market_value: Optional[float] = None
    cost_basis: Optional[float] = None
    unrealized_pl: Optional[float] = None
    as_of_date: Optional[datetime] = None

class PositionResponse(PositionBase):
    """Schema for position response."""
    id: str
    custodian_id: str
    portfolio_id: str
    account_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Transaction schemas
class TransactionBase(BaseModel):
    """Base schema for transaction data."""
    transaction_id: str
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

class TransactionCreate(TransactionBase):
    """Schema for creating a transaction."""
    custodian_id: str
    portfolio_id: str
    account_id: str

class TransactionUpdate(BaseModel):
    """Schema for updating a transaction."""
    amount: Optional[float] = None
    settlement_date: Optional[datetime] = None
    description: Optional[str] = None

class TransactionResponse(TransactionBase):
    """Schema for transaction response."""
    id: str
    custodian_id: str
    portfolio_id: str
    account_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True