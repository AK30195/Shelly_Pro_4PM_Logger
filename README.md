# Shelly_Pro_4PM_Logger
This is a Python script to enable long-term storage of readings from a Shelly Pro 4PM. The script is setup to store readings for switch status(on/off), power, current and temperature in CSV format which can then be easily viewed using Excel or a similar application.
The Shelly Pro 4PM is a professional 4-channel DIN rail smart switch. The script is setup to take hourly readings from each of the 4 channels on the device and will create a new CSV file each day, named by date.

## Usage
1. Download the Shelly_Pro_4PM_Logger.py script from this repository.
2. Store the script in a folder where you would like your device's readings to be stored.
3. Find the IP address that your Shelly Pro 4PM is using. Open the script and edit the `SHELLY_URL` variable accordingly.
4. Make sure you have Python installed on your computer. Downloads available here - https://www.python.org/downloads/
5. Run the python script using command prompt/terminal. On Windows `python Shelly_Pro_4PM_Logger.py` - Mac/Linux `python3 Shelly_Pro_4PM_Logger.py`

## Altering Script
The script can be amended easily to include readings for other data points. If you navigate to `http://[Your_Shelly's_IP]/rpc/Shelly.GetStatus` in your browser you can see the other data categories that the Shelly device monitors.
Follow the syntax already setout in the script to add extra data to the CSV files.

