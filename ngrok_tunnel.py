from pyngrok import ngrok, conf, installer
import subprocess
import time
import os

# Get ngrok authtoken from environment or skip
try:
    authtoken = os.getenv('NGROK_AUTHTOKEN')
    if authtoken:
        conf.get_default().auth_token = authtoken
except:
    print("No NGROK_AUTHTOKEN - using anonymous tunnel")

print("Starting Streamlit tunnel on port 8501...")
try:
    # Kill any existing ngrok tunnels
    ngrok.kill()
    
    # Create public tunnel
    public_url = ngrok.connect(8501, "http")
    print(f"✅ Public URL: {public_url}")
    print("Press Ctrl+C to stop tunnel")
    
    # Keep tunnel alive
    while True:
        time.sleep(60)
