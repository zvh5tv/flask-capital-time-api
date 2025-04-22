from flask import Flask, request, jsonify
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz

app = Flask(__name__)

API_TOKEN = "supersecrettoken123"

geolocator = Nominatim(user_agent="capital-time-api")
tz_finder = TimezoneFinder()

def token_required(f):
    def decorator(*args, **kwargs):
        auth = request.headers.get('Authorization')
        if auth and auth.startswith("Bearer "):
            token = auth.split(" ")[1]
            if token == API_TOKEN:
                return f(*args, **kwargs)
        return jsonify({"error": "Unauthorized"}), 401
    decorator.__name__ = f.__name__
    return decorator

@app.route('/api/time', methods=['GET'])
@token_required
def get_time():
    capital = request.args.get('capital')
    if not capital:
        return jsonify({"error": "Missing 'capital' query parameter"}), 400

    try:
        location = geolocator.geocode(capital)
        if not location:
            raise ValueError("City not found")

        timezone_str = tz_finder.timezone_at(lat=location.latitude, lng=location.longitude)
        if not timezone_str:
            raise ValueError("Timezone not found")

        tz = pytz.timezone(timezone_str)
        now = datetime.now(tz)
        utc_offset = now.strftime('%z')
        utc_offset_formatted = f"{utc_offset[:3]}:{utc_offset[3:]}"

        return jsonify({
            "capital": capital,
            "local_time": now.strftime("%Y-%m-%d %H:%M:%S"),
            "utc_offset": utc_offset_formatted
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 404

@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello, world!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

(venv) soliyanayohannes04@flask-time-api:~/flask-capital-api$ 
