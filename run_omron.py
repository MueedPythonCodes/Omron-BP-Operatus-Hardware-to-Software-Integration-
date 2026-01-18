import subprocess
import time
import sys
import os
import webbrowser
import sync_sheets

def start_flask():
    print(">>> Starting Dashboard Server...")
    # Ye background mein Flask start karega
    return subprocess.Popen([sys.executable, "app.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def monitor_sync():
    # Omron sync command
    cmd = [sys.executable, "omblepy.py", "-d", "hem-7361t", "-m", "00:5F:BF:2B:63:A8", "-n", "-t"]
    
    sys.stdout.write(f"\r[{time.strftime('%H:%M:%S')}] Monitoring... Press Bluetooth Button on Device.")
    sys.stdout.flush()
    
    process = subprocess.run(cmd, capture_output=True, text=True)
    
    if "communication finished" in process.stdout:
        print("\n" + "="*40)
        print(">>> DATA SYNCED!")
        
        # 1. Google Sheets update
        sync_sheets.upload_to_sheets()
        
        # 2. Browser auto-open (Flask port 8080)
        webbrowser.open("http://127.0.0.1:8080")
        print(">>> Dashboard Launched!")
        print("="*40)
        return True
    return False

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Flask start karein
    flask_proc = start_flask()
    time.sleep(2) 
    
    print("\nSYSTEM ACTIVE: Bluetooth button dabayein.")
    try:
        while True:
            if monitor_sync():
                time.sleep(10)
            else:
                time.sleep(3)
    except KeyboardInterrupt:
        flask_proc.terminate()
        print("\nSystem Stopped.")










# import subprocess
# import time
# import sys
# import os
# import json

# # --- CONFIGURATION ---
# DEVICE_NAME = "hem-7361t"
# MAC_ADDRESS = "00:5F:BF:2B:63:A8"
# # ---------------------

# def sync_data():
#     # Terminal par status update dikhana (saaf suthra)
#     sys.stdout.write(f"\r[{time.strftime('%H:%M:%S')}] Waiting for User to press Bluetooth button... ")
#     sys.stdout.flush()
    
#     # Hum -n (New records) aur -t (Time sync) use kar rahe hain
#     cmd = [
#         sys.executable, "omblepy.py", 
#         "-d", DEVICE_NAME, 
#         "-m", MAC_ADDRESS, 
#         "-n", "-t"
#     ]
    
#     try:
#         # Background mein omblepy.py ko chalana
#         # stderr ko hide kiya hai taake "Device not found" se screen na bhare
#         process = subprocess.run(cmd, capture_output=True, text=True)
        
#         # Agar sync kamyab raha
#         if "communication finished" in process.stdout:
#             print("\n" + "="*40)
#             print(">>> SUCCESS: DATA RECEIVED!")
#             print("="*40)
            
#             # ubpm.json se latest reading nikal kar screen par dikhana
#             if os.path.exists("ubpm.json"):
#                 try:
#                     with open("ubpm.json", "r") as f:
#                         data = json.load(f)
#                         # Agar data nested hai (purana format) to handle karega
#                         # Lekin aapka naya omblepy function sirf 1 record dega
#                         print(f"User:     {data.get('user_id', '1')}")
#                         print(f"DateTime: {data.get('datetime', 'N/A')}")
#                         print(f"BP:       {data.get('sys', '0')}/{data.get('dia', '0')} mmHg")
#                         print(f"Pulse:    {data.get('bpm', '0')} bpm")
#                         print("="*40)
#                 except Exception as e:
#                     print(f"Note: Data saved but display error: {e}")
            
#             return True # Sync success
            
#     except Exception as e:
#         # Koi bara error aaye to print karein
#         pass
#     return False

# if __name__ == "__main__":
#     # Clear terminal screen
#     os.system('cls' if os.name == 'nt' else 'clear')
    
#     print("="*50)
#     print("   OMRON AUTOMATIC SYNC SERVICE IS RUNNING")
#     print("="*50)
#     print(f"Target Device: {DEVICE_NAME}")
#     print(f"MAC Address:   {MAC_ADDRESS}")
#     print("\nHOW TO USE:")
#     print("1. Take your Blood Pressure reading.")
#     print("2. When reading shows, press Bluetooth button ONCE.")
#     print("3. Watch this screen for automatic data update.")
#     print("-" * 50)
#     print("Press Ctrl+C to stop the service.")
    
#     while True:
#         success = sync_data()
        
#         # Agar sync ho gaya to 10 second rukien (taake double sync na ho)
#         # Warna har 3 second baad check karein
#         wait_time = 10 if success else 3
#         time.sleep(wait_time)