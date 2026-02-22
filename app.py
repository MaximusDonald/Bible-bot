import streamlit as st
import time
from main import ask  # ton fonction qui appelle le modèle

# Configuration de la page
st.set_page_config(
    page_title="Bible_Bot Thomas",
    page_icon="📖",
    layout="wide"
)

# ────────────────────────────────────────
# Initialisation de l'historique
# ────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []


# ────────────────────────────────────────
# Fonctions utilitaires
# ────────────────────────────────────────
def add_message(role: str, content: str):
    """Ajoute un message au format officiel Streamlit chat"""
    st.session_state.messages.append({"role": role, "content": content})


def stream_response(text: str, delay=0.015):
    """Affiche le texte en streaming (effet machine à écrire)"""
    placeholder = st.empty()
    streamed_text = ""
    
    for char in text:
        streamed_text += char
        placeholder.markdown(streamed_text + "▌")
        time.sleep(delay)
    
    placeholder.markdown(streamed_text)  # version finale sans curseur
    return streamed_text


# ────────────────────────────────────────
# Style personnalisé
# ────────────────────────────────────────
st.markdown("""
    <style>
    .stChatMessage.user {
        background-color: #e6f3ff !important;
    }
    .stChatMessage.assistant {
        background-color: #f5f5f5 !important;
    }
    @media (prefers-color-scheme: dark) {
        .stChatMessage.user {
            background-color: #2b507c !important;
        }
        .stChatMessage.assistant {
            background-color: #333 !important;
        }
    }
    .footer {
        text-align: center;
        color: #777;
        margin-top: 3rem;
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)


# ────────────────────────────────────────
# Interface principale
# ────────────────────────────────────────
st.title("📖 Thomas – Assistant Biblique")
st.caption("Pose-moi toutes tes questions sur la Bible, la théologie, les versets, les contextes historiques…")

# ─── Sidebar ─────────────────────────────
with st.sidebar:
    st.header("Options")
    if st.button("🗑️ Nouvelle conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# ─── Affichage de l'historique ───────────
for message in st.session_state.messages:
    role = "user" if message["role"] == "user" else "assistant"
    avatar = "🙋‍♂️" if role == "user" else "📖"
    
    with st.chat_message(role, avatar=avatar):
        st.markdown(message["content"])


# ─── Zone de saisie (chat input moderne) ─
if prompt := st.chat_input("Pose ta question biblique…"):
    # 1. Ajout et affichage immédiat du message utilisateur
    add_message("user", prompt)
    with st.chat_message("user", avatar="🙋‍♂️"):
        st.markdown(prompt)

    # 2. Génération de la réponse
    with st.chat_message("assistant", avatar="📖"):
        with st.spinner("Thomas réfléchit…"):
            try:
                full_response = ask(prompt)
            except Exception as e:
                full_response = f"**Erreur :** {str(e)}"

        # 3. Streaming de la réponse
        streamed_content = stream_response(full_response, delay=0.012)

        # 4. Sauvegarde de la réponse complète
        add_message("assistant", streamed_content)


# ─── Footer ──────────────────────────────
st.markdown(
    '<div class="footer">Made with ❤️ by <a href="https://www.linkedin.com/in/ghilth/" target="_blank">Ghilth GBAGUIDI</a></div>',
    unsafe_allow_html=True
)