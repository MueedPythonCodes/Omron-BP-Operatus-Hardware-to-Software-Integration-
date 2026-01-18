import subprocess
import time
import sys
import os
import webbrowser
import sync_sheets
import threading
from Omron_Fresh_RePair import refresh_connection_logic
from config import Config

# Counter: Taake device refresh sirf program shuru hote waqt aik baar ho
refresh_counter = [0]

def run_sync_logic():
    """
    Background Loop: Jo lagatar device dhoondta rahega bina kisi window ke.
    """
    print(">>> [OMRON] System Started in Background...")

    # STEP 1: Initial Connection Refresh
    if refresh_counter[0] == 0:
        print(">>> [OMRON] Initializing Fresh Connection... Please wait.")
        try:
            refresh_connection_logic()
            refresh_counter[0] = 1 
        except Exception as e:
            print(f">>> [OMRON] Refresh Warning: {e}")
        time.sleep(5) 

    # STEP 2: Loop mein rehna aur device dhoondna
    sync_cmd = [
        sys.executable, "omblepy.py",
        "-d", Config.DEVICE_NAME,
        "-m", Config.MAC_ADDRESS,
        "-n", "-t"
    ]
    
    while True:
        print(">>> [OMRON] 📡 Searching for Device... (Keep 'P' Flashing on Device)")
        
        # omblepy ko call karna
        process = subprocess.run(sync_cmd, capture_output=True, text=True)
        output_log = (process.stdout + process.stderr).lower()

        # CASE A: Agar Sync Kamyab ho jaye
        if "communication finished" in output_log or "success" in output_log:
            print(">>> [OMRON] ✅ Sync Success! Updating Google Sheets...")
            
            try:
                sync_sheets.upload_to_sheets()
            except Exception as e: 
                print(f">>> [OMRON] Sheets Error: {e}")
            
            # Dashboard kholna
            web_url = f"http://127.0.0.1:8080?t={int(time.time())}"
            webbrowser.open(web_url)
            
            print(f">>> [OMRON] SUCCESS: Data Synced at {time.strftime('%H:%M:%S')}")
            time.sleep(15) # Cooling time
            
        # CASE B: Agar device na mile
        else:
            print(">>> [OMRON] ⏳ Device not found. Retrying in 3s...")
            time.sleep(3) 

def start_flask():
    """Background mein Flask server (app.py) shuru karna"""
    print(">>> [OMRON] Starting Dashboard Server...")
    # Flask ko hamesha background mein hi rehna chahiye
    subprocess.Popen([sys.executable, "app.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)

if __name__ == "__main__":
    # 1. Dashboard server start karein
    start_flask()
    
    # 2. Sync Logic Loop start karein (Bina GUI ke)
    try:
        run_sync_logic()
    except KeyboardInterrupt:
        print("\n>>> [OMRON] System Stopped by User.")
        sys.exit()


















# import subprocess
# import time
# import sys
# import os
# import webbrowser
# import sync_sheets
# import tkinter as tk
# import threading
# from Omron_Fresh_RePair import refresh_connection_logic
# from config import Config

# # Counter: Taake device refresh sirf program shuru hote waqt aik baar ho
# refresh_counter = [0]

# def run_sync(status_label, sync_button, running_flag):
#     """
#     Background Thread: Jo lagatar device dhoondta rahega bina GUI hang kiye.
#     """
#     # STEP 1: Pehli dafa connection refresh karna (Taake pairing fresh ho jaye)
#     if refresh_counter[0] == 0:
#         status_label.config(text="🧹 Initializing Fresh Connection...", fg="#3b82f6")
#         try:
#             refresh_connection_logic()
#             refresh_counter[0] = 1 
#             print(f">>> Initial Refresh Done.")
#         except Exception as e:
#             print(f"Refresh Warning: {e}")
#         time.sleep(5) # Windows ko settle hone ke liye 5 second ka waqt

#     # STEP 2: Loop mein rehna aur device dhoondna
#     sync_cmd = [
#         sys.executable, "omblepy.py",
#         "-d", Config.DEVICE_NAME,
#         "-m", Config.MAC_ADDRESS,
#         "-n", "-t"
#     ]
    
#     # UI update: Button ko active dikhana
#     sync_button.config(state=tk.DISABLED, text="🚀 Auto-Sync Active", bg="#1e293b")
    
#     while running_flag[0]:
#         status_label.config(text="📡 Searching for Device... (Keep 'P' Flashing)", fg="#fbbf24")
        
#         # omblepy ko call karna aur uska output check karna
#         # Humne isay subprocess mein rakha hai taake agar omblepy crash ho, to main program na ruke
#         process = subprocess.run(sync_cmd, capture_output=True, text=True)
        
#         output_log = (process.stdout + process.stderr).lower()

#         # CASE A: Agar Sync Kamyab ho jaye
#         if "communication finished" in output_log or "success" in output_log:
#             status_label.config(text="✅ Sync Success! Updating Google Sheets...", fg="#4ade80")
            
#             # Google Sheets update karna
#             try:
#                 sync_sheets.upload_to_sheets()
#             except Exception as e: 
#                 print(f"Sheets Error: {e}")
            
#             # Browser mein dashboard kholna (Timestamp ke saath taake cache refresh ho)
#             web_url = f"http://127.0.0.1:8080?t={int(time.time())}"
#             webbrowser.open(web_url)
            
#             print(f">>> SUCCESS: Data Synced at {time.strftime('%H:%M:%S')}")
#             time.sleep(15) # 15 seconds cooling time taake device disconnect ho sakay
            
#         # CASE B: Agar device na mile (Timeout ya Not Found)
#         else:
#             # Bajaye error dene ke, hum khamoshi se foran dobara dhoondna shuru kar denge
#             status_label.config(text="⏳ Device not found. Retrying...", fg="#94a3b8")
#             print(">>> 📡 Ready & Waiting for Sync Mode......")
#             time.sleep(3) 

# def start_flask():
#     """Background mein Flask server (app.py) shuru karna"""
#     print(">>> Starting Dashboard Server...")
#     subprocess.Popen([sys.executable, "app.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
#     time.sleep(2)

# def on_closing(running_flag, root):
#     """Program band karte waqt counter reset karna"""
#     running_flag[0] = False
#     refresh_counter[0] = 0
#     print(">>> System Closing. See you next time!")
#     root.destroy()

# if __name__ == "__main__":
#     # 1. Dashboard server start karein
#     start_flask()
    
#     app_running = [True] # Hamesha True se start hoga taake thread chalta rahe
    
#     # 2. GUI Setup
#     root = tk.Tk()
#     root.title("Omron Live Sync System")
#     root.geometry("500x380")
#     root.configure(bg="#0f172a")
#     root.resizable(False, False)
    
#     # Close button handle karna
#     root.protocol("WM_DELETE_WINDOW", lambda: on_closing(app_running, root))
    
#     # UI Elements
#     tk.Label(root, text="OMRON AUTOMATION", bg="#0f172a", fg="#3b82f6", font=("Segoe UI", 22, "bold")).pack(pady=(25, 5))
    
#     instr_frame = tk.Label(root, text="AUTO-MODE INSTRUCTIONS:\n1. Keep Omron BT Button pressed until 'P' flashes.\n2. System will automatically detect and sync.\n3. Do not close this window during sync.", 
#                           bg="#1e293b", fg="#e2e8f0", font=("Segoe UI", 10), padx=20, pady=15, justify="left")
#     instr_frame.pack(pady=15)
    
#     status_label = tk.Label(root, text="System Booting...", bg="#0f172a", fg="#60a5fa", font=("Segoe UI", 13, "italic"))
#     status_label.pack(pady=10)
    
#     sync_button = tk.Button(root, text="🚀 Auto-Sync Active", 
#                            font=("Segoe UI", 13, "bold"), width=20, height=2, bg="#1e293b", fg="white", state=tk.DISABLED)
#     sync_button.pack(pady=10)

#     # 3. AUTO CALL: Thread foran start kar dena bina kisi button click ke
#     threading.Thread(target=run_sync, args=(status_label, sync_button, app_running), daemon=True).start()
    
#     root.mainloop()







































# """ Final 1 again repair nhi krna paray da sirf disconnect hoga aur system restart par again connect """



# import subprocess
# import time
# import sys
# import os
# import webbrowser
# import sync_sheets
# import tkinter as tk
# import threading
# from Omron_Fresh_RePair import refresh_connection_logic
# from config import Config

# # Counter to ensure refresh only happens once per app session
# refresh_counter = [0]

# def run_sync(status_label, running_flag):
#     # LOGIC: First run refresh
#     if refresh_counter[0] == 0:
#         status_label.config(text="🧹 First Time Refreshing... Please Wait", fg="#3b82f6")
#         refresh_connection_logic()
#         refresh_counter[0] = 1 
#         print(f">>> Initial Refresh Done. Counter: {refresh_counter[0]}")
#         time.sleep(2)

#     # LOOP: Infinite Syncing
#     sync_cmd = [
#         sys.executable, "omblepy.py",
#         "-d", Config.DEVICE_NAME,
#         "-m", Config.MAC_ADDRESS,
#         "-n", "-t"
#     ]
    
#     while running_flag[0]:
#         status_label.config(text="📡 Ready & Searching for Device...", fg="#fbbf24")
        
#         # Run omblepy
#         process = subprocess.run(sync_cmd, capture_output=True, text=True)
        
#         # Combine stdout and stderr for checking
#         output_log = (process.stdout + process.stderr).lower()

#         # Success Case
#         if "communication finished" in output_log or "success" in output_log:
#             status_label.config(text="✅ Sync Success! Updating Sheets...", fg="#4ade80")
            
#             # Step 1: Update Sheets
#             try:
#                 sync_sheets.upload_to_sheets()
#             except: print("Sheets Update Error")
            
#             # Step 2: Refresh Web Dashboard
#             web_url = f"http://127.0.0.1:8080?t={int(time.time())}"
#             webbrowser.open(web_url)
            
#             print(f">>> SUCCESS: Data Synced and Web Opened at {time.strftime('%H:%M:%S')}")
#             time.sleep(10) # Cooling time
            
#         elif "not found" in output_log or "timeout" in output_log:
#             status_label.config(text="⏳ Waiting for Reading / BT Signal...", fg="#94a3b8")
#             time.sleep(3)
#         else:
#             status_label.config(text="⚠️ Searching... Ensure BT is on", fg="#f87171")
#             time.sleep(4)

# def start_flask():
#     print(">>> Starting Dashboard Server...")
#     # Using Popen so it doesn't block the UI
#     subprocess.Popen([sys.executable, "app.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
#     time.sleep(2)

# def on_start_sync(status_label, sync_button, running_flag):
#     sync_button.config(state=tk.DISABLED, text="🚀 Auto-Sync Active", bg="#1e293b")
#     running_flag[0] = True
#     threading.Thread(target=run_sync, args=(status_label, running_flag), daemon=True).start()

# def on_closing(running_flag, root):
#     running_flag[0] = False
#     refresh_counter[0] = 0
#     print(">>> System Closing. Counter Reset.")
#     root.destroy()

# if __name__ == "__main__":
#     start_flask()
    
#     app_running = [False]
    
#     root = tk.Tk()
#     root.title("Omron Live Sync System")
#     root.geometry("500x380")
#     root.configure(bg="#0f172a")
#     root.resizable(False, False)
#     root.protocol("WM_DELETE_WINDOW", lambda: on_closing(app_running, root))
    
#     tk.Label(root, text="OMRON AUTOMATION", bg="#0f172a", fg="#3b82f6", font=("Segoe UI", 20, "bold")).pack(pady=(20, 5))
    
#     instr = "1. First Time: Press BT button (P flashes)\n2. After that: Just take reading & it will sync\n3. Counter resets only when you close app"
#     tk.Label(root, text=instr, bg="#1e293b", fg="#e2e8f0", font=("Segoe UI", 10), padx=20, pady=10).pack(pady=15)
    
#     status_label = tk.Label(root, text="System Ready", bg="#0f172a", fg="#60a5fa", font=("Segoe UI", 12, "italic"))
#     status_label.pack(pady=10)
    
#     sync_button = tk.Button(root, text="▶ Start Auto-Sync", 
#                            command=lambda: on_start_sync(status_label, sync_button, app_running), 
#                            font=("Segoe UI", 13, "bold"), width=20, height=2, bg="#3b82f6", fg="white", cursor="hand2")
#     sync_button.pack(pady=10)
    
#     root.mainloop()


# """ Final 1 again repair nhi krna paray da sirf disconnect hoga aur system restart par again connect """



















""" Final 2 again pair hoga aur system restart par again pair """



# import subprocess
# import time
# import sys
# import os
# import webbrowser
# import sync_sheets
# import tkinter as tk
# from tkinter import messagebox
# import threading

# def run_sync(status_label, running_flag):
#     # Command configuration
#     sync_cmd = [
#         sys.executable, "omblepy.py",
#         "-d", "hem-7361t",
#         "-m", "00:5F:BF:2B:63:A8",
#         "-n", "-t"
#     ]
    
#     while running_flag[0]:
#         status_label.config(text="🔄 Waiting for Omron Button...", fg="#fbbf24")
        
#         # subprocess.run code ko tab tak rok ke rakhega jab tak omblepy khatam na ho
#         process = subprocess.run(sync_cmd, capture_output=True, text=True)
        
#         # Debugging ke liye terminal par output dikhana
#         print("Omblepy Output:", process.stderr)
        
#         # Case 1: Agar sync kamyab ho gaya
#         if "communication finished" in process.stderr.lower():
#             status_label.config(text="✅ Sync Successful! Updating...", fg="#4ade80")
            
#             # Step 1: Google Sheets Update
#             sync_sheets.upload_to_sheets()
            
#             # Step 2: Web Dashboard Open/Refresh 
#             # ?t= timestamp lagane se browser purana cache use nahi karega
#             web_url = f"http://127.0.0.1:8080?t={int(time.time())}"
#             webbrowser.open(web_url)
            
#             print(f">>> SUCCESS: Data Synced and Web Opened at {time.strftime('%H:%M:%S')}")
#             time.sleep(10)  # 10 second ka gap taake device disconnect ho sake
            
#         # Case 2: Agar device nahi mili (Bluetooth button nahi dabaya)
#         elif "not found" in process.stderr.lower() or "timeout" in process.stderr.lower():
#             status_label.config(text="⏳ Device not found. Press Bluetooth button!", fg="#94a3b8")
#             time.sleep(3)  # 3 second wait karke dobara check karega
            
#         # Case 3: Koi aur error
#         else:
#             status_label.config(text="⚠️ Communication Error. Retrying...", fg="#f87171")
#             time.sleep(5)

# def start_flask():
#     # Flask server ko background mein start karna
#     print(">>> Starting Dashboard Server...")
#     subprocess.Popen([sys.executable, "app.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
#     time.sleep(2)

# def on_start_sync(status_label, sync_button, root, running_flag):
#     sync_button.config(state=tk.DISABLED, text="🚀 Auto-Sync Active", bg="#1e293b")
#     running_flag[0] = True
#     # Background thread taake GUI hang na ho
#     threading.Thread(target=run_sync, args=(status_label, running_flag), daemon=True).start()

# def on_closing(running_flag, root):
#     running_flag[0] = False
#     print(">>> Closing System...")
#     root.destroy()

# if __name__ == "__main__":
#     # Server start karein
#     start_flask()
    
#     running_flag = [False]
    
#     # GUI Setup
#     root = tk.Tk()
#     root.title("Omron Live Sync System")
#     root.geometry("500x350")
#     root.configure(bg="#0f172a")
#     root.resizable(False, False)
#     root.protocol("WM_DELETE_WINDOW", lambda: on_closing(running_flag, root))
    
#     # Header
#     tk.Label(root, text="OMRON AUTOMATION", bg="#0f172a", fg="#3b82f6", font=("Segoe UI", 20, "bold")).pack(pady=(20, 5))
#     tk.Label(root, text="Real-time Sheet & Web Sync", bg="#0f172a", fg="#94a3b8", font=("Segoe UI", 10)).pack(pady=5)
    
#     # Instructions
#     instr = "1. Wear Cuff & Take Reading\n2. Press Bluetooth Button (P flashes)\n3. System will auto-detect & sync"
#     tk.Label(root, text=instr, bg="#1e293b", fg="#e2e8f0", font=("Segoe UI", 10), padx=20, pady=10, justify="left").pack(pady=15)
    
#     # Status Area
#     status_label = tk.Label(root, text="System Ready", bg="#0f172a", fg="#60a5fa", font=("Segoe UI", 12, "italic"))
#     status_label.pack(pady=10)
    
#     # Start Button
#     sync_button = tk.Button(root, text="▶ Start Auto-Sync", 
#                            command=lambda: on_start_sync(status_label, sync_button, root, running_flag), 
#                            font=("Segoe UI", 13, "bold"), width=20, height=2, bg="#3b82f6", fg="white", cursor="hand2")
#     sync_button.pack(pady=10)
    
#     root.mainloop()



""" Final 2 again pair hoga aur system restart par again pair """


















































