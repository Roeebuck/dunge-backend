import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Nastavení DeepSeek API klíče sss
DEEPSEEK_API_KEY = "sk-b0169bef2c044b3db675bc2a516c9104"
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"


@app.route('/next', methods=['POST'])
def next_scene():
    data = request.json
    character = data.get("character", "Neznámá postava")
    user_input = data.get("input", "")

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": f"Jsi vypravěč fantasy příběhu. Hráč hraje za {character}."},
            {"role": "user", "content": user_input}
        ]
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Vyhodí výjimku pro chybové stavy HTTP
        response_data = response.json()
        
        story_text = response_data["choices"][0]["message"]["content"]
        return jsonify({"story": story_text})
    
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"API request failed: {str(e)}"}), 500
    except KeyError:
        return jsonify({"error": "Invalid response format from API"}), 500

if __name__ == '__main__':
    app.run(debug=True)