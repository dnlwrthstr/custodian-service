#!/usr/bin/env python3
"""
Script to seed the MongoDB database with test data.
"""
import json
import asyncio
import os
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

# MongoDB connection settings
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "custodian_service")

# Path to data files
DATA_DIR = os.path.dirname(os.path.abspath(__file__))

async def load_json_data(file_path):
    """Load data from a JSON file."""
    with open(file_path, 'r') as file:
        return json.load(file)

async def seed_database():
    """Seed the database with test data."""
    # Connect to MongoDB
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[MONGODB_DB_NAME]
    
    # Clear existing data
    await db.custodians.delete_many({})
    await db.portfolios.delete_many({})
    await db.accounts.delete_many({})
    await db.positions.delete_many({})
    await db.transactions.delete_many({})
    
    print("Cleared existing data from database.")
    
    # Load data from JSON files
    custodians_data = await load_json_data(os.path.join(DATA_DIR, 'custodians.json'))
    portfolios_data = await load_json_data(os.path.join(DATA_DIR, 'portfolios.json'))
    accounts_data = await load_json_data(os.path.join(DATA_DIR, 'accounts.json'))
    positions_data = await load_json_data(os.path.join(DATA_DIR, 'positions.json'))
    transactions_data = await load_json_data(os.path.join(DATA_DIR, 'transactions.json'))
    
    # Insert custodians and store their IDs
    custodian_id_map = {}  # Maps placeholder IDs to actual MongoDB ObjectIds
    
    for i, custodian in enumerate(custodians_data):
        placeholder_id = f"CUSTODIAN_ID_{i+1}"
        custodian['created_at'] = datetime.utcnow()
        custodian['updated_at'] = custodian['created_at']
        
        result = await db.custodians.insert_one(custodian)
        custodian_id_map[placeholder_id] = str(result.inserted_id)
    
    print(f"Inserted {len(custodians_data)} custodians.")
    
    # Insert portfolios and store their IDs
    portfolio_id_map = {}  # Maps portfolio_id to actual MongoDB ObjectIds
    
    for portfolio in portfolios_data:
        # Replace placeholder custodian_id with actual MongoDB ObjectId
        if portfolio['custodian_id'] in custodian_id_map:
            portfolio['custodian_id'] = custodian_id_map[portfolio['custodian_id']]
        
        portfolio['created_at'] = datetime.utcnow()
        portfolio['updated_at'] = portfolio['created_at']
        
        result = await db.portfolios.insert_one(portfolio)
        portfolio_id_map[portfolio['portfolio_id']] = str(result.inserted_id)
    
    print(f"Inserted {len(portfolios_data)} portfolios.")
    
    # Insert accounts
    account_id_map = {}  # Maps account_id to actual MongoDB ObjectIds
    
    for account in accounts_data:
        # Replace placeholder IDs with actual MongoDB ObjectIds
        if account['custodian_id'] in custodian_id_map:
            account['custodian_id'] = custodian_id_map[account['custodian_id']]
        
        if account['portfolio_id'] in portfolio_id_map:
            account['portfolio_id'] = portfolio_id_map[account['portfolio_id']]
        
        account['created_at'] = datetime.utcnow()
        account['updated_at'] = account['created_at']
        
        result = await db.accounts.insert_one(account)
        account_id_map[account['account_id']] = str(result.inserted_id)
    
    print(f"Inserted {len(accounts_data)} accounts.")
    
    # Insert positions
    for position in positions_data:
        # Replace placeholder IDs with actual MongoDB ObjectIds
        if position['custodian_id'] in custodian_id_map:
            position['custodian_id'] = custodian_id_map[position['custodian_id']]
        
        if position['portfolio_id'] in portfolio_id_map:
            position['portfolio_id'] = portfolio_id_map[position['portfolio_id']]
        
        if position['account_id'] in account_id_map:
            position['account_id'] = account_id_map[position['account_id']]
        
        # Convert string dates to datetime objects
        if isinstance(position['as_of_date'], str):
            position['as_of_date'] = datetime.fromisoformat(position['as_of_date'].replace('Z', '+00:00'))
        
        position['created_at'] = datetime.utcnow()
        position['updated_at'] = position['created_at']
        
        await db.positions.insert_one(position)
    
    print(f"Inserted {len(positions_data)} positions.")
    
    # Insert transactions
    for transaction in transactions_data:
        # Replace placeholder IDs with actual MongoDB ObjectIds
        if transaction['custodian_id'] in custodian_id_map:
            transaction['custodian_id'] = custodian_id_map[transaction['custodian_id']]
        
        if transaction['portfolio_id'] in portfolio_id_map:
            transaction['portfolio_id'] = portfolio_id_map[transaction['portfolio_id']]
        
        if transaction['account_id'] in account_id_map:
            transaction['account_id'] = account_id_map[transaction['account_id']]
        
        # Convert string dates to datetime objects
        if isinstance(transaction['trade_date'], str):
            transaction['trade_date'] = datetime.fromisoformat(transaction['trade_date'].replace('Z', '+00:00'))
        
        if 'settlement_date' in transaction and isinstance(transaction['settlement_date'], str):
            transaction['settlement_date'] = datetime.fromisoformat(transaction['settlement_date'].replace('Z', '+00:00'))
        
        transaction['created_at'] = datetime.utcnow()
        transaction['updated_at'] = transaction['created_at']
        
        await db.transactions.insert_one(transaction)
    
    print(f"Inserted {len(transactions_data)} transactions.")
    
    print("Database seeding completed successfully!")

if __name__ == "__main__":
    asyncio.run(seed_database())