from fastapi import APIRouter

from app.api.v1.endpoints import custodian

# Create the main API router
router = APIRouter()

# Include routers from different API versions
router.include_router(custodian.router, prefix="/v1/custodian", tags=["custodian"])