#!/usr/bin/env python3
import requests
import time
import csv
from datetime import datetime

# Shelly device GetStatus URL
SHELLY_URL = "http://192.168.1.10/rpc/Shelly.GetStatus"

# Create filename with today's date
def get_filename():
    return f"shelly_log_{datetime.now().strftime('%Y-%m-%d')}.csv"

# Create CSV file to store data and write column headers
def initialize_csv():
    try:
        with open(get_filename(), mode='x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Switch_0 - Status", "Switch_0 - apower(watts)", "Switch_0 - current(amps)", "Switch_0 - temp(celsius°C)", 
                             "Switch_1 - Status", "Switch_1 - apower(watts)", "Switch_1 - current(amps)", "Switch_1 - temp(°C)",
                             "Switch_2 - Status", "Switch_2 - apower(watts)", "Switch_2 - current(amps)", "Switch_2 - temp(°C)", 
                             "Switch_3 - Status", "Switch_3 - apower(watts)", "Switch_3 - current(amps)", "Switch_3 - temp(°C)"])
    except FileExistsError:
        pass  # File already exists

# Read values from the Shelly device and output to CSV file
def read_Shelly():
    try:
        # Get JSON from Shelly http response
        response = requests.get(SHELLY_URL, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Extract readings for each of the 4 switches
        status0 = data.get("switch:0", {}).get("output", {})
        status1 = data.get("switch:1", {}).get("output", {})
        status2 = data.get("switch:2", {}).get("output", {})
        status3 = data.get("switch:3", {}).get("output", {})
        # Status reading changed from true/false to On/Off
        rawStatuses = [status0, status1, status2, status3]
        statuses = []
        for status in rawStatuses:
            if status is True:
                statuses.append('On')
            else: statuses.append('Off')
    
        apower0 = data.get("switch:0", {}).get("apower", {})
        apower1 = data.get("switch:1", {}).get("apower", {})
        apower2 = data.get("switch:2", {}).get("apower", {})
        apower3 = data.get("switch:3", {}).get("apower", {})
        
        current0 = data.get("switch:0", {}).get("current", {})
        current1 = data.get("switch:1", {}).get("current", {})
        current2 = data.get("switch:2", {}).get("current", {})
        current3 = data.get("switch:3", {}).get("current", {})
        
        temp0 = data.get("switch:0", {}).get("temperature", {}).get("tC", None)
        temp1 = data.get("switch:1", {}).get("temperature", {}).get("tC", None)
        temp2 = data.get("switch:2", {}).get("temperature", {}).get("tC", None)
        temp3 = data.get("switch:3", {}).get("temperature", {}).get("tC", None)

        # Timestamp for readings
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Write timestamp & readings to CSV file
        with open(get_filename(), mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, statuses[0], apower0, current0, temp0, statuses[1], apower1, current1, temp1,
                             statuses[2], apower2, current2, temp2, statuses[3], apower3, current3, temp3])
        # Console logging
        print(f"[{timestamp}] Logged status: {statuses[0]}, {statuses[1]}, {statuses[2]}, {statuses[3]}")
        print(f"[{timestamp}] Logged apower: {apower0}, {apower1}, {apower2}, {apower3}")
        print(f"[{timestamp}] Logged current: {current0}, {current1}, {current2}, {current3}")
        print(f"[{timestamp}] Logged temperatures: {temp0}, {temp1}, {temp2}, {temp3}")
    
    # Errors logged to console
    except Exception as e:
        print(f"[ERROR] {datetime.now()} - Failed to read Shelly: {e}")

def main():
    current_date = datetime.now().date()
    initialize_csv()
    print("Starting Shelly logger...")
    
    # Reading interval set to 1 hour, can be modified as desired
    READ_INTERVAL = 3600
    while True:
        # Check if new log file to be created if date changes
        if datetime.now().date() != current_date:
            current_date = datetime.now().date()
            initialize_csv()

        read_Shelly()
        time.sleep(READ_INTERVAL)  
        

if __name__ == "__main__":
    main()