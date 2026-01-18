import asyncio
from threading import Thread
from flask import Flask, render_template
from flask_socketio import SocketIO
from bleak import BleakClient
from config import Config
from google_sheets import GoogleSheetsHandler

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
sheet_handler = GoogleSheetsHandler()

class OmronFinalEngine:
    def __init__(self):
        self.BP_UUID = "00002a35-0000-1000-8000-00805f9b34fb"

    async def start_sync(self):
        print(f"📡 Waiting for Omron BP Start... ({Config.OMRON_MAC_ADDRESS})")

        while True:
            try:
                async with BleakClient(Config.OMRON_MAC_ADDRESS, timeout=20.0) as client:
                    if not client.is_connected:
                        raise Exception("Not connected")

                    print("✅ Connected to Omron")
                    socketio.emit('status', {'msg': 'Connected'})

                    await client.start_notify(self.BP_UUID, self.data_handler)

                    print("🩺 PRESS START on BP machine NOW")

                    while client.is_connected:
                        await asyncio.sleep(1)

            except Exception as e:
                print(f"🔁 Reconnecting... {e}")
                await asyncio.sleep(3)

    def data_handler(self, sender, data):
        try:
            flags = data[0]

            systolic = int.from_bytes(data[1:3], "little") / 100
            diastolic = int.from_bytes(data[3:5], "little") / 100
            mean_ap = int.from_bytes(data[5:7], "little") / 100

            pulse = None
            index = 7
            if flags & 0x04:
                pulse = int.from_bytes(data[index:index+2], "little") / 100

            reading = {
                "systolic": systolic,
                "diastolic": diastolic,
                "pulse": pulse
            }

            print(f"💓 FETCHED READING: {reading}")

            socketio.emit("new_bp_reading", reading)
            sheet_handler.save_reading(reading)

        except Exception as e:
            print(f"⚠️ Decode Error: {e}")


omron = OmronFinalEngine()

@app.route('/')
def index():
    return render_template('index.html')

def bt_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(omron.start_sync())

if __name__ == '__main__':
    sheet_handler.initialize()
    Thread(target=bt_thread, daemon=True).start()
    socketio.run(app, host='0.0.0.0', port=5001, debug=False, allow_unsafe_werkzeug=True)