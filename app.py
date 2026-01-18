# """ Ye original code ke saath wala app.py hai  """



from flask import Flask, render_template, jsonify, make_response
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/latest')
def get_latest():
    if os.path.exists("ubpm.json"):
        # File ko 'fresh' read karne ke liye loop
        with open("ubpm.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            
        # Browser ko batana ke data cache NA kare
        response = make_response(jsonify(data))
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    
    return jsonify({"error": "No data found"})

if __name__ == '__main__':
    # Debug=False taake background mein sahi chale
    app.run(debug=False, port=8080)





# """ Ye originakl code ke saath wala app.py hai  """
















# from flask import Flask, render_template, jsonify
# import json
# import os

# app = Flask(__name__)

# @app.route('/')
# def index():
#     # Ye line templates folder mein index.html dhoondti hai
#     return render_template('index.html')

# @app.route('/api/latest')
# def get_latest():
#     if os.path.exists("ubpm.json"):
#         with open("ubpm.json", "r") as f:
#             return jsonify(json.load(f))
#     return jsonify({"error": "No data found"})

# if __name__ == '__main__':
#     # Dashboard ko http://127.0.0.1:8080 par chalayega
#     app.run(debug=True, port=8080)