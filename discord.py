import requests

webhook_url = 'https://discord.com/api/webhooks/1401570205523640410/eSuuiNiNPNd4P0Rl_6N2WxS9lbGRPlCaToTk64MBg9nY_lMIiJYu6aJHRieaeAkdLzHl'
file_path = 'E:\OneDrive\Pictures\LastWar\BotShots\window_capture.gif'

with open(file_path, 'rb') as f:
    response = requests.post(webhook_url, files={'file': f})

# Step 5: Send status message
if response.status_code != 200:
    error_msg = f"Screenshot upload failed ❌ Status: {response.status_code}"
    requests.post(webhook_url, json={"content": error_msg})