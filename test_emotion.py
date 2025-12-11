import base64

with open("test.jpg", "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode()

from emotion_model import analyze_emotion_from_b64

print(analyze_emotion_from_b64(img_b64))
