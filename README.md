# RPi-AQI
Use a Raspberry Pi to retrieve air quality index (AQI) data and activate a relay based on pollution levels
  
Using AirNow API current as of September 2026  

  *Details*  
  
RPi-AQI uses a Raspberry Pi single board computer to poll air quality index (AQI) data from the US Government website https://www.airnow.gov . When the AQI number is above a set point (bad air quality) the RPi will activate a relay via GPIO pin.  When the air quality improves, (AQI falls below the set point) the relay is switched off.  AQI data is retrieved for a specific location via "reporting area code" (not to be confused with phone area code).
  
The user needs to obtain an API key from https://docs.airnowapi.org/ and enter that into the code, along with the desired reporting area code.  The API data is currently limited (by AirNow) to 500 data pulls per hour, however, data on the site is usually updated every hour so more frequent pulls are not necessarily going to return better data.  The (configurable) poll frequency defaults to once every minute.  It is unlikely you would ever exceed the 500 polls per hour, even if you were running several devices under a single API key.  

  *Use Cases*

So why would anyone want this?  Well, if you have an HVAC system that ducts fresh air to increase efficiency (e.g., pulling in cold outside air to reduce cooling load), you may wish to disable this during periods of high pollution such as wildfire or smog.  Or if you have electronic windows or vents controlled by something like Home Assistant, you may want to close those sources of outside air if pollutants are high.  

At a higher level of abstraction, the code is an exercise in parsing JSON data, and activating real-world devices based on the results.  

  *Prerequisites*  

`sudo install python3-requests python3-rpi.gpio`  

  This should currently work for Raspberry Pi 2,3,4, and 5(?) but may not work with gpio libraries on a Raspberry Pi B+ (aka Pi 1).  Consult your favorite LLM for help converting to run on a Pi 1.  
  
