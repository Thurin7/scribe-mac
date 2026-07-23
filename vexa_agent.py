import requests
import os
from dotenv import load_dotenv


class VexaAgent:
    def __init__(self):
        load_dotenv()
        self.api_key = os.environ["VEXA_API_KEY"]
        self.base_url = "https://api.cloud.vexa.ai"
        self.headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }

    def send_bot(self, platform, meeting_id, bot_name="Vexa"):
        response = requests.post(
            f"{self.base_url}/bots",
            headers=self.headers,
            json={
                "platform": platform,
                "native_meeting_id": meeting_id,
                "bot_name": bot_name
            }
        )
        return response.json()

    def get_transcript(self, platform, meeting_id):
        response = requests.get(
            f"{self.base_url}/transcripts/{platform}/{meeting_id}",
            headers=self.headers
        )
        return response.json()

    def stop_bot(self, platform, meeting_id):
        response = requests.delete(
            f"{self.base_url}/bots/{platform}/{meeting_id}",
            headers=self.headers
        )
        return response.status_code


if __name__ == "__main__":
    vexa = VexaAgent()

    # 1. Envoyer le bot dans une réunion Google Meet
    #result = vexa.send_bot(
    #    platform="google_meet",
    #   meeting_id="ejp-duws-etx"  # l'ID dans l'URL de ta réunion
    #)
    # print("Bot envoyé :", result)

    # 2. Récupérer la transcription
    transcript = vexa.get_transcript("google_meet", "ejp-duws-etx")
    for segment in transcript.get("segments", []):
        print(f"{segment['speaker']} : {segment['text']}")

    # 3. Arrêter le bot
    # vexa.stop_bot("google_meet", "ejp-duws-etx")