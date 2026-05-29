import streamlit as st
import requests
import streamlit.components.v1 as components

BASE_URL = "http://127.0.0.1:8001"

st.set_page_config(page_title="English Learning", layout="centered")

# ================= CSS =================
st.markdown("""
<style>

.stApp {
    background: linear-gradient(130deg, #667eea, #764ba2, #ff6a00);
    background-size: 200% 200%;
    animation: gradientMove 10s ease infinite;
    color: white;
}

@keyframes gradientMove {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.title {
    text-align: center;
    font-size: 45px;
    font-weight: bold;
}

.subtitle {
    text-align: center;
    color: #ddd;
    margin-bottom: 25px;
}

.card {
    background: rgba(255,255,255,0.08);
    padding: 25px;
    border-radius: 20px;
    backdrop-filter: blur(15px);
    box-shadow: 0 10px 40px rgba(0,0,0,0.3);
}

.stButton>button {
    background: linear-gradient(90deg, #ff6a00, #ee0979);
    color: white;
    border-radius: 12px;
    height: 45px;
    font-weight: bold;
    border: none;
}

</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown(
    '<div class="title">English Learning App</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Quiz + Live Chat + Practice</div>',
    unsafe_allow_html=True
)

# ================= SESSION =================
if "question" not in st.session_state:
    st.session_state.question = None
    st.session_state.q_id = None
    st.session_state.audio = None
    st.session_state.used_questions = []
    st.session_state.answered = False
    st.session_state.username = None

# ================= NAME =================
st.markdown("### 👤 Enter Your Name")

name = st.text_input("Your Name")

if st.button("Enter Chat"):

    if name.strip() == "":
        st.warning("⚠️ Enter name first")

    else:
        st.session_state.username = name
        st.success(f"Welcome {name} 👋")

# ================= START QUIZ =================
if st.button("🎯 Start Quiz"):

    st.session_state.used_questions = []
    st.session_state.answered = False

    res = requests.get(f"{BASE_URL}/quiz/start").json()

    if "question" in res:

        st.session_state.question = res["question"]
        st.session_state.q_id = res["question_id"]
        st.session_state.audio = res["audio_url"]

# ================= QUIZ =================
if st.session_state.question:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("🧠 Question")

    st.write(st.session_state.question)

    if st.session_state.audio:
        st.audio(st.session_state.audio)

    answer = st.text_input("✍️ Your Answer")

    col1, col2 = st.columns(2)

    # ===== SUBMIT =====
    with col1:

        if st.button("✅ Submit"):

            res = requests.post(
                f"{BASE_URL}/submit-answer",
                params={
                    "q_id": st.session_state.q_id,
                    "answer": answer
                }
            ).json()

            st.session_state.answered = True

            if res.get("correct"):

                st.success("🎉 Correct Answer!")

            else:

                st.error("❌ Incorrect")

                if "hint" in res:
                    st.info(f"💡 Hint: {res['hint']}")

                if "correct_answer" in res:
                    st.warning(
                        f"📘 Correct Answer: {res['correct_answer']}"
                    )

    # ===== NEXT =====
    with col2:

        if st.session_state.answered:

            if st.button("➡ Next"):

                res = requests.get(
                    f"{BASE_URL}/quiz/next",
                    params={
                        "used_ids": ",".join(
                            map(str, st.session_state.used_questions)
                        )
                    }
                ).json()

                if "question" in res:

                    st.session_state.question = res["question"]
                    st.session_state.q_id = res["question_id"]
                    st.session_state.audio = res["audio_url"]

                    st.session_state.used_questions.append(
                        res["question_id"]
                    )

                    st.session_state.answered = False

                else:

                    st.success("🏁 Quiz Completed")

                    st.session_state.question = None

    st.markdown('</div>', unsafe_allow_html=True)

# ================= CHAT =================
# ================= CHAT + NAVBAR =================
if st.session_state.username:

    components.html(f"""
    
    <style>

    body {{
        margin: 0;
        padding: 0;
    }}

    /* ================= NAVBAR ================= */

    .navbar {{
        position: fixed;
        top: 0;
        left: 0;

        width: 100%;
        height: 70px;

        background: rgba(0,0,0,0.35);

        backdrop-filter: blur(12px);

        display: flex;
        align-items: center;
        justify-content: space-between;

        padding: 0px 20px;

        z-index: 99999;

        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }}

    .nav-left {{
        display: flex;
        align-items: center;
        gap: 10px;

        color: white;

        font-size: 22px;
        font-weight: bold;
    }}

    .logo {{
        width: 45px;
        height: 45px;

        border-radius: 50%;

        background: white;

        color: #ff6a00;

        display: flex;
        align-items: center;
        justify-content: center;

        font-size: 22px;
    }}

    .nav-right {{
        display: flex;
        align-items: center;
        gap: 15px;

        margin-right: 40px;
    }}

    .nav-user {{
        color: white;
        font-size: 15px;
        font-weight: bold;
    }}

    .chat-icon {{
        width: 50px;
        height: 50px;

        border-radius: 50%;
        border: none;

        background: #25D366;

        color: white;

        font-size: 22px;

        cursor: pointer;

        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }}

    /* ================= CHAT BOX ================= */

    .chat-box {{
        position: fixed;

        top: 80px;
        right: 20px;

        width: 330px;
        height: 400px;

        background: #efeae2;

        border-radius: 20px;

        overflow: hidden;

        display: none;
        flex-direction: column;

        box-shadow: 0 8px 30px rgba(0,0,0,0.3);

        z-index: 9999;
    }}

    .chat-header {{
        background: #075E54;

        color: white;

        padding: 12px;

        display: flex;
        align-items: center;
        gap: 10px;

        font-size: 17px;
        font-weight: bold;
    }}

    .chat-avatar {{
        width: 40px;
        height: 40px;

        border-radius: 50%;

        background: white;

        color: #075E54;

        display: flex;
        align-items: center;
        justify-content: center;

        font-size: 18px;
        font-weight: bold;
    }}

    /* ================= MESSAGES ================= */

    .chat-messages {{
        flex: 1;

        overflow-y: auto;

        padding: 12px;

        display: flex;
        flex-direction: column;

        gap: 10px;

        background: #e5ddd5;
    }}

    .my-message {{
        align-self: flex-end;

        background: #DCF8C6;

        padding: 10px 14px;

        border-radius: 15px 15px 0px 15px;

        max-width: 75%;

        color: black;

        font-size: 14px;

        box-shadow: 0 2px 5px rgba(0,0,0,0.1);

        word-wrap: break-word;
    }}

    .other-message {{
        align-self: flex-start;

        background: white;

        padding: 10px 14px;

        border-radius: 15px 15px 15px 0px;

        max-width: 75%;

        color: black;

        font-size: 14px;

        box-shadow: 0 2px 5px rgba(0,0,0,0.1);

        word-wrap: break-word;
    }}

    .username {{
        font-size: 11px;

        font-weight: bold;

        color: #075E54;

        margin-bottom: 4px;
    }}

    /* ================= INPUT ================= */

    .chat-input {{
        display: flex;

        align-items: center;

        gap: 10px;

        padding: 10px;

        background: #f0f0f0;
    }}

    .chat-input input {{
        flex: 1;

        border: none;

        outline: none;

        padding: 12px;

        border-radius: 25px;

        font-size: 14px;
    }}

    .send-btn {{
        width: 45px;
        height: 45px;

        border-radius: 50%;

        border: none;

        background: #25D366;

        color: white;

        font-size: 18px;

        cursor: pointer;
    }}

    </style>

    <!-- ================= NAVBAR ================= -->

    <div class="navbar">

        <div class="nav-left">

            <div class="logo">
                📘
            </div>

            <div>
                English Learning
            </div>

        </div>

        <div class="nav-right">

            <div class="nav-user">
                👋 {st.session_state.username}
            </div>

            <button
                class="chat-icon"
                onclick="toggleChat()"
            >
                💬
            </button>

        </div>

    </div>

    <!-- ================= CHAT BOX ================= -->

    <div class="chat-box" id="chatBox">

        <div class="chat-header">

            <div class="chat-avatar">
                {st.session_state.username[:1].upper()}
            </div>

            <div>
                Live Chat
            </div>

        </div>

        <div
            class="chat-messages"
            id="chatMessages"
        ></div>

        <div class="chat-input">

            <input
                id="msg"
                type="text"
                placeholder="Type a message..."
            >

            <button
                class="send-btn"
                onclick="sendMsg()"
            >
                ➤
            </button>

        </div>

    </div>

    <!-- ================= JAVASCRIPT ================= -->

    <script>

    let ws = null;

    let username = "{st.session_state.username}";

    function connectWS() {{

        if(ws && ws.readyState === WebSocket.OPEN) {{
            return;
        }}

        ws = new WebSocket(
             "ws://127.0.0.1:8001/ws/chat"
        );

        ws.onopen = function() {{
            console.log("✅ Connected");
        }};

        ws.onclose = function() {{
            console.log("❌ Disconnected");
        }};

        ws.onerror = function(error) {{
            console.log(error);
        }};

        ws.onmessage = function(e) {{

            let chat =
                document.getElementById(
                    "chatMessages"
                );

            let data = e.data;

            let parts = data.split(":");

            let sender = parts[0]
                .replace("👤", "")
                .trim();

            let message = parts
                .slice(1)
                .join(":");

            let div =
                document.createElement("div");

            if(sender === username) {{
                div.className = "my-message";
            }}
            else {{
                div.className = "other-message";
            }}

            div.innerHTML =
                "<div class='username'>"
                + sender +
                "</div>"
                +
                "<div>"
                + message +
                "</div>";

            chat.appendChild(div);

            chat.scrollTop =
                chat.scrollHeight;
        }};
    }}

    window.onload = function() {{
        connectWS();
    }};

    function toggleChat() {{

        let box =
            document.getElementById(
                "chatBox"
            );

        if(box.style.display === "flex") {{

            box.style.display = "none";
        }}
        else {{

            box.style.display = "flex";
        }}
    }}

    function sendMsg() {{

        let input =
            document.getElementById(
                "msg"
            );

        if(!input) return;

        let message =
            input.value.trim();

        if(message.length === 0)
            return;

        if(
            ws &&
            ws.readyState === 1
        ) {{

            ws.send(
                username + "|" + message
            );

            input.value = "";

            input.focus();
        }}
    }}

    document.addEventListener(
        "DOMContentLoaded",
        function() {{

            let input =
                document.getElementById(
                    "msg"
                );

            if(input) {{

                input.addEventListener(
                    "keypress",
                    function(e) {{

                        if(
                            e.key === "Enter"
                        ) {{

                            e.preventDefault();

                            sendMsg();
                        }}
                    }}
                );
            }}
        }}
    );

    </script>

    """, height=650,
         scrolling=True
    )

else:
    st.warning("⚠️ Enter name to enable chat")