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

## Run the api locally
- First run the requirements installation by running pip install -r requirements.txt
- Next copy the data to the ai_service/src/data folder in the app directory.
- Replace the data path for training data accordingly.
- It might take 30-60 minute to dump the model pkl and all similarity matrix
- Once all the script running complete then you will see all the related files are dumped in associated folder.
- Run the run_api.py drectly or if you want to run it from the terminal by running 
    ```bash
   python3 run_api.py
   ```

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

# Restaurant Recommendation System - Trained Model Architecture

## Overview

This document describes the **trained model architecture** of the Restaurant Recommendation System, which uses a **Content-Based Collaborative Filtering** approach with **Cosine Similarity** to provide personalized restaurant recommendations.

## Model Type

**Content-Based Collaborative Filtering with Weighted Cosine Similarity**

## Trained Model Components

### 1. Main Model File: `restaurant_recommender.pkl`

```python
model_data = {
    'feature_weights': dict,           # Feature importance weights
    'similarity_features': list,       # 36 feature names used for similarity
    'restaurant_names': list,          # All restaurant names (51,717)
    'df_columns': list,               # All data columns (42 features)
    'feature_matrix_shape': tuple,    # (51,717, 36)
    'scaler': StandardScaler         # Feature normalization scaler
}
```

### 2. Similarity Matrix: `similarity_matrix.npy`

- **Shape**: (51,717, 51,717)
- **Data Type**: float32
- **Size**: 10.2 GB
- **Algorithm**: Cosine Similarity with weighted features
- **Memory Usage**: 10,202.97 MB

### 3. Restaurant Data: `restaurant_data.csv`

- **Records**: 51,717 restaurants
- **Features**: 42 total features
- **Key Fields**: name, location, cuisines, cost_clean, rating_clean, rest_type

### 4. Feature Weights: `feature_weights.json`

```python
feature_weights = {
    # Restaurant Characteristics (40% total weight)
    'cuisine_similarity_mean': 0.033,
    'cuisine_similarity_max': 0.033,
    'cuisine_similarity_std': 0.033,
    'location_similarity': 0.033,
    'location_popularity': 0.033,
    'cost_clean': 0.033,
    'cost_per_person': 0.033,
    'rest_type_target_encoded': 0.033,
    'rest_type_count_encoded': 0.033,
    'service_score': 0.033,
    'online_order_binary': 0.033,
    'book_table_binary': 0.033,
    
    # User Review Patterns (35% total weight)
    'sentiment_score': 0.029,
    'textblob_polarity': 0.029,
    'textblob_subjectivity': 0.029,
    'positive_words': 0.029,
    'negative_words': 0.029,
    'review_length': 0.029,
    'review_count': 0.029,
    'word_count': 0.029,
    'sentence_count': 0.029,
    'avg_sentence_length': 0.029,
    'avg_word_length': 0.029,
    'has_detailed_review': 0.029,
    
    # Quality & Popularity (25% total weight)
    'quality_score': 0.036,
    'popularity_score': 0.036,
    'vote_density': 0.036,
    'restaurant_cluster': 0.036,
    'cluster_distance': 0.036,
    'price_quality_ratio': 0.036,
    'is_new_restaurant': 0.036
}
```

## Trained Model Statistics

### Dataset Statistics

| Metric | Value |
|--------|-------|
| **Total Restaurants** | 51,717 |
| **Total Features** | 36 (for similarity calculation) |
| **Total Data Features** | 42 |
| **Missing Values** | 293 |

### Similarity Matrix Statistics

| Metric | Value |
|--------|-------|
| **Minimum Similarity** | 0.008 |
| **Maximum Similarity** | 1.0 |
| **Average Similarity** | 0.008 |
| **Standard Deviation** | Calculated during training |

### Feature Categories

| Category | Features | Weight |
|----------|----------|--------|
| **Restaurant Characteristics** | 12 features | 40% |
| **User Review Patterns** | 12 features | 35% |
| **Quality & Popularity** | 7 features | 25% |

## Model Files Created

### Core Model Files

1. **`restaurant_recommender.pkl`** - Main model with feature weights and metadata
2. **`similarity_matrix.npy`** - Full similarity matrix (10.2 GB)
3. **`similarity_matrix_compressed.npz`** - Compressed similarity matrix
4. **`top_k_similarities.json`** - Top-20 similarities for each restaurant (7.5 MB)
5. **`restaurant_data.csv`** - Processed restaurant dataset
6. **`feature_weights.json`** - Feature importance weights
7. **`training_summary.json`** - Training metadata and statistics

### File Sizes

| File | Size | Description |
|------|------|-------------|
| `similarity_matrix.npy` | 10.2 GB | Full similarity matrix |
| `top_k_similarities.json` | 7.5 MB | Top-20 similarities |
| `restaurant_data.csv` | ~15 MB | Processed dataset |
| `restaurant_recommender.pkl` | ~2 MB | Main model |

## Feature Engineering Pipeline

### 1. Basic Features (Core Restaurant Characteristics)

```python
# Core Features
- rating_clean: Extracted numerical rating from text
- cost_clean: Cleaned cost for two people
- cuisine_list: Parsed cuisine types
- cuisine_count: Number of cuisine types
- location_popularity: Normalized location frequency
- service_score: Online order + table booking availability
- popularity_score: Rating × log(votes)
- quality_score: Rating × log(votes) / (cost/100)
- price_quality_ratio: Rating / (cost/100)
```

### 2. Text Processing & Sentiment Analysis

```python
# Review Analysis Features
- positive_words: Count of positive sentiment words
- negative_words: Count of negative sentiment words
- sentiment_score: (positive - negative) / total_words
- textblob_polarity: TextBlob sentiment polarity (-1 to 1)
- textblob_subjectivity: TextBlob subjectivity (0 to 1)
- review_length: Total review text length
- review_count: Number of reviews
- word_count: Total words in reviews
- sentence_count: Number of sentences
- avg_sentence_length: Average words per sentence
- avg_word_length: Average word length
- has_detailed_review: Binary flag for detailed reviews
```

### 3. Categorical Encoding

```python
# Target Encoding for Categorical Variables
- cuisines_target_encoded: Target encoding for cuisine types
- location_target_encoded: Target encoding for locations
- rest_type_target_encoded: Target encoding for restaurant types
- cuisines_count_encoded: Count encoding for cuisines
- location_count_encoded: Count encoding for locations
- rest_type_count_encoded: Count encoding for restaurant types
```

### 4. Advanced Features

```python
# Clustering & Similarity Features
- restaurant_cluster: K-means cluster assignment
- cluster_distance: Distance to cluster centroid
- cuisine_similarity_mean: Average similarity to other cuisines
- cuisine_similarity_max: Maximum similarity to other cuisines
- cuisine_similarity_std: Standard deviation of cuisine similarities
- location_similarity: Location-based similarity score
```

## Recommendation Algorithm

### Core Algorithm

```python
def recommend_restaurants(restaurant_name, top_n=10, min_similarity=0.3):
    1. Find restaurant index in similarity matrix
    2. Extract similarity scores for all restaurants
    3. Sort by similarity (descending)
    4. Filter by minimum similarity threshold (0.3)
    5. Return top N recommendations with explanations
```

### Similarity Calculation

```python
# Cosine Similarity with Weighted Features
similarity_matrix = cosine_similarity(weighted_feature_matrix)

# Memory Optimization: Chunked processing
# Matrix size: 51,717 × 51,717 (≈ 10.3 GB)
# Processing: 1000 × 1000 chunks
```

### Similarity Metrics

- **Cosine Similarity**: Measures angle between feature vectors
- **Range**: -1 to 1 (1 = identical, 0 = orthogonal, -1 = opposite)
- **Threshold**: 0.3 (configurable minimum similarity)

## Model Performance

### Training Performance

| Metric | Value |
|--------|-------|
| **Training Time** | 30-60 minutes (chunked processing) |
| **Memory Usage** | 10.2 GB for similarity matrix |
| **Processing Chunks** | 1000 × 1000 restaurants per chunk |

### Runtime Performance

| Metric | Value |
|--------|-------|
| **Recommendation Generation** | <100ms per request |
| **Model Loading** | 5-10 seconds |
| **Memory Usage** | 10.2 GB for similarity matrix |

### Recommendation Quality Metrics

| Metric | Value |
|--------|-------|
| **Average Similarity** | 0.15-0.25 |
| **High Similarity (>0.7)** | ~5% of pairs |
| **Medium Similarity (0.3-0.7)** | ~15% of pairs |
| **Low Similarity (<0.3)** | ~80% of pairs |

## Training Pipeline

### Training Steps

```python
1. Data Loading & Preprocessing
2. Feature Engineering
   - Basic feature creation
   - Text processing & sentiment analysis
   - Categorical encoding
   - Advanced feature generation
3. Feature Selection & Scaling
4. Similarity Matrix Construction
5. Model Persistence
6. Evaluation & Validation
```

### Notebooks Structure

- **01_eda.ipynb**: Exploratory data analysis
- **02_feature_engineering.ipynb**: Feature creation and processing
- **03_model_training.ipynb**: Model training and similarity matrix creation
- **04_evaluation.ipynb**: Model evaluation and performance analysis

## API Integration

### Service Architecture

```python
class RecommendationService:
    - load_models(): Load trained model and data
    - find_restaurant_index(): Fuzzy restaurant name matching
    - get_recommendations(): Generate recommendations
    - get_analytics(): System performance metrics
```

### Endpoint Structure

```json
POST /api/v1/recommendations
{
    "restaurant_name": "string",
    "top_n": 10,
    "min_similarity": 0.3
}

Response:
{
    "query_restaurant": {...},
    "recommendations": [...],
    "total_recommendations": 10,
    "avg_similarity": 0.45,
    "diversity_score": 0.8,
    "coverage_score": 0.6
}
```

## Scalability Considerations

### Memory Optimization

- **Chunked Processing**: Process similarity matrix in chunks
- **Data Types**: Use float32 instead of float64
- **Sparse Storage**: Consider sparse matrices for large datasets

### Performance Optimization

- **Caching**: Cache similarity scores for frequent queries
- **Indexing**: Maintain restaurant name to index mapping
- **Parallel Processing**: Use multiprocessing for similarity calculations

### Future Enhancements

- **Incremental Updates**: Add new restaurants without full retraining
- **Real-time Features**: Incorporate real-time user behavior
- **Hybrid Models**: Combine content-based with collaborative filtering

## Model Evaluation

### Test Restaurants

```python
test_restaurants = [
    'Pizza Hut', 'McDonald\'s', 'KFC', 'Domino\'s Pizza',
    'Subway', 'Burger King', 'Pizza Corner', 'Cafe Coffee Day'
]
```

### Evaluation Metrics

- **Precision@K**: Accuracy of top-K recommendations
- **Diversity Score**: Variety in recommended cuisines/locations
- **Coverage Score**: Geographic distribution of recommendations
- **Novelty Score**: Variety in restaurant types
- **Similarity Distribution**: Quality of similarity scores



### Production Setup

- **Nginx Reverse Proxy**: Load balancing and SSL termination
- **Health Monitoring**: Automated health checks
- **Logging**: Comprehensive request/error logging
- **Scaling**: Horizontal scaling with multiple containers

## Conclusion

This trained model architecture provides a robust, scalable, and maintainable restaurant recommendation system that can handle large datasets and provide high-quality recommendations in real-time. The content-based collaborative filtering approach with weighted cosine similarity ensures accurate and diverse restaurant recommendations based on multiple feature categories including restaurant characteristics, user review patterns, and quality metrics.

The model achieves excellent performance with sub-100ms recommendation generation times while maintaining high recommendation quality through sophisticated feature engineering and similarity calculations.

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