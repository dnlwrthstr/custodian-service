# Custodian Service API

A FastAPI service that implements custodian interfaces as specified in OpenWealth standards, using MongoDB as the database.

## Features

- RESTful API for custodian data management
- Implementation of OpenWealth standards for financial data
- MongoDB integration for data storage
- Asynchronous API with FastAPI
- Comprehensive data validation with Pydantic

## Requirements

- Python 3.8+
- MongoDB

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd custodian-service
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
   - Copy the `.env.example` file to `.env` (if not already present)
   - Update the MongoDB connection URL and other settings as needed

## Running the Application

Start the application with:

```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000.

## API Documentation

Once the application is running, you can access the interactive API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

The API documentation provides detailed information about all endpoints, including:
- Request parameters and their types
- Request body schemas
- Response schemas
- Error responses

### Using API Documentation in a Frontend Project

For detailed instructions on how to use the API documentation in a frontend project, see [API_DOCUMENTATION.md](API_DOCUMENTATION.md). This guide covers:

- Linking to the API documentation
- Embedding the documentation in your frontend
- Generating client code from the OpenAPI specification
- Using Swagger UI directly in your frontend application

## API Endpoints

### Custodians

- `POST /api/v1/custodian/`: Create a new custodian
- `GET /api/v1/custodian/`: List all custodians
- `GET /api/v1/custodian/{custodian_id}`: Get a specific custodian
- `PUT /api/v1/custodian/{custodian_id}`: Update a custodian
- `DELETE /api/v1/custodian/{custodian_id}`: Delete a custodian

### Portfolios

- `GET /api/v1/custodian/{custodian_id}/portfolios`: List all portfolios for a custodian
- `POST /api/v1/custodian/{custodian_id}/portfolios`: Create a new portfolio for a custodian

### Accounts

- `GET /api/v1/custodian/{custodian_id}/accounts`: List all accounts for a custodian
- `POST /api/v1/custodian/{custodian_id}/accounts`: Create a new account for a custodian

### Positions

- `GET /api/v1/custodian/{custodian_id}/positions`: List all positions for a custodian
- `POST /api/v1/custodian/{custodian_id}/positions`: Create a new position for a custodian

### Transactions

- `GET /api/v1/custodian/{custodian_id}/transactions`: List all transactions for a custodian
- `POST /api/v1/custodian/{custodian_id}/transactions`: Create a new transaction for a custodian

## OpenWealth Standards Implementation

This service implements the OpenWealth standards for custodian interfaces, providing a standardized way to access financial data from different custodians. The implementation includes:

- Standard data models for custodians, portfolios, accounts, positions, and transactions
- Consistent API endpoints for accessing financial data
- Filtering options for retrieving specific data

## Development

### Project Structure

```
custodian-service/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   └── endpoints/
│   │   │       └── custodian.py
│   │   └── routes.py
│   ├── core/
│   │   └── config.py
│   ├── db/
│   │   └── mongodb.py
│   ├── models/
│   │   └── custodian.py
│   ├── schemas/
│   │   └── custodian.py
│   └── services/
│       └── custodian_service.py
├── data/
│   ├── custodians.json
│   ├── portfolios.json
│   ├── accounts.json
│   ├── positions.json
│   ├── transactions.json
│   └── seed_database.py
├── .env
├── API_DOCUMENTATION.md
├── main.py
├── requirements.txt
└── README.md
```

### Database Seeding

The project includes a data folder with test data and a script to seed the database:

1. **Test Data Files**:
   - `custodians.json`: Sample custodian data
   - `portfolios.json`: Sample portfolio data
   - `accounts.json`: Sample account data
   - `positions.json`: Sample position data
   - `transactions.json`: Sample transaction data

2. **Seeding Script**:
   - `seed_database.py`: Python script to populate the database with test data

To seed the database with test data:

```bash
# Make sure the MongoDB container is running
docker-compose up -d mongo

# Run the seeding script
python data/seed_database.py
```

Alternatively, you can run the seeding script inside the Docker container:

```bash
docker-compose exec app python /app/data/seed_database.py
```

The seeding script will:
- Clear existing data from all collections
- Insert test data from the JSON files
- Maintain relationships between collections
- Convert date strings to proper datetime objects

### Testing

To run tests:

```bash
pytest
```

## License

[MIT License](LICENSE)
