import random
from groq import Groq
from config import settings
import json

client = Groq(api_key=settings.GROQ_API_KEY)


def generate_question_from_row(row):

    row_text = ", ".join([str(x) for x in row if x])

    prompt = f"""
Generate a very simple English question.

Data: {row_text}

STRICT RULES:
- Return ONLY valid JSON
- No explanation
- No extra text
- No line breaks inside values

Format:
{{
  "question": "simple question",
  "answer": "short answer",
  "hint1": "hint",
  "hint2": "hint",
  "topic": "general",
  "difficulty": "easy"
}}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9
        )

        content = response.choices[0].message.content.strip()

        # 🔥 CLEAN JSON
        content = content.replace("\n", " ").replace("\r", " ")

        start = content.find("{")
        end = content.rfind("}") + 1

        return json.loads(content[start:end])

    except Exception as e:
        print("Groq Error:", e)
        return None
