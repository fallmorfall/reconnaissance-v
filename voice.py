import streamlit as st
import pyaudio
import speech_recognition as sr

def transcribe_speech(api_choice, language):
    r = sr.Recognizer()
    st.info("Veuillez parler maintenant...")  # Message affiché une seule fois
    with sr.Microphone() as source:
        try:
            audio_text = r.listen(source, timeout=10)
            st.info("Transcription en cours...")  # Stable, pas dans une boucle rapide

            if api_choice == "Google":
                text = r.recognize_google(audio_text, language=language)
            elif api_choice == "Sphinx":
                text = r.recognize_sphinx(audio_text, language=language)
            else:
                return "API non prise en charge."
            
            return text
        except sr.WaitTimeoutError:
            st.warning("Temps d'attente dépassé. Veuillez réessayer.")
        except sr.UnknownValueError:
            st.warning("Je n'ai pas compris ce que vous avez dit. Essayez à nouveau.")
        except sr.RequestError as e:
            st.error(f"Erreur de l'API : {str(e)}")
        except Exception as e:
            st.error(f"Une erreur inattendue s'est produite : {str(e)}")

def save_transcription(text):
    with open("transcription.txt", "w", encoding="utf-8") as file:
        file.write(text)
    st.success("Texte sauvegardé sous 'transcription.txt'.")

def main():
    st.title("Application de Reconnaissance Vocale")
    st.write("Cliquez sur le bouton pour démarrer la reconnaissance vocale.")

    # Sélection de l'API
    api_choice = st.selectbox("Choisissez l'API de reconnaissance vocale", ["Google", "Sphinx"])
    
    # Sélection de la langue
    language = st.text_input("Entrez le code de langue (ex : 'fr-FR' pour français, 'en-US' pour anglais)", "fr-FR")

    # Détection et transcription
    if st.button("Démarrer l'enregistrement"):
        text = transcribe_speech(api_choice, language)
        st.write("Transcription : ", text)
        
        # Option pour sauvegarder le texte transcrit
        if st.button("Enregistrer la transcription"):
            save_transcription(text)

    # Gestion de pause/reprise
    st.warning("Pause/reprise non implémentées dans cette version. Vous pouvez arrêter et relancer.")

if __name__ == "__main__":
    main()

