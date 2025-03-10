import streamlit as st
import requests

st.title("Chat-AI Interface: résumé de texte")

## Sidebar with secrets
st.sidebar.title("Secrets")
api_key = st.sidebar.text_input("OpenAI API Key: ", type="password")
model_api = st.sidebar.text_input("Model API", type="password")

# st.secrets["OPENAI_API_KEY"]
# st.secrets["MODEL_API"]

st.header("1) Summariser un fichier texte")

if "resume" not in st.session_state:
    st.session_state.resume = None

uploaded_file = st.file_uploader("Choisissez un fichier .txt à résumer :", type=["txt"])

if uploaded_file is not None:
    files = {"file": (uploaded_file.name, uploaded_file.read(), uploaded_file.type)}

    if st.button("Summarize!"):
        response = requests.post("http://localhost:8000/initialize", files=files)
        if response.status_code == 200:
            st.session_state.resume = response.json().get("summarize")
        else:
            st.write("Erreur lors de la requête")
if st.session_state.resume:
    st.write("Résumé :")
    st.write(st.session_state.resume)

st.header("2) Assistant Intelligent")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("Entrez votre message :")

if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})
    response = requests.post(
        "http://localhost:8000/update", data={"request": user_input}, stream=True
    )
    if response.status_code == 200:
        response_text = ""
        for token in response.iter_lines():
            if token:
                response_text += token.decode("utf-8")
        st.session_state.history.append({"role": "AI", "content": response_text})
    else:
        st.write("Erreur lors de la requête")

for message in st.session_state.history:
    if message["role"] == "user":
        st.write(f"Vous : {message['content']}")
    else:
        st.write(f"AI : {message['content']}")
