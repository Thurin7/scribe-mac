from recall_agent import RecallAgent
from vocal_classifier_agent import VocalClassifierAgent
import os


class RecallClassifierAgent:
    def __init__(self):
        self.recall_agent = RecallAgent()
        self.vocal_classifier = VocalClassifierAgent()

    def run(self, meeting_url, audio_path="meeting.mp3"):
        # 1. Envoyer le bot
        print("🤖 Envoi du bot dans la réunion...")
        result = self.recall_agent.send_bot(meeting_url)
        bot_id = result["id"]
        print(f"✅ Bot envoyé : {bot_id}")

        # 2. Attendre la fin de la réunion
        if self.recall_agent.wait_for_recording(bot_id):

            # 3. Télécharger l'audio
            print("⬇️ Téléchargement de l'audio...")
            audio_path = self.recall_agent.download_audio(bot_id, output_path=audio_path)

            # 4. Classifier l'audio
            print("🔍 Classification en cours...")
            text, interpretation = self.vocal_classifier.classify_audio(audio_path)

            # 5. Nettoyer le fichier audio
            os.remove(audio_path)

            return text, interpretation
        else:
            print("Timeout — l'enregistrement n'est pas encore prêt.")
            return None, None


if __name__ == "__main__":
    agent = RecallClassifierAgent()
    text, interpretation = agent.run("https://meet.google.com/vyf-viiv-ptf")

    if text:
        print("\n📝 Transcription :")
        print(text)
        print("-" * 50)
        print("🎯 Classification :")
        for type_info, info in interpretation.items():
            print(f"{type_info.replace('_', ' ')} : {info}")