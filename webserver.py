from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
from config import Config

socketio = SocketIO(cors_allowed_origins="*", async_mode='threading')

def create_app(system_instance):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = Config.SECRET_KEY
    socketio.init_app(app)
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/api/status')
    def status_api():
        return jsonify(system_instance.get_status())
    
    @app.route('/api/readings')
    def readings_api():
        count = request.args.get('count', default=10, type=int)
        return jsonify(system_instance.get_recent_readings(count))
    
    @socketio.on('connect')
    def handle_connect():
        print("🌐 Web client connected")
        emit('system_status', system_instance.get_status())
        
        if system_instance.current_reading:
            emit('new_reading', system_instance.current_reading)
    
    @socketio.on('request_status')
    def handle_status_request():
        emit('status_update', system_instance.get_status())
    
    return app











# """
# Flask Web Server for Omron BP Monitor
# """

# from flask import Flask, render_template, jsonify, request
# from flask_socketio import SocketIO, emit
# from config import Config
# from datetime import datetime

# socketio = SocketIO(cors_allowed_origins="*", async_mode='threading')

# def create_app(system_instance):
#     """Create Flask application for Omron"""
#     app = Flask(__name__)
#     app.config['SECRET_KEY'] = Config.SECRET_KEY
#     socketio.init_app(app)
    
#     @app.route('/')
#     def index():
#         """Main dashboard page"""
#         return render_template(
#             'index.html',
#             config={
#                 'device_name': Config.DEVICE_NAME,
#                 'port': Config.PORT,
#                 'mac_address': Config.OMRON_MAC_ADDRESS
#             }
#         )
    
#     @app.route('/api/status')
#     def get_status_api():
#         """API endpoint for system status"""
#         return jsonify(system_instance.get_status())
    
#     @app.route('/api/readings')
#     def get_readings():
#         """API endpoint for recent readings"""
#         count = request.args.get('count', default=10, type=int)
#         return jsonify(system_instance.get_recent_readings(count))

#     @socketio.on('connect')
#     def handle_connect(auth=None):
#         """Handle new client connection"""
#         print(f"🌐 New client connected")
        
#         # Send current status
#         emit('system_status', system_instance.get_status())
        
#         # Send current reading if available
#         if system_instance.current_reading:
#             emit('new_reading', system_instance.current_reading)
        
#         # Send recent readings
#         recent = system_instance.get_recent_readings(10)
#         if recent:
#             emit('recent_readings', recent)
    
#     @socketio.on('disconnect')
#     def handle_disconnect():
#         print(f"🌐 Client disconnected")
    
#     @socketio.on('request_status')
#     def handle_status_request():
#         emit('status_update', system_instance.get_status())
    
#     @socketio.on('request_readings')
#     def handle_readings_request(data):
#         count = data.get('count', 10)
#         emit('readings_update', system_instance.get_recent_readings(count))
    
#     return app