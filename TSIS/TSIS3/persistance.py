import json
import os

def load_data(filename, default):
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump(default, f)
        return default
    with open(filename, 'r') as f:
        return json.load(f)

def save_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def add_score(name, score, distance):
    leaderboard = load_data('leaderboard.json', [])
    leaderboard.append({"name": name, "score": score, "distance": int(distance)})
    # Сортировка по очкам, берем топ 10
    leaderboard = sorted(leaderboard, key=lambda x: x['score'], reverse=True)[:10]
    save_data('leaderboard.json', leaderboard)