from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional, TypeVar, Callable, Awaitable, Any
import functools

from app.db.mongodb import get_database
from app.models.custodian import CustodianInDB
from app.schemas.custodian import (
    CustodianCreate,
    CustodianResponse,
    CustodianUpdate,
    PortfolioCreate,
    PortfolioResponse,
    AccountCreate,
    AccountResponse,
    PositionCreate,
    PositionResponse,
    TransactionCreate,
    TransactionResponse
)
from app.services.custodian_service import CustodianService

T = TypeVar('T')

def handle_db_errors(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
    """
    Decorator to handle database connection errors in endpoint functions.
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except (ValueError, ConnectionError) as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )
    return wrapper

router = APIRouter()

@router.post("/", response_model=CustodianResponse, status_code=status.HTTP_201_CREATED)
@handle_db_errors
async def create_custodian(
    custodian: CustodianCreate,
    db = Depends(get_database)
):
    """
    Create a new custodian.

    Parameters:
    - **custodian**: Required. The custodian data including name, code, description, contact_info, and api_credentials.

    Returns:
    - A custodian object with id, created_at, and updated_at fields.

    Raises:
    - 500: If there's a database connection error.
    """
    custodian_service = CustodianService(db)
    return await custodian_service.create_custodian(custodian)

@router.get("/", response_model=List[CustodianResponse])
@handle_db_errors
async def get_custodians(
    skip: int = 0,
    limit: int = 100,
    db = Depends(get_database)
):
    """
    Retrieve all custodians.

    Parameters:
    - **skip**: Optional. Number of custodians to skip (for pagination). Default: 0.
    - **limit**: Optional. Maximum number of custodians to return. Default: 100.

    Returns:
    - A list of custodian objects.

    Raises:
    - 500: If there's a database connection error.
    """
    custodian_service = CustodianService(db)
    return await custodian_service.get_custodians(skip=skip, limit=limit)

@router.get("/{custodian_id}", response_model=CustodianResponse)
@handle_db_errors
async def get_custodian(
    custodian_id: str,
    db = Depends(get_database)
):
    """
    Retrieve a specific custodian by ID.

    Parameters:
    - **custodian_id**: Required. The ID of the custodian to retrieve.

    Returns:
    - A custodian object.

    Raises:
    - 404: If the custodian with the specified ID is not found.
    - 500: If there's a database connection error.
    """
    custodian_service = CustodianService(db)
    custodian = await custodian_service.get_custodian(custodian_id)
    if not custodian:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Custodian with ID {custodian_id} not found"
        )
    return custodian

@router.put("/{custodian_id}", response_model=CustodianResponse)
@handle_db_errors
async def update_custodian(
    custodian_id: str,
    custodian_update: CustodianUpdate,
    db = Depends(get_database)
):
    """
    Update a custodian.

    Parameters:
    - **custodian_id**: Required. The ID of the custodian to update.
    - **custodian_update**: Required. The updated custodian data. Only the fields to be updated need to be included.

    Returns:
    - The updated custodian object.

    Raises:
    - 404: If the custodian with the specified ID is not found.
    - 500: If there's a database connection error.
    """
    custodian_service = CustodianService(db)
    custodian = await custodian_service.update_custodian(custodian_id, custodian_update)
    if not custodian:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Custodian with ID {custodian_id} not found"
        )
    return custodian

@router.delete("/{custodian_id}", status_code=status.HTTP_204_NO_CONTENT)
@handle_db_errors
async def delete_custodian(
    custodian_id: str,
    db = Depends(get_database)
):
    """
    Delete a custodian.

    Parameters:
    - **custodian_id**: Required. The ID of the custodian to delete.

    Returns:
    - No content (204) if successful.

    Raises:
    - 404: If the custodian with the specified ID is not found.
    - 500: If there's a database connection error.
    """
    custodian_service = CustodianService(db)
    deleted = await custodian_service.delete_custodian(custodian_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Custodian with ID {custodian_id} not found"
        )

# OpenWealth standard endpoints for portfolios
@router.get("/{custodian_id}/portfolios", response_model=List[PortfolioResponse])
@handle_db_errors
async def get_portfolios(
    custodian_id: str,
    db = Depends(get_database)
):
    """
    Retrieve all portfolios for a custodian.

    Parameters:
    - **custodian_id**: Required. The ID of the custodian whose portfolios to retrieve.

    Returns:
    - A list of portfolio objects associated with the specified custodian.

    Raises:
    - 500: If there's a database connection error.
    """
    custodian_service = CustodianService(db)
    return await custodian_service.get_portfolios(custodian_id)

@router.post("/{custodian_id}/portfolios", response_model=PortfolioResponse, status_code=status.HTTP_201_CREATED)
@handle_db_errors
async def create_portfolio(
    custodian_id: str,
    portfolio: PortfolioCreate,
    db = Depends(get_database)
):
    """
    Create a new portfolio for a custodian.

    Parameters:
    - **custodian_id**: Required. The ID of the custodian to associate with the portfolio.
    - **portfolio**: Required. The portfolio data including portfolio_id, name, description, and currency.

    Returns:
    - The created portfolio object with id, custodian_id, created_at, and updated_at fields.

    Raises:
    - 500: If there's a database connection error.
    """
    # Ensure the portfolio is associated with the specified custodian
    portfolio_data = portfolio.dict()
    portfolio_data["custodian_id"] = custodian_id

    custodian_service = CustodianService(db)
    return await custodian_service.create_portfolio(PortfolioCreate(**portfolio_data))

# OpenWealth standard endpoints for accounts
@router.get("/{custodian_id}/accounts", response_model=List[AccountResponse])
@handle_db_errors
async def get_accounts(
    custodian_id: str,
    portfolio_id: Optional[str] = None,
    db = Depends(get_database)
):
    """
    Retrieve all accounts for a custodian, optionally filtered by portfolio.

    Parameters:
    - **custodian_id**: Required. The ID of the custodian whose accounts to retrieve.
    - **portfolio_id**: Optional. The ID of the portfolio to filter accounts by.

    Returns:
    - A list of account objects associated with the specified custodian and optionally filtered by portfolio.

    Raises:
    - 500: If there's a database connection error.
    """
    custodian_service = CustodianService(db)
    return await custodian_service.get_accounts(custodian_id, portfolio_id)

@router.post("/{custodian_id}/accounts", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
@handle_db_errors
async def create_account(
    custodian_id: str,
    account: AccountCreate,
    db = Depends(get_database)
):
    """
    Create a new account for a custodian.

    Parameters:
    - **custodian_id**: Required. The ID of the custodian to associate with the account.
    - **account**: Required. The account data including account_id, portfolio_id, name, description, and currency.

    Returns:
    - The created account object with id, custodian_id, created_at, and updated_at fields.

    Raises:
    - 500: If there's a database connection error.
    """
    # Ensure the account is associated with the specified custodian
    account_data = account.dict()
    account_data["custodian_id"] = custodian_id

    custodian_service = CustodianService(db)
    return await custodian_service.create_account(AccountCreate(**account_data))

# OpenWealth standard endpoints for positions
@router.get("/{custodian_id}/positions", response_model=List[PositionResponse])
@handle_db_errors
async def get_positions(
    custodian_id: str,
    account_id: Optional[str] = None,
    portfolio_id: Optional[str] = None,
    db = Depends(get_database)
):
    """
    Retrieve all positions for a custodian, optionally filtered by account or portfolio.

    Parameters:
    - **custodian_id**: Required. The ID of the custodian whose positions to retrieve.
    - **account_id**: Optional. The ID of the account to filter positions by.
    - **portfolio_id**: Optional. The ID of the portfolio to filter positions by.

    Returns:
    - A list of position objects associated with the specified custodian and optionally filtered by account or portfolio.

    Raises:
    - 500: If there's a database connection error.
    """
    custodian_service = CustodianService(db)
    return await custodian_service.get_positions(custodian_id, account_id, portfolio_id)

@router.post("/{custodian_id}/positions", response_model=PositionResponse, status_code=status.HTTP_201_CREATED)
@handle_db_errors
async def create_position(
    custodian_id: str,
    position: PositionCreate,
    db = Depends(get_database)
):
    """
    Create a new position for a custodian.

    Parameters:
    - **custodian_id**: Required. The ID of the custodian to associate with the position.
    - **position**: Required. The position data including position_id, account_id, portfolio_id, instrument, quantity, and value.

    Returns:
    - The created position object with id, custodian_id, created_at, and updated_at fields.

    Raises:
    - 500: If there's a database connection error.
    """
    # Ensure the position is associated with the specified custodian
    position_data = position.dict()
    position_data["custodian_id"] = custodian_id

    custodian_service = CustodianService(db)
    return await custodian_service.create_position(PositionCreate(**position_data))

# OpenWealth standard endpoints for transactions
@router.get("/{custodian_id}/transactions", response_model=List[TransactionResponse])
@handle_db_errors
async def get_transactions(
    custodian_id: str,
    account_id: Optional[str] = None,
    portfolio_id: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    db = Depends(get_database)
):
    """
    Retrieve all transactions for a custodian, optionally filtered by account, portfolio, or date range.

    Parameters:
    - **custodian_id**: Required. The ID of the custodian whose transactions to retrieve.
    - **account_id**: Optional. The ID of the account to filter transactions by.
    - **portfolio_id**: Optional. The ID of the portfolio to filter transactions by.
    - **from_date**: Optional. The start date (inclusive) to filter transactions by (ISO format).
    - **to_date**: Optional. The end date (inclusive) to filter transactions by (ISO format).

    Returns:
    - A list of transaction objects associated with the specified custodian and optionally filtered by account, portfolio, or date range.

    Raises:
    - 500: If there's a database connection error.
    """
    custodian_service = CustodianService(db)
    return await custodian_service.get_transactions(
        custodian_id, account_id, portfolio_id, from_date, to_date
    )

@router.post("/{custodian_id}/transactions", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
@handle_db_errors
async def create_transaction(
    custodian_id: str,
    transaction: TransactionCreate,
    db = Depends(get_database)
):
    """
    Create a new transaction for a custodian.

    Parameters:
    - **custodian_id**: Required. The ID of the custodian to associate with the transaction.
    - **transaction**: Required. The transaction data including transaction_id, account_id, portfolio_id, instrument, quantity, price, and trade_date.

    Returns:
    - The created transaction object with id, custodian_id, created_at, and updated_at fields.

    Raises:
    - 500: If there's a database connection error.
    """
    # Ensure the transaction is associated with the specified custodian
    transaction_data = transaction.dict()
    transaction_data["custodian_id"] = custodian_id

    custodian_service = CustodianService(db)
    return await custodian_service.create_transaction(TransactionCreate(**transaction_data))
