from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from config.settings import Settings
from services.weather_service import WeatherService
from services.alert_service import AlertService
from models.weather_data import WeatherData
from utils.weather_analyzer import WeatherAnalyzer

app = FastAPI()

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

settings = Settings()
weather_service = WeatherService(settings)
alert_service = AlertService(settings)
weather_analyzer = WeatherAnalyzer()

scheduler = BackgroundScheduler()
scheduler.add_job(weather_service.fetch_weather_data, 'interval', minutes=5)
scheduler.start()

@app.on_event("startup")
async def startup_event():
    # Initialize database connection, etc.
    pass

@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()

@app.get("/")
async def root():
    return {"message": "Weather Monitoring System API"}

@app.get("/current-weather/{city}")
async def get_current_weather(city: str):
    return await weather_service.get_current_weather(city)

@app.get("/daily-summary/{city}")
async def get_daily_summary(city: str):
    return weather_analyzer.get_daily_summary(city)

@app.post("/set-alert-threshold")
async def set_alert_threshold(threshold: float, city: str):
    alert_service.set_threshold(threshold, city)
    return {"message": f"Alert threshold set to {threshold}°C for {city}"}

@app.get("/alerts/{city}")
async def get_alerts(city: str):
    return alert_service.get_alerts(city)