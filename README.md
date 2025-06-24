# Custodian Service API

A FastAPI service that implements custodian interfaces as specified in OpenWealth standards, using MongoDB as the database. This service is part of the Financial Advisory Project, a comprehensive financial advisory application built with a microservices architecture.

## Features

- RESTful API for custodian data management
- Implementation of OpenWealth standards for financial data
- MongoDB integration for data storage
- Asynchronous API with FastAPI
- Comprehensive data validation with Pydantic
- Event-driven architecture with Kafka integration
- Containerized deployment with Docker
- Kubernetes deployment support

## Requirements

### For Local Development
- Python 3.8+
- MongoDB

### For Containerized Deployment (Optional)
- Docker and Docker Compose
- Kubernetes (for production deployment)

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

## Environment Variables

The Custodian Service can be configured using the following environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `HOST` | Host to bind the service | `0.0.0.0` |
| `PORT` | Port to bind the service | `8000` |
| `DEBUG` | Enable debug mode | `False` |
| `MONGODB_URL` | MongoDB connection URL | `mongodb://localhost:27017` |
| `MONGODB_DB_NAME` | MongoDB database name | `custodian_service` |
| `SECRET_KEY` | Secret key for JWT tokens | Required |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT token expiration time in minutes | `30` |
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka bootstrap servers | `localhost:9092` |
| `KAFKA_TRANSACTION_TOPIC` | Kafka topic for transaction events | `custodian.transactions` |
| `KAFKA_CUSTODIAN_TOPIC` | Kafka topic for custodian events | `custodian.custodian` |
| `KAFKA_ENABLED` | Enable Kafka integration | `False` |

These variables can be set in the `.env` file for local development or as environment variables in Docker/Kubernetes deployments.

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

## Docker Containerization

The Custodian Service is containerized using Docker for easy deployment and scaling. The service includes:

- A `Dockerfile` for building the service container
- A service-specific `docker-compose.yml` for local development
- Integration with the main project's `docker-compose.yml` for running as part of the complete system

### Building and Running with Docker

To build and run the service using Docker:

```bash
# Build the Docker image
docker build -t custodian-service .

# Run the container
docker run -p 8000:8000 custodian-service
```

### Running with Docker Compose

For local development with MongoDB:

```bash
# Start the service with its dependencies
docker-compose up -d

# Stop the service
docker-compose down
```

To run as part of the complete Financial Advisory Project:

```bash
# From the project root directory
docker-compose up -d
```

## Kubernetes Deployment

The Custodian Service supports deployment to Kubernetes clusters. Kubernetes manifests are provided in the `k8s/custodian-service` directory:

- `configmap.yaml`: Configuration for the service
- `deployment.yaml`: Deployment specification
- `service.yaml`: Service definition for network access

### Deploying to Kubernetes

To deploy the service to a Kubernetes cluster:

```bash
# Apply the Kubernetes manifests
kubectl apply -f k8s/custodian-service/

# Check the deployment status
kubectl get deployments
kubectl get pods
kubectl get services
```

## Integration with Other Services

The Custodian Service is part of the Financial Advisory Project's microservices architecture and integrates with:

### MongoDB
- Used for storing custodian data, portfolios, accounts, positions, and transactions
- Configured via environment variables

### Kafka
- Publishes events to Kafka topics for event-driven communication
- Main topics:
  - `custodian.transactions`: Transaction events
  - `custodian.custodian`: Custodian events
- Consumed by other services like `load-custodian-service`

### Search Service
- Consumes data from the Custodian Service API
- Provides search capabilities across custodian data

### Frontend
- Connects to the Custodian Service API for data display and management
- Configured to access the API at the appropriate endpoint

## License

[MIT License](LICENSE)
