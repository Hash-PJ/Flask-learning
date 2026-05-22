from flask import Flask, jsonify, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
PROJECTS = [
        {"name": "Guess Man", "description": "CLI based guessing game"},
        {"name": "Weather-app", "description": "Realtime weather app"},
        {"name": "Dev-Morning-brief", "description": "Tells price of gold, silver, weather, news, joke, riddles, etc to the dev"},
        {"name": "Url-shortner", "description": "Shortens the url"}
    ]

@app.route('/', methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to my API",
        "version": "1.0"
    }), 200


@app.route('/me', methods=["GET"])
def me():
    return jsonify({
        "name": "PJ",
        "age": 26,
        "skills": ["Python", "VSCode"],
        "currently_learning": "Flask"
    }), 200


@app.route('/projects/<int:p_id>', methods=["GET"])
def get_projects(p_id):
    if p_id> len(PROJECTS):
        return jsonify({"message": "no projects found", "results": []}), 404
    return jsonify({"project": PROJECTS[p_id-1]}), 200


@app.route('/projects/search', methods=['GET'])
def search_projects():
    query = request.args.get('name', '').lower()
    if not query:
        return jsonify({"error": "Providea search term e.g. ?name=weather"}), 400
    results = [p for p in PROJECTS if query in p['name'].lower()]
    if not results:
        return jsonify({"message": "no projects found", "results": []}), 404
    return jsonify({"results": results, "count": len(results)}), 200


@app.route('/joke', methods=["GET"])
def get_joke():
    try:
        URL = "https://v2.jokeapi.dev/joke/programming"
        joke = "No Joke"
        response = requests.get(URL, timeout=5)
        response.raise_for_status()
        data = response.json()
        if not data:
            joke = "No joke"
        if data.get('type') == 'single':
            joke = data.get('joke')
        elif data.get('type') == 'twopart':
            joke = data.get('setup')+'\n'+data.get('delivery')
        return jsonify({
            "joke": joke
        }), 200
    except requests.exceptions.ConnectionError:
        return jsonify({"Error": "No Internet connectivity!!!"}), 503
    except requests.exceptions.Timeout:
        return jsonify({"Error": "Request timed out!!!"}), 504
    except requests.exceptions.HTTPError as e:
        return jsonify({"Error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Unexpected error"}), 500


app.route('/weather/<string:city>', methods=["GET"])
def get_weather(city):
    try:
        if not city:
            return jsonify({"error": "No City found"}), 404
        api_key = os.getenv("WEATHER_API_KEY")
        if not api_key:
            return jsonify({"error": "Weather API key missing"}), 400
        params = {"q": city, "appid": api_key, "units": "metrics"}
        URL = "https://api.openweathermap.org/data/2.5/weather"
        weather = "No weather details"
        response = requests.get(URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data:
            weather = {
                "city": data.get("name", "Unknown"),
                "description": data.get("weather", [])[0].get("description", ""),
                "temperature": data.get("main", {}).get("temp"),
                "feels_like": data.get("main", {}).get("feels_like", "No info"),
                "humidity": data.get("main", {}).get("humidity", "0"),
                "visibiliity": data.get("visibilty", "0")
            }
        return jsonify({
            "weather": weather
        }), 200
    except requests.exceptions.ConnectionError:
        return jsonify({"Error": "No Internet connectivity!!!"}), 503
    except requests.exceptions.Timeout:
        return jsonify({"Error": "Request timed out!!!"}), 504
    except requests.exceptions.HTTPError as e:
        return jsonify({"Error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Unexpected error"}), 500


@app.route("/projects", methods=["POST"])
def create_projects():
    data = request.json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    name = data.get("name")
    desc = data.get("description")
    if not name:
        return jsonify({"error": "name is required"}),400
    if not desc:
        return jsonify({"error": "Description is required"}),400
    return jsonify({
        "message": f"Project {name} created",
        "project": {"name": name, "description": desc}
    }), 201


@app.errorhandler(404)
def not_found(e):
    return jsonify({"Error": "Route not found"}), 404

if __name__=="__main__":
    app.run(debug=True)
