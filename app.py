import os
import json
from uninformed import bfs, dfs, ucs, ids
from informed import a_star, greedy_best_first
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

MAP_DATA_FILE = "map_data.json"


def load_map_data():
    """Load graph and location data from map_data.json if available."""
    if os.path.exists(MAP_DATA_FILE):
        try:
            with open(MAP_DATA_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {MAP_DATA_FILE}: {e}")
    return {
        "region": "State / Metro Area",
        "total_cities": 0,
        "total_edges": 0,
        "locations": {},
        "graph": {}
    }


@app.route("/")
def index():
    """Renders the main deployment webpage."""
    return render_template("index.html")


@app.route("/api/map", methods=["GET"])
def get_map():
    """Returns map locations and graph connections."""
    data = load_map_data()
    return jsonify(data)


@app.route("/api/search", methods=["POST"])
def search():
    """
    Search endpoint placeholder for deployment testing.
    """
    payload = request.get_json() or {}
    start = payload.get("start", "")
    goal = payload.get("goal", "")
    algorithm = payload.get("algorithm", "")
    data= load_map_data()
    result = {"path": [], "distance": 0, "expanded": []}
    if algorithm == "bfs":
        result = bfs(data, start, goal)
    elif algorithm == "dfs":
            result = dfs(data, start, goal)
    elif algorithm == "ucs":
            result = ucs(data, start, goal)
    elif algorithm == "ids":
            result = ids(data, start, goal)
    elif algorithm == "astar":
                result = a_star(data, start, goal)
    elif algorithm == "greedy":
                result = greedy_best_first(data, start, goal)

    print("Algorithm received:", algorithm)
    return jsonify({
        "status": "ready",
        "message": f"Deployment server active. Request received for algorithm '{algorithm}' from '{start}' to '{goal}'.",
        "path": result["path"],
        "cost": result["distance"],
        "nodes_expanded": len(result["expanded"])
        
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
