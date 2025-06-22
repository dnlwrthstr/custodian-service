from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional

from app.db.mongodb import get_database
from app.models.custodian import CustodianInDB
from app.schemas.custodian import (
    CustodianCreate,
    CustodianResponse,
    CustodianUpdate,
    PortfolioResponse,
    AccountResponse,
    PositionResponse,
    TransactionResponse
)
from app.services.custodian_service import CustodianService

router = APIRouter()

@router.post("/", response_model=CustodianResponse, status_code=status.HTTP_201_CREATED)
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
    """
    custodian_service = CustodianService(db)
    return await custodian_service.create_custodian(custodian)

@router.get("/", response_model=List[CustodianResponse])
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
    """
    custodian_service = CustodianService(db)
    return await custodian_service.get_custodians(skip=skip, limit=limit)

@router.get("/{custodian_id}", response_model=CustodianResponse)
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
    """
    custodian_service = CustodianService(db)
    return await custodian_service.get_portfolios(custodian_id)

@router.post("/{custodian_id}/portfolios", response_model=PortfolioResponse, status_code=status.HTTP_201_CREATED)
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
    """
    # Ensure the portfolio is associated with the specified custodian
    portfolio_data = portfolio.dict()
    portfolio_data["custodian_id"] = custodian_id

    custodian_service = CustodianService(db)
    return await custodian_service.create_portfolio(PortfolioCreate(**portfolio_data))

# OpenWealth standard endpoints for accounts
@router.get("/{custodian_id}/accounts", response_model=List[AccountResponse])
async def get_accounts(
    custodian_id: str,
    portfolio_id: Optional[str] = None,
    db = Depends(get_database)
):
    """
    Retrieve all accounts for a custodian, optionally filtered by portfolio.
    """
    custodian_service = CustodianService(db)
    return await custodian_service.get_accounts(custodian_id, portfolio_id)

@router.post("/{custodian_id}/accounts", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
async def create_account(
    custodian_id: str,
    account: AccountCreate,
    db = Depends(get_database)
):
    """
    Create a new account for a custodian.
    """
    # Ensure the account is associated with the specified custodian
    account_data = account.dict()
    account_data["custodian_id"] = custodian_id

    custodian_service = CustodianService(db)
    return await custodian_service.create_account(AccountCreate(**account_data))

# OpenWealth standard endpoints for positions
@router.get("/{custodian_id}/positions", response_model=List[PositionResponse])
async def get_positions(
    custodian_id: str,
    account_id: Optional[str] = None,
    portfolio_id: Optional[str] = None,
    db = Depends(get_database)
):
    """
    Retrieve all positions for a custodian, optionally filtered by account or portfolio.
    """
    custodian_service = CustodianService(db)
    return await custodian_service.get_positions(custodian_id, account_id, portfolio_id)

@router.post("/{custodian_id}/positions", response_model=PositionResponse, status_code=status.HTTP_201_CREATED)
async def create_position(
    custodian_id: str,
    position: PositionCreate,
    db = Depends(get_database)
):
    """
    Create a new position for a custodian.
    """
    # Ensure the position is associated with the specified custodian
    position_data = position.dict()
    position_data["custodian_id"] = custodian_id

    custodian_service = CustodianService(db)
    return await custodian_service.create_position(PositionCreate(**position_data))

# OpenWealth standard endpoints for transactions
@router.get("/{custodian_id}/transactions", response_model=List[TransactionResponse])
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
    """
    custodian_service = CustodianService(db)
    return await custodian_service.get_transactions(
        custodian_id, account_id, portfolio_id, from_date, to_date
    )

@router.post("/{custodian_id}/transactions", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    custodian_id: str,
    transaction: TransactionCreate,
    db = Depends(get_database)
):
    """
    Create a new transaction for a custodian.
    """
    # Ensure the transaction is associated with the specified custodian
    transaction_data = transaction.dict()
    transaction_data["custodian_id"] = custodian_id

    custodian_service = CustodianService(db)
    return await custodian_service.create_transaction(TransactionCreate(**transaction_data))
