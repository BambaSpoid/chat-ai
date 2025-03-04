import streamlit as st
import requests

# Adresse de votre API FastAPI (modifiez si vous déployez ailleurs)
API_URL = "http://127.0.0.1:8000"


def main():
    st.title("Chat-AI Interface")
    st.write(
        "Bienvenue sur le dashboard. Utilisez la barre latérale pour sélectionner une action."
    )

    # Menu de sélection dans la sidebar
    action = st.sidebar.radio(
        "Actions disponibles",
        (
            "Summariser un fichier texte",
            "Initialiser une conversation",
            "Continuer la conversation",
        ),
    )

    # ---- Section 1 : Summariser un fichier ----
    if action == "Summariser un fichier texte":
        st.subheader("1) Summariser un fichier texte")
        uploaded_file = st.file_uploader(
            "Choisissez un fichier .txt à résumer :", type=["txt"], key="summarize"
        )
        if st.button("Summarize!"):
            if uploaded_file is not None:
                files = {"file": (uploaded_file.name, uploaded_file, "text/plain")}
                try:
                    response = requests.post(
                        f"{API_URL}/summarize", files=files, timeout=30
                    )
                    if response.status_code == 200:
                        data = response.json()
                        summary = data.get("summary", "No summary found.")
                        st.subheader("Résumé :")
                        st.write(summary)
                    else:
                        st.error(f"Erreur (status code: {response.status_code})")
                except requests.exceptions.RequestException as e:
                    st.error(f"Erreur réseau ou timeout : {e}")
            else:
                st.warning(
                    "Veuillez sélectionner un fichier avant de cliquer sur Summarize!"
                )

    # ---- Section 2 : Initialiser la conversation ----
    elif action == "Initialiser une conversation":
        st.subheader("2) Initialiser la conversation")
        init_file = st.file_uploader(
            "Choisissez un fichier .txt pour initialiser la conversation :",
            type=["txt"],
            key="init",
        )
        if st.button("Initialize!"):
            if init_file is not None:
                files = {"file": (init_file.name, init_file, "text/plain")}
                try:
                    response = requests.post(
                        f"{API_URL}/initialize", files=files, timeout=30
                    )
                    if response.status_code == 200:
                        data = response.json()
                        summary = data.get("summarize", "")
                        st.subheader("Résumé initial obtenu :")
                        st.write(summary)
                        st.success("Conversation initialisée avec succès !")
                    else:
                        st.error(
                            f"Erreur lors de l'initialisation (status code: {response.status_code})"
                        )
                except requests.exceptions.RequestException as e:
                    st.error(f"Erreur réseau ou timeout : {e}")
            else:
                st.warning(
                    "Veuillez sélectionner un fichier avant de cliquer sur Initialize!"
                )

    # ---- Section 3 : Continuer la conversation ----
    else:  # "Continuer la conversation"
        st.subheader("3) Continuer la conversation")
        user_input = st.text_input("Posez une question ou envoyez un message :")

        if st.button("Envoyer", key="update"):
            if user_input.strip():
                try:
                    response = requests.post(
                        f"{API_URL}/update", data=user_input.encode("utf-8"), timeout=30
                    )
                    if response.status_code == 200:
                        # /update renvoie un StreamingResponse, on récupère le contenu complet ici
                        st.subheader("Réponse du modèle :")
                        st.write(response.text)
                    else:
                        st.error(
                            f"Erreur lors de la mise à jour (status code: {response.status_code})"
                        )
                except requests.exceptions.RequestException as e:
                    st.error(f"Erreur réseau ou timeout : {e}")
            else:
                st.warning(
                    "Veuillez saisir une question ou un message avant de cliquer sur Envoyer !"
                )


if __name__ == "__main__":
    main()
