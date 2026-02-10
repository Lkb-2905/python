# IP Geolocation Application - Getting Started

## Status: ✓ Running Successfully!

Your application is now running with both the FastAPI server and NiceGUI client active.

### Access the Application

1. **NiceGUI Client Interface:**
   - Open your browser and go to: **http://127.0.0.1:8080**

2. **API Server (FastAPI):**
   - API Base URL: **http://127.0.0.1:8000**
   - Root endpoint: **http://127.0.0.1:8000/**
   - Geolocation endpoint: **http://127.0.0.1:8000/ip/{IP_ADDRESS}**

### Quick Test

#### Test the API Directly
Try these URLs in your browser:
- `http://127.0.0.1:8000/` - Check if server is running
- `http://127.0.0.1:8000/ip/8.8.8.8` - Geolocate Google's DNS
- `http://127.0.0.1:8000/ip/1.1.1.1` - Geolocate Cloudflare's DNS

**Example Response:**
```json
{
  "ip": "8.8.8.8",
  "country": "United States",
  "country_code": "US",
  "latitude": 37.386,
  "longitude": -122.084,
  "city": "Mountain View",
  "asn": "AS15169",
  "timezone": "America/Los_Angeles"
}
```

#### Use the Web Interface
1. Go to **http://127.0.0.1:8080**
2. Enter an IP address (try `8.8.8.8`)
3. Click "Geolocate IP"
4. View results and OpenStreetMap will automatically open

### Terminal Windows

- **Terminal 1:** FastAPI Server (webserv.py) - Running on port 8000
- **Terminal 2:** NiceGUI Client (client.py) - Running on port 8080

### Troubleshooting

- If you see "Failed to connect to server", make sure **both terminals are still running**
- If the map doesn't open, check your browser's popup blocker settings
- For invalid IP errors, use public IPs like 8.8.8.8, 1.1.1.1, or 208.67.222.222

### All Features Implemented

✓ FastAPI REST API with Pydantic configuration management  
✓ CIRCL API integration for IP geolocation  
✓ NiceGUI web interface with dynamic results  
✓ Automatic OpenStreetMap integration  
✓ Error handling and user notifications  
✓ CORS support for cross-origin requests  
✓ Environment variable configuration support  

Enjoy your IP geolocation application!
