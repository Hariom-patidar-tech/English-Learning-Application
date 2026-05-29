from gtts import gTTS
import os

def generate_audio(text, filename):
    path = f"static/{filename}"

    # agar already file hai to dubara mat bana (optimization)
    if not os.path.exists(path):
        tts = gTTS(text=text, lang='en')
        tts.save(path)

    return f"http://127.0.0.1:8001/{path}"