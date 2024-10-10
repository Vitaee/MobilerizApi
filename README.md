## Unified Vendor Data Backend
A FastAPI backend for a Flutter mobile app that provides customers with an up-to-date and unified product catalog sourced from multiple vendors. The backend retrieves product information—such as name, description, price, and photos—from various vendor APIs and unifies this data. The architecture is designed for fast data retrieval and processing, ensuring a seamless user experience on mobile devices.

## Table of Contents
Features
Architecture Overview
Project Structure
Prerequisites
Installation
Configuration
Running the Application
Kafka and Flink Integration
Data Synchronization
Testing
Notes
License
Features

- Unified Product Catalog: Combines product data from multiple vendors into a single catalog.
- Fast Data Retrieval: Uses SQLite for quick local storage and retrieval.
- Near Real-Time Updates: Integrates Kafka and Flink for real-time data processing.
- Scalable Architecture: Built with Hexagonal Architecture principles for scalability and maintainability.
- Data Synchronization: Synchronizes data between SQLite and PostgreSQL for long-term storage and analytics.

## Architecture Overview

### Components
Mobile App (Flutter): Client application that users interact with to request product data.
FastAPI Backend: Processes data requests and communicates with other system components.
Kafka: Messaging system for communication between the backend and Flink.
Flink: Stream processing framework responsible for data transformation and external API calls.
SQLite: Quick local data storage for active products.
PostgreSQL: Relational database used for long-term storage and analytics.
SymmetricDS: Used for data synchronization between SQLite and PostgreSQL.

### Data Flow

User Request: The user requests product data from the mobile app.
Local Check: FastAPI checks SQLite for the requested information.
Message to Kafka: If the data is unavailable in SQLite, FastAPI sends a message to Kafka.
Flink Processing: Flink processes the message from Kafka, retrieves the data from the external API, and stores it in SQLite.
Data Synchronization: The data in SQLite is synchronized with PostgreSQL for long-term storage using SymmetricDS.



## Project Structure
```
app/
├── adapters/
│   ├── databases/
│   │   ├── postgresql_adapter.py
│   │   └── sqlite_adapter.py
│   ├── external_apis/
│   │   └── vendor_api_adapter.py
│   └── kafka/
│       └── kafka_producer.py
├── api/
│   └── endpoints/
│       ├── products.py
│       └── vendors.py
├── core/
│   └── config.py
├── db/
│   ├── base.py
│   ├── base_class.py
│   └── session.py
├── dependencies.py
├── domain/
│   ├── models/
│   │   ├── product.py
│   │   └── vendor.py
│   └── schemas/
│       ├── pagination.py
│       ├── product.py
│       └── vendor.py
├── main.py
├── repositories/
│   ├── implementations/
│   │   ├── sqlite_product_repository.py
│   │   └── sqlite_vendor_repository.py
│   └── interfaces/
│       ├── product_repository.py
│       └── vendor_repository.py
└── services/
    ├── implementations/
    │   ├── product_service_impl.py
    │   └── vendor_service_impl.py
    └── interfaces/
        ├── product_service.py
        └── vendor_service.py
```

- `main.py:` The entry point of your FastAPI application.
- `api/endpoints/:` Contains your API route handlers.
- `core/:` Configuration and global settings.
- `domain/models/:` Your core business models (e.g., Product, Vendor).
- `domain/schemas/:` Pydantic models for request and response validation.
- `services/:` Business logic interfaces and implementations.
- `repositories/:` Data access layer interfaces and implementations.
- `adapters/:` External system integrations (e.g., Kafka, databases, external APIs).
- `db/:` Database session management.
- `utils/:` Utility functions and helpers.


## Prerequisites
Python 3.9+
Kafka
Flink
SQLite
PostgreSQL
SymmetricDS
Virtual Environment (optional but recommended)


## Common Commands
- uvicorn app.main:app --reload

- docker exec -it kafka-docker-kafka-1 kafka-topics --create --topic vendor_requests --bootstrap-server localhost:29092 --replication-factor 1 --partitions 1
- docker exec -it kafka-docker-kafka-1 kafka-topics --create --topic product_requests --bootstrap-server localhost:29092 --replication-factor 1 --partitions 1

