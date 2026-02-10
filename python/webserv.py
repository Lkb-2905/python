from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings, SettingsConfigDict
import requests
from functools import lru_cache


class Settings(BaseSettings):
    """Configuration model for the application using Pydantic Settings"""
    app_name: str = "IP Geolocation API"
    circl_api_url: str = "https://ip.circl.lu"
    debug: bool = False

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


@lru_cache()
def get_settings():
    """Load settings once and cache them"""
    return Settings()


app = FastAPI(title="IP Geolocation Service")

# Add CORS middleware to allow requests from the client
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    """Root endpoint"""
    settings = get_settings()
    return {"message": "Hello from IP Geolocation API", "app_name": settings.app_name}


@app.get("/ip/{ip_address}")
async def geolocate_ip(ip_address: str):
    """
    Geolocate an IP address using the CIRCL API
    
    Args:
        ip_address: The IP address to geolocate
        
    Returns:
        JSON response containing latitude, longitude, country, and other info
    """
    settings = get_settings()
    
    try:
        # Construct the URL to query CIRCL API
        circl_url = f"{settings.circl_api_url}/geolookup/{ip_address}"
        
        # Make the request to CIRCL API with timeout
        response = requests.get(circl_url, timeout=10)
        response.raise_for_status()
        
        # Parse the JSON response - CIRCL API returns a list
        data_list = response.json()
        
        if not data_list or not isinstance(data_list, list) or len(data_list) == 0:
            raise HTTPException(
                status_code=404,
                detail=f"No geolocation data found for IP: {ip_address}"
            )
        
        # Get the first result (usually the most specific match)
        data = data_list[0]
        
        # Extract country info
        country_info = data.get("country_info", {})
        country_name = country_info.get("Country", "Unknown")
        country_code = country_info.get("Alpha-2 code", "")
        latitude = float(country_info.get("Latitude (average)", 0)) if country_info.get("Latitude (average)") else None
        longitude = float(country_info.get("Longitude (average)", 0)) if country_info.get("Longitude (average)") else None
        
        # Extract ASN info if available
        country_data = data.get("country", {})
        asn = country_data.get("AutonomousSystemNumber", "Unknown")
        asn_org = country_data.get("AutonomousSystemOrganization", "Unknown")
        
        # Build result object
        result = {
            "ip": ip_address,
            "country": country_name,
            "country_code": country_code,
            "latitude": latitude,
            "longitude": longitude,
            "city": "Unknown",  # CIRCL API doesn't provide city data
            "asn": f"{asn} ({asn_org})" if asn != "Unknown" else "Unknown",
            "timezone": "Unknown",  # CIRCL API doesn't provide timezone
        }
        
        # Validate that we have coordinates
        if result["latitude"] is None or result["longitude"] is None:
            raise HTTPException(
                status_code=404,
                detail=f"No geolocation data found for IP: {ip_address}"
            )
        
        return result
        
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="CIRCL API request timed out")
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=502, detail="Failed to connect to CIRCL API")
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail=f"IP not found in CIRCL database: {ip_address}")
        raise HTTPException(status_code=502, detail=f"CIRCL API error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    settings = get_settings()
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=settings.debug)
