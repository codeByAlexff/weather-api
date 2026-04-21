# Weather API Wrapper with Redis Caching

A simple command-line weather application that fetches real-time weather data using the OpenWeatherMap API with Redis caching for improved performance.

This project was made following roadmap.sh:
https://roadmap.sh/projects/weather-api-wrapper-service

## Features

- **Real-time Weather Data** — Get current temperature, feels-like temperature, min/max temps, and timezone
- **Redis Caching** — Cache weather data for 1 hour to reduce API calls and improve response time
- **Temperature Conversion** — Display temperature in Celsius or Fahrenheit
- **Error Handling** — Validates city names and handles network errors gracefully
- **Timezone Support** — Shows the timezone of the requested city

## Requirements

- Python 3.7+
- Redis server running locally or remotely
- OpenWeatherMap API key (free tier available)

### Example Output

```
From API!
Temperature in MIAMI, USA:

        Celsius: 24.50°C

        Feels Like: 23.80°C

        Minimum Temperature: 22.10°C

        Maximum Temperature: 26.40°C

        Timezone: UTC-05:00
```

On subsequent requests within 1 hour, the app will use cached data:
```
From cache!
Temperature in MIAMI, USA:
...
```

## How It Works

1. **Cache Check** — Checks if weather data for the city exists in Redis cache
2. **Cache Hit** — If data exists and hasn't expired (1 hour), returns cached data instantly
3. **Cache Miss** — If data doesn't exist, fetches from OpenWeatherMap API
4. **Temperature Conversion** — Converts Kelvin to Celsius/Fahrenheit based on user input
5. **Cache Storage** — Stores the API response in Redis with 1-hour expiration
6. **Display** — Shows formatted weather information including timezone

## Configuration

Edit the cache expiration time in `weather.py`:
```python
cache.setex(f"weather:{CITY}", 3600, json.dumps(data))
# Change 3600 to desired seconds (e.g., 300 for 5 minutes)
```

## Error Handling

The app validates:
- ✓ Valid city names
- ✓ Valid country codes
- ✓ Temperature unit input (C or F)
- ✓ Network connectivity
- ✓ API response status codes

## API Key

Get a free OpenWeatherMap API key:
1. Visit [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Replace `API_KEY` in the code with your key

## Technologies Used

- **requests** — HTTP library for API calls
- **redis** — In-memory cache for storing weather data
- **json** — Serialize/deserialize cached data
- **datetime** — Timezone handling

## Future Improvements

- Multiple location searches
- Weather forecast (5-day, 16-day)
- Save favorite cities
- Web interface with Flask/Django
- Database integration for historical data
- Notifications for severe weather

## License

This project is open source and available under the MIT License.

## Author

[codeByAlexff](https://github.com/codeByAlexff)
