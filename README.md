
# Weather Monitoring System

This project implements a real-time weather monitoring system using FastAPI.

## Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix or MacOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file in the root directory with the following content:
   ```
   OPENWEATHERMAP_API_KEY=your_api_key_here
   DATABASE_URL=sqlite:///./weather_data.db
   ```
6. Run the application: `uvicorn main:app --reload`

## API Endpoints

- GET `/`: Root endpoint
- GET `/current-weather/{city}`: Get current weather for a city
- GET `/daily-summary/{city}`: Get daily weather summary for a city
- POST `/set-alert-threshold`: Set temperature alert threshold
- GET `/alerts/{city}`: Get alerts for a city

## Design Choices

- FastAPI for high performance and easy API development
- SQLAlchemy for database operations
- APScheduler for scheduling periodic weather data fetching
- Pydantic for data validation and settings management
