import streamlit as st # type: ignore
import uuid
from db import conn 
from redis_db import redis_client
from chatbot_1 import ask_stormbreaker

# db = sqlite3.connect(
#     "stormbreaker.db",
#     check_same_thread=False
# )

# cursor = conn.cursor()


st.markdown("""
<style>

/* Main App */
.stApp {
    background: linear-gradient(
        180deg,
        #0B0F19 0%,
        #111827 100%
    );
    color: white;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #111827;
    border-right: 2px solid #D4AF37;
}

/* Titles */
h1, h2, h3 {
    color: #D4AF37 !important;
}

/* Buttons */
.stButton > button {
    width: 100%;
    border-radius: 12px;
    border: 1px solid #3B82F6;
    background-color: #1E293B;
    color: white;
    font-weight: bold;
}

.stButton > button:hover {
    border: 1px solid #60A5FA;
    box-shadow: 0px 0px 12px #60A5FA;
}

/* Input Box */
.stChatInputContainer {
    border-top: 1px solid #3B82F6;
}

/* Chat Messages */
[data-testid="stChatMessage"] {
    background-color: rgba(255,255,255,0.03);
    border-radius: 15px;
    padding: 10px;
    margin-bottom: 10px;
    border: 1px solid rgba(212,175,55,0.3);
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-thumb {
    background: #D4AF37;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "username" not in st.session_state:
    st.session_state.username = None

if not st.session_state.logged_in:

    st.title("⚡ StormBreaker Login")

    menu = st.radio(
        "Select Option",
        ["Login", "Register"]
    )

    if menu == "Register":
        username = st.text_input("Username")

    email = st.text_input("Email")
    password = st.text_input(
        "Password",
        type="password"
    )

    if menu == "Register":
        if st.button("Create Account"):
            if username == "" or email == "" or password == "":
                st.error("All fields are required")

            else:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM users WHERE email=%s",
                        (email,)
                    )

                existing_user = cursor.fetchone()

                if existing_user:
                    st.error(
                        "This email is already registered"
                    )

                else:
                    with conn.cursor() as cursor:   
                        cursor.execute(
                            """
                            INSERT INTO users
                            (username, email, password)
                            VALUES (%s, %s, %s)
                            """,
                            (
                                username,
                                email,
                                password
                            )
                        )

                        conn.commit()

                    st.success(
                        "Account Created Successfully!"
                    )

    else:
        if st.button("Login"):
            if email == "" or password == "":
                st.error(
                    "Email and Password are required"
                )

            else:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT * FROM users
                        WHERE email=%s AND password=%s
                        """,
                        (
                            email,
                            password
                        )
                    )

                    user = cursor.fetchone()

                if user:
                    st.session_state.logged_in = True
                    st.session_state.user_id = user[0]
                    st.session_state.username = user[1]

                    if "current_chat" in st.session_state:
                        del st.session_state.current_chat

                    st.rerun()

                else:
                    st.error(
                        "Invalid Email or Password"
                    )

    st.stop()

def load_chats():
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM chats WHERE user_id=%s",
            (st.session_state.user_id,)
        )
        return cursor.fetchall()

def create_chat():
    with conn.cursor() as cursor:
        chat_id = str(uuid.uuid4())
        cursor.execute(
            """
            INSERT INTO chats
            (id, user_id, title)
            VALUES (%s, %s, %s)
            """,
            (
                chat_id,
                st.session_state.user_id,
                "New Chat"
            )
        )

        conn.commit()

        return chat_id

def load_messages(chat_id):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM messages
            WHERE chat_id=%s
            """,
            (chat_id,)
        )

        return cursor.fetchall()

def save_message(chat_id, role, content):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO messages
            (chat_id, role, content)
            VALUES (%s, %s, %s)
            """,
            (
                chat_id,
                role,
                content
            )
        )

        conn.commit()

if "current_chat" not in st.session_state:
    chats = load_chats()
    if len(chats) == 0:
        st.session_state.current_chat = create_chat()

    else:
        st.session_state.current_chat = chats[0][0]

with st.sidebar:
    st.markdown("""
    # ⚡ StormBreaker AI

    *The Power of Asgard*
    """)

    st.write(
        f"Welcome {st.session_state.username}"
    )

    st.divider()

    if st.button(
        "➕ New Chat",
        use_container_width=True
    ):

        st.session_state.current_chat = create_chat()
        st.rerun()

    st.divider()

    st.subheader("💬 Chats")

    chats = load_chats()

    for chat in chats:
        col1, col2 = st.columns([5, 1])
        with col1:
            if st.button(
                chat[2],
                key=chat[0],
                use_container_width=True
            ):

                st.session_state.current_chat = chat[0]
                st.rerun()

        with col2:
            if st.button(
                "🗑",
                key=f"delete_{chat[0]}"
            ):
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        DELETE FROM messages
                        WHERE chat_id=%s
                        """,
                        (chat[0],)
                    )

                    cursor.execute(
                        """
                        DELETE FROM chats
                        WHERE id=%s
                        """,
                        (chat[0],)
                    )

                    conn.commit()
                    redis_client.delete(f"chat:{chat[0]}:recent_chat")

                if st.session_state.current_chat == chat[0]:
                    chats = load_chats()
                    if len(chats) > 0:
                        st.session_state.current_chat = chats[0][0]
                    else:
                        st.session_state.current_chat = create_chat()

                st.rerun()

    st.divider()
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = None
        if "current_chat" in st.session_state:
            del st.session_state.current_chat
        st.rerun()

current_chat = st.session_state.current_chat
messages = load_messages(current_chat)
st.markdown("""
<div style='text-align:center;'>

<h1>⚡ STORMBREAKER AI ⚡</h1>

<h4 style='color:#D4AF37;'>
Speak Mortal , Thunder listens.
</h4>

</div>
""", unsafe_allow_html=True)


for msg in messages:
    if msg[2] == "assistant":
        with st.chat_message(
            "assistant",
            avatar="stormbreaker_pic.png"
        ):
            st.markdown(msg[3])

    else:
        with st.chat_message(
            "user",
            avatar="👤"
        ):
            st.markdown(msg[3])

prompt = st.chat_input(
    "Ask StormBreaker AI anything..."
)

if prompt:
    save_message(
        current_chat,
        "user",
        prompt
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner(
    "⚡ Summoning the wisdom of Asgard..."
    ):

        result = ask_stormbreaker(
            prompt,
            st.session_state.user_id,
            current_chat
        )

        response = result["response"]

    save_message(
        current_chat,
        "assistant",
        response
    )

    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT title FROM chats
            WHERE id=%s
            """,
            (current_chat,)
        )

        chat = cursor.fetchone()

        with conn.cursor() as cursor:
            if chat[0] == "New Chat":
                cursor.execute(
                    """
                    UPDATE chats
                    SET title=%s
                    WHERE id=%s
                    """,
                    (
                        prompt[:30],
                        current_chat
                    )
                )
                conn.commit()

    with st.chat_message(
        "assistant",
        avatar="stormbreaker_pic.png"
    ):
        st.markdown(response)

    st.rerun()
    