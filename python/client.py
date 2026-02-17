import requests
import webbrowser
from nicegui import ui
from typing import Optional


class GeolocateClient:
    """Client for querying the IP geolocation API"""
    
    def __init__(self, server_hostname: str = "127.0.0.1", server_port: int = 8000):
        """
        Initialize the client with server details
        
        Args:
            server_hostname: The hostname of the server (default: localhost)
            server_port: The port of the server (default: 8000)
        """
        self.server_hostname = server_hostname
        self.server_port = server_port
        self.base_url = f"http://{server_hostname}:{server_port}"
    
    def query(self, ip_address: str) -> Optional[dict]:
        """
        Query the API for IP geolocation data
        
        Args:
            ip_address: The IP address to geolocate
            
        Returns:
            Dictionary containing geolocation data, or None if request failed
        """
        try:
            # Construct the full URL
            url = f"{self.base_url}/ip/{ip_address}"
            
            # Send GET request
            response = requests.get(url, timeout=10)
            
            # Check if request was successful
            if response.status_code == 200:
                return response.json()
            else:
                error_detail = response.json().get("detail", "Unknown error")
                raise Exception(f"Server error ({response.status_code}): {error_detail}")
                
        except requests.exceptions.Timeout:
            raise Exception("Request timed out - server may be unreachable")
        except requests.exceptions.ConnectionError:
            raise Exception(f"Failed to connect to server at {self.base_url}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request error: {str(e)}")
        except Exception as e:
            raise Exception(f"Error: {str(e)}")
    
    def open_map(self, latitude: float, longitude: float, country: str = ""):
        """
        Open OpenStreetMap centered on the given coordinates
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            country: Country name for information
        """
        # Create OSM URL centered on the coordinates with zoom level
        osm_url = f"https://www.openstreetmap.org/?mlat={latitude}&mlon={longitude}&zoom=10"
        webbrowser.open(osm_url)


# Initialize the client
client = GeolocateClient("127.0.0.1", 8000)

# Create the UI
ui.page_title("GeoIP-Vision")

with ui.card().classes("w-96 mx-auto mt-8"):
    ui.label("GeoIP-Vision").classes("text-2xl font-bold")
    ui.label("Locate any IP address on a map").classes("text-gray-600 mb-4")
    
    # Input field for IP address
    ip_input = ui.input(
        label="Target IP Address",
        placeholder="Enter an IP (e.g., 8.8.8.8)",
        value=""
    ).classes("w-full")
    
    # Server configuration inputs
    with ui.row().classes("w-full gap-2"):
        hostname_input = ui.input(
            label="Server Hostname",
            placeholder="127.0.0.1",
            value="127.0.0.1"
        ).classes("flex-1")
        
        port_input = ui.input(
            label="Server Port",
            placeholder="8000",
            value="8000"
        ).classes("w-24")
    
    # Result display area
    result_label = ui.label("Ready to geolocate...").classes("text-gray-700 mt-4")
    result_area = ui.markdown("").classes("mt-4 p-3 bg-gray-100 rounded")
    
    def on_geolocate():
        """Handle the geolocate button click"""
        ip_address = ip_input.value.strip()
        hostname = hostname_input.value.strip() or "127.0.0.1"
        port_str = port_input.value.strip() or "8000"
        
        # Validate inputs
        if not ip_address:
            ui.notify("Please enter an IP address", type="warning")
            return
        
        try:
            # Update client configuration
            client.server_hostname = hostname
            client.server_port = int(port_str)
            client.base_url = f"http://{hostname}:{port_str}"
            
            # Show loading state
            result_label.set_text("⏳ Querying API...")
            result_area.set_content("")
            
            # Query the API
            data = client.query(ip_address)
            
            if data:
                # Display results
                result_label.set_text(f"✓ Results for {ip_address}")
                
                # Format the result as markdown
                result_md = f"""
**IP Address:** {data.get('ip', 'N/A')}

**Location:** {data.get('city', 'N/A')}, {data.get('country', 'N/A')}

**Coordinates:** {data.get('latitude', 'N/A')}, {data.get('longitude', 'N/A')}

**Additional Info:**
- **Country Code:** {data.get('country_code', 'N/A')}
- **ASN:** {data.get('asn', 'N/A')}
- **Timezone:** {data.get('timezone', 'N/A')}
"""
                result_area.set_content(result_md)
                
                ui.notify(f"Opening map for {data.get('country', 'location')}...", type="positive")
                
                # Open the map
                client.open_map(
                    data['latitude'],
                    data['longitude'],
                    data.get('country', '')
                )
        
        except Exception as e:
            result_label.set_text(f"✗ Error occurred")
            result_area.set_content(f"**Error:** {str(e)}")
            ui.notify(str(e), type="negative")
    
    # Geolocate button
    ui.button("Geolocate IP", on_click=on_geolocate).classes("w-full mt-4 bg-blue-600")


# Footer with info
with ui.card().classes("w-96 mx-auto mt-4 text-center text-sm text-gray-600"):
    ui.label("Make sure the API server (webserv.py) is running on the specified hostname and port")


if __name__ == "__main__":
    ui.run(host="127.0.0.1", port=8080, reload=False)
