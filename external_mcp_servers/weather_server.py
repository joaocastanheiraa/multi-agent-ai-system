from mcp.server.fastmcp import FastMCP
import json

mcp = FastMCP("Weather")

# Dados simulados de clima para diferentes cidades
WEATHER_DATA = {
    "new york": {"temperature": "22°C", "condition": "Sunny", "humidity": "65%"},
    "london": {"temperature": "15°C", "condition": "Cloudy", "humidity": "80%"},
    "tokyo": {"temperature": "28°C", "condition": "Partly Cloudy", "humidity": "70%"},
    "paris": {"temperature": "18°C", "condition": "Rainy", "humidity": "85%"},
    "sydney": {"temperature": "25°C", "condition": "Clear", "humidity": "60%"},
    "são paulo": {"temperature": "24°C", "condition": "Partly Cloudy", "humidity": "75%"},
    "rio de janeiro": {"temperature": "29°C", "condition": "Sunny", "humidity": "78%"},
}

@mcp.tool()
async def get_weather(location: str) -> str:
    """Get weather for a specific location."""
    location_lower = location.lower().strip()
    
    if location_lower in WEATHER_DATA:
        weather = WEATHER_DATA[location_lower]
        return json.dumps({
            "location": location,
            "temperature": weather["temperature"],
            "condition": weather["condition"],
            "humidity": weather["humidity"],
            "status": "success"
        })
    else:
        return json.dumps({
            "location": location,
            "message": f"Weather data not available for {location}. Available locations: {', '.join(WEATHER_DATA.keys())}",
            "status": "not_found"
        })

@mcp.tool()
async def get_forecast(location: str, days: int = 3) -> str:
    """Get weather forecast for a location for the next few days."""
    location_lower = location.lower().strip()
    
    if location_lower in WEATHER_DATA:
        base_weather = WEATHER_DATA[location_lower]
        forecast = []
        
        for day in range(1, days + 1):
            forecast.append({
                "day": f"Day {day}",
                "temperature": base_weather["temperature"],
                "condition": base_weather["condition"],
                "humidity": base_weather["humidity"]
            })
        
        return json.dumps({
            "location": location,
            "forecast": forecast,
            "status": "success"
        })
    else:
        return json.dumps({
            "location": location,
            "message": f"Forecast data not available for {location}",
            "status": "not_found"
        })

if __name__ == "__main__":
    mcp.run(transport="streamable-http") 