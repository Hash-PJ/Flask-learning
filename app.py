from flask import Flask, jsonify
import requests

app = Flask(__name__)
URL = "https://v2.jokeapi.dev/joke/programming"

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


@app.route('/projects', methods=["GET"])
def get_projects():
    return jsonify({
        "projects":[
        {"name": "Guess Man", "description": "CLI based guessing game"},
        {"name": "Weather-app", "description": "Realtime weather app"},
        {"name": "Dev-Morning-brief", "description": "Tells price of gold, silver, weather, news, joke, riddles, etc to the dev"},
        {"name": "Url-shortner", "description": "Shortens the url"}
    ]}), 200


@app.route('/joke', methods=["GET"])
def get_joke():
    try:
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
        return jsonify({"Error": "No Internet cnnectivity!!!"}), 503
    except requests.exceptions.Timeout:
        return jsonify({"Error": "Request timed out!!!"}), 504
    except requests.exceptions.HTTPError as e:
        return jsonify({"Error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Unexpected error"}), 500


@app.errorhandler(404)
def not_found(e):
    return jsonify({"Error": "Route not found"}), 404

if __name__=="__main__":
    app.run(debug=True)
