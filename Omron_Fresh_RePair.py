import subprocess
import sys
import time
import re
from config import Config

def refresh_connection_logic():
    """Logic: Optimized Refresh using pnputil for speed"""
    print("🚀 Initializing High-Speed Connection Refresh...")
    
    # 1. Partner Key Patch (Wahi purana logic)
    PARTNER_KEY = "E9EB2256E0D94BC0A5220F9B14AAFB6F"
    try:
        with open("omblepy.py", "r") as f:
            data = f.read()
        new_data = re.sub(r'examplePairingKey\s*=\s*bytearray\.fromhex\(".*"\)', 
                          f'examplePairingKey = bytearray.fromhex("{PARTNER_KEY}")', data)
        with open("omblepy.py", "w") as f:
            f.write(new_data)
    except: pass

    # 2. OPTIMIZED: Fast Unpair using pnputil
    print("🗑️ Removing old Windows Bond (Fast Mode)...")
    
    # Hum pehle device ki Instance ID nikalenge aur phir sirf usko remove karenge
    # Is se poora system scan nahi hota
    ps_command = (
        f"$dev = Get-PnpDevice -FriendlyName '*{Config.DEVICE_NAME}*' -ErrorAction SilentlyContinue; "
        f"if ($dev) {{ pnputil /remove-device $dev.InstanceId }}"
    )
    
    subprocess.run(["powershell", "-Command", ps_command], capture_output=True)
    
    # 3. Fresh Pair Attempt
    print("🔗 Attempting New Pair (Direct)...")
    
    # Scanning timeout ko kam rakha hai taake jaldi result mile
    pair_cmd = [
        sys.executable, "omblepy.py",
        "-d", Config.DEVICE_NAME,
        "-m", Config.MAC_ADDRESS,
        "-p" # Pair mode
    ]
    
    try:
        # Isko 10 seconds ka timeout dein, agar na ho to aage badhein
        subprocess.run(pair_cmd, timeout=15)
        print("✅ Pairing command sent.")
    except subprocess.TimeoutExpired:
        print("⚠️ Pairing taking too long, skipping to sync...")
    
    print("✨ Refresh Complete. Waiting 2s for Windows to settle.")
    time.sleep(2)





























################################# Final From Omron ####################################################





# import subprocess
# import sys
# import time
# import re
# from config import Config

# def refresh_connection_logic():
#     """Logic: Refresh by Unpairing and Fresh Pairing (First Run Only)"""
#     print("🔄 Initializing Fresh Connection Refresh...")
    
#     # 1. Partner Key Patch (Ensuring correct key is in omblepy)
#     PARTNER_KEY = "E9EB2256E0D94BC0A5220F9B14AAFB6F"
#     try:
#         with open("omblepy.py", "r") as f:
#             data = f.read()
#         new_data = re.sub(r'examplePairingKey\s*=\s*bytearray\.fromhex\(".*"\)', 
#                           f'examplePairingKey = bytearray.fromhex("{PARTNER_KEY}")', data)
#         with open("omblepy.py", "w") as f:
#             f.write(new_data)
#     except: pass

#     # 2. Force Unpair from Windows (To clear any stuck driver)
#     print("🗑️ Removing old Windows Bond...")
#     subprocess.run(["powershell", "-Command", f"Get-PnpDevice -FriendlyName '*{Config.DEVICE_NAME}*' | Remove-PnpDevice -Confirm:$false"], capture_output=True)
    
#     # 3. Fresh Pair Attempt
#     # Yahan monitor ka 'P' ya 'Sync' mode mein hona zaroori hai pehli dafa
#     print("🔗 Attempting New Pair...")
#     pair_cmd = [sys.executable, "omblepy.py", "-d", Config.DEVICE_NAME, "-m", Config.MAC_ADDRESS, "--pair"]
#     subprocess.run(pair_cmd, capture_output=True, timeout=25)
    
#     return True