# Restaurant Recommendation System

A FastAPI-based restaurant recommendation system with JWT authentication that provides personalized restaurant suggestions based on user preferences and restaurant characteristics.

## Features

- **JWT Authentication**: Secure login system with bearer token authentication
- **Restaurant Recommendations**: AI-powered recommendation engine using collaborative filtering
- **RESTful API**: Clean and well-documented API endpoints
- **Docker Support**: Containerized deployment with Docker and Docker Compose
- **Nginx Reverse Proxy**: Production-ready setup with load balancing
- **Health Monitoring**: Built-in health checks and monitoring endpoints

## Tech Stack

- **Backend**: FastAPI (Python 3.13)
- **Authentication**: JWT with passlib/bcrypt
- **ML/AI**: scikit-learn, pandas, numpy
- **Containerization**: Docker & Docker Compose
- **Reverse Proxy**: Nginx
- **Documentation**: Auto-generated OpenAPI/Swagger docs

## Project Structure

```
RestaurantRecommendationSystem/
├── app/
│   ├── api/
│   │   ├── core/
│   │   │   ├── config.py          # Application configuration
│   │   │   ├── security.py        # JWT authentication & user management
│   │   │   └── schemas.py         # Pydantic models
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── auth.py        # Authentication endpoints
│   │       │   ├── health.py      # Health check endpoints
│   │       │   └── recommendation.py # Recommendation endpoints
│   │       └── routes.py          # API route definitions
│   ├── ai_service/
│   │   └── notebooks/             # ML model training notebooks
│   └── main.py                    # FastAPI application entry point
├── infrastructure/
│   ├── Dockerfile                 # Docker image definition
│   ├── docker-compose.yml         # Multi-service orchestration
│   ├── nginx.conf                 # Nginx configuration
│   └── .dockerignore              # Docker build exclusions
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.13 (for local development)

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd RestaurantRecommendationSystem
   ```

2. **Build and run with Docker Compose**
   ```bash
   cd infrastructure
   docker-compose up --build
   ```

3. **Access the application**
   - API Documentation: http://localhost/docs
   - Health Check: http://localhost/api/v1/health/public
   - API Base URL: http://localhost/api/v1

### Local Development

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## Authentication

The system uses JWT (JSON Web Tokens) for authentication. Here's how to use it:

### 1. Login to get a token

```bash
curl -X POST "http://localhost/api/v1/auth/login" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "admin",
       "password": "admin123"
     }'
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 30
}
```

### 2. Use the token for authenticated requests

```bash
curl -X GET "http://localhost/api/v1/health" \
     -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

## Available Endpoints

### Authentication Endpoints

- `POST /api/v1/auth/login` - Login and get JWT token
- `GET /api/v1/auth/test-users` - Get test user credentials (development only)

### Health Endpoints

- `GET /api/v1/health` - Health check (requires authentication)
- `GET /api/v1/health/public` - Public health check (no authentication required)

### Recommendation Endpoints

- `POST /api/v1/recommendations` - Get restaurant recommendations
- `GET /api/v1/analytics` - Get system analytics

## Test Users

For development and testing, the following users are available:

| Username | Password | Role |
|----------|----------|------|
| admin    | admin123 | Administrator |
| user     | user123  | Regular User |
| test     | test123  | Test User |

## API Usage Examples

### Get Restaurant Recommendations

```bash
curl -X POST "http://localhost/api/v1/recommendations" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "restaurant_name": "Pizza Palace",
       "top_n": 5,
       "min_similarity": 0.3
     }'
```

### Get System Analytics

```bash
curl -X GET "http://localhost/api/v1/analytics" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Docker Commands

### Build and Run

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Individual Service Management

```bash
# Rebuild specific service
docker-compose build restaurant-api

# Restart specific service
docker-compose restart restaurant-api

# View service logs
docker-compose logs restaurant-api
```

## Environment Variables

Key environment variables that can be configured:

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | `Please change it according to the technonext policy pleaes or you can generate it by make a api request.` | JWT secret key |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | JWT token expiration time |
| `MODEL_PATH` | `/app/app/ai_service/notebooks/models/restaurant_recommender.pkl` | Path to ML model |
| `DATA_PATH` | `/app/app/ai_service/notebooks/models/restaurant_data.csv` | Path to restaurant data |
| `SIMILARITY_MATRIX_PATH` | `/app/app/ai_service/notebooks/models/similarity_matrix.npy` | Path to similarity matrix |

## Security Considerations

1. **Change the SECRET_KEY** in production
2. **Use HTTPS** in production (SSL certificates configured in nginx)
3. **Remove test users** in production
4. **Implement proper user management** for production use
5. **Add rate limiting** for API endpoints
6. **Use environment variables** for sensitive configuration

## Development

### Adding New Endpoints

1. Create endpoint in `app/api/v1/endpoints/`
2. Add route to `app/api/v1/routes.py`
3. Use `get_current_user` dependency for authentication

### Testing

```bash
# Run tests (if available)
pytest

# Test API endpoints
curl -X GET "http://localhost/api/v1/health/public"
```

## Troubleshooting

### Common Issues

1. **Port already in use**: Change ports in `docker-compose.yml`
2. **Model files missing**: Ensure ML model files are in the correct location
3. **Authentication errors**: Check JWT token expiration and format
4. **Docker build fails**: Check Python version compatibility

### Logs

```bash
# View application logs
docker-compose logs restaurant-api

# View nginx logs
docker-compose logs nginx
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please open an issue in the repository or contact the development team.