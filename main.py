from flask import Flask, request
import requests

app = Flask(__name__)

DISCORD_WEBHOOK_URL = "https://discordapp.com/api/webhooks/1560020035156705330/iCLQHgJbbMU3hzc3QTYBy_GU2oL1jPHOkxIR3833tAZyjFq7k2dw5TpW8rlgonXccsB7"
HELMET_ICON = "https://i.imgur.com/v82M98J.png"

@app.route('/dink-webhook', methods=['POST'])
def handle_dink():
    data = request.json
    if not data:
        return "No Data", 400

    event_type = data.get("type", "NOTIFICATION")
    player_name = data.get("playerName", "Player")
    extra = data.get("extra", {})
    
    title_text = "Notification"
    description_text = ""
    image_url = None

    if event_type == "PLAYER_LOGIN":
        world = extra.get("world", "Unknown")
        title_text = "Player Login"
        description_text = f"{player_name} logged into World {world}"

    elif event_type == "PLAYER_LOGOUT":
        title_text = "Player Logout"
        description_text = f"{player_name} logged out"

    elif event_type == "LEVEL":
        skill = extra.get("skill", "Skill")
        level = extra.get("level", "0")
        title_text = "Level Up"
        description_text = f"{player_name} has levelled **{skill}** to {level}"
        
        file_urls = data.get("fileUrls", [])
        if file_urls:
            image_url = file_urls[0]

    embed = {
        "author": {"name": player_name, "icon_url": HELMET_ICON},
        "title": title_text,
        "description": description_text,
        "color": 0x2b2d31,
        "footer": {"text": "Swift Services", "icon_url": HELMET_ICON}
    }

    if image_url:
        embed["image"] = {"url": image_url}

    payload = {"embeds": [embed]}
    requests.post(DISCORD_WEBHOOK_URL, json=payload)
    return "Success", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
