import requests
import time
import RPi.GPIO as GPIO

# Configuration
API_KEY = "YOUR-API-KEY-HERE"  # Replace with your key from https://docs.airnowapi.org/
REPORTING_CODE = "tx052"                          # Replace with your target reporting area code
RELAY_PIN = 18                                    # GPIO pin connected to the relay module
THRESHOLD = 45                                    # Threshold AQI to activate relay

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.output(RELAY_PIN, GPIO.LOW) # Relay off by default (assuming active low logic)

def get_aqi(reporting_code, api_key):
    """
    Fetch current AQI for a given reporting code from AirNow API.
    
    :param reporting_code: AirNow reporting area code.
    :param api_key: API key from AirNow.
    :return: Integer AQI value for PM2.5 pollutants.

    """
    url = "https://www.airnowapi.org/aq/observation/current/racode/"
    params = {
        "format": "application/json",
        "reportingAreaCode": reporting_code,
        "API_KEY": api_key
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data and len(data) > 0:
            # AirNow returns a list; take the second (PM2.5) valid observation
            aqi_value = data[1]["nowcastAQI"]
            return int(aqi_value)
        return None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def main():
    try:
        while True:
            aqi = get_aqi(REPORTING_CODE, API_KEY)
            
            if aqi is not None:
                print(f"Current AQI: {aqi}")
                
                # Activate relay if AQI >= 50
                if aqi >= THRESHOLD:
                    print("AQI >= ",THRESHOLD,": Activating relay")
                    GPIO.output(RELAY_PIN, GPIO.HIGH) # Turn relay ON
                else:
                    print("AQI < ",THRESHOLD,": Deactivating relay")
                    GPIO.output(RELAY_PIN, GPIO.LOW)  # Turn relay OFF
            else:
                print("Could not retrieve AQI data.")
            
            # Wait 1 minute before next check (AirNow limits to 500 polls/hour)
            time.sleep(60)
            
    except KeyboardInterrupt:
        print("Stopping...")
        GPIO.output(RELAY_PIN, GPIO.LOW)
        GPIO.cleanup()

if __name__ == "__main__":
    main()

