import random
import models

from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.sql.expression import func

from db import SessionLocal, engine, Base
from config import settings

from services import *
from models import Question, Attempt

from fastapi.staticfiles import StaticFiles
from tts_service import generate_audio
from groq_service import generate_question_from_row
from excel_loader import load_all_excels

app = FastAPI()
# ================= CHAT MANAGER =================

class ConnectionManager:

    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):

        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):

        disconnected = []

        for connection in self.active_connections:

            try:
                await connection.send_text(message)

            except:
                disconnected.append(connection)

        for conn in disconnected:

            if conn in self.active_connections:
                self.active_connections.remove(conn)

manager = ConnectionManager()
# ================= CORS =================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================= STATIC =================
app.mount("/static", StaticFiles(directory="static"), name="static")

# ================= DB =================
Base.metadata.create_all(bind=engine)

# ================= DB SESSION =================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ================= HOME =================
@app.get("/")
def home():
    return {"msg": "API running 🚀"}

# ================= HELPER =================
def generate_ai_question(db, topic="general"):
    rows = list(load_all_excels())
    row = random.choice(rows)

    result = generate_question_from_row(row)

    if not result:
        return None

    # 🔥 UNIQUE banane ke liye random add karo
    result["question"] += f" ({random.randint(1,10000)})"

    if topic != "All":
        result["topic"] = topic

    save_questions(db, result)

    return db.query(Question).order_by(func.random()).first()

# ================= GENERATE QUESTIONS =================
@app.post("/generate-questions")
def generate(db: Session = Depends(get_db)):

    count = 0

    for row in load_all_excels():
        for _ in range(2):   # 🔥 multiple questions per row

            result = generate_question_from_row(row)

            if not result:
                continue

            question_text = result.get("question", "").lower()

            if not question_text or "nan" in question_text:
                continue

            # 🔥 loose duplicate check
            existing = db.query(Question).filter(
                Question.question.ilike(f"%{question_text[:20]}%")
            ).first()

            if existing:
                continue

            save_questions(db, result)
            count += 1

    return {"msg": f"{count} questions generated"}

# ================= START QUIZ =================
@app.get("/quiz/start")
def start_quiz(
    topic: str = "All",
    used_ids: str = "",
    db: Session = Depends(get_db)
):

    used_list = [int(x) for x in used_ids.split(",") if x]

    query = db.query(Question)

    if topic != "All":
        query = query.filter(Question.topic.ilike(f"%{topic}%"))

    if used_list:
        query = query.filter(~Question.id.in_(used_list))

    q = query.order_by(func.random()).first()

    # 🔥 AI fallback
    if not q:
        q = generate_ai_question(db, topic)

    if not q:
        return {"msg": "No questions available"}

    audio_url = generate_audio(q.question, f"q_{q.id}.mp3")

    return {
        "question_id": q.id,
        "question": q.question,
        "audio_url": audio_url
    }

# ================= NEXT QUESTION =================


@app.get("/quiz/next")
def next_question(
    topic: str = "All",
    used_ids: str = "",
    db: Session = Depends(get_db)
):

    used_list = [int(x) for x in used_ids.split(",") if x]

    use_ai = random.random() < 0.3   # 🔥 30% AI

    if use_ai:
        q = generate_ai_question(db, topic)

        if q:
            audio_url = generate_audio(q.question, f"q_{q.id}.mp3")

            return {
                "question_id": q.id,
                "question": q.question,
                "audio_url": audio_url
            }

    # 👉 DB fallback
    query = db.query(Question)

    if topic != "All":
        query = query.filter(Question.topic.ilike(f"%{topic}%"))

    if used_list:
        query = query.filter(~Question.id.in_(used_list))

    q = query.order_by(func.random()).first()

    if not q:
        q = generate_ai_question(db, topic)

    if not q:
        return {"msg": "No more questions"}

    audio_url = generate_audio(q.question, f"q_{q.id}.mp3")

    return {
        "question_id": q.id,
        "question": q.question,
        "audio_url": audio_url
    }
# ============= SUBMIT =================
@app.post("/submit-answer")
def submit(q_id: int, answer: str, db: Session = Depends(get_db)):

    q = db.query(Question).filter(Question.id == q_id).first()

    if not q:
        raise HTTPException(404, "Question not found")

    attempt = db.query(Attempt).filter(Attempt.question_id == q_id).first()

    if not attempt:
        attempt = Attempt(question_id=q_id, attempt_count=1)
        db.add(attempt)
    else:
        attempt.attempt_count += 1

    db.commit()

    is_correct = check_answer(answer, q.correct_answer)

    if is_correct:
        return {"correct": True}

    if attempt.attempt_count == 2:
        return {"correct": False, "hint": q.hint1}

    if attempt.attempt_count >= 3:
        return {
            "correct": False,
            "correct_answer": q.correct_answer
        }

    return {"correct": False}

# ================= ALL QUESTIONS =================
@app.get("/all-questions")
def all_questions(db: Session = Depends(get_db)):
    return db.query(Question).all()

# ================= WEBSOCKET CHAT =================

@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):

    await manager.connect(websocket)

    try:

        while True:

            data = await websocket.receive_text()

            if "|" not in data:
                continue

            username, message = data.split("|", 1)

            final_message = f"👤 {username}: {message}"

            await manager.broadcast(final_message)

    except WebSocketDisconnect:

        manager.disconnect(websocket)