import requests
import os
import time
from dotenv import load_dotenv
from moviepy import VideoFileClip


class RecallAgent:
    def __init__(self):
        load_dotenv()
        self.api_key = os.environ["RECALLAI_API_KEY"]
        self.region = os.environ["RECALLAI_REGION"]
        self.base_url = f"https://{self.region}.recall.ai/api/v1"
        self.headers = {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "application/json"
        }

    def send_bot(self, meeting_url, bot_name="Scribe"):
        response = requests.post(
            f"{self.base_url}/bot",
            headers=self.headers,
            json={
                "meeting_url": meeting_url,
                "bot_name": bot_name
            }
        )
        return response.json()

    def get_bot_status(self, bot_id):
        response = requests.get(
            f"{self.base_url}/bot/{bot_id}",
            headers=self.headers
        )
        return response.json()

    def download_audio(self, bot_id, output_path="meeting.mp3"):
        bot = self.get_bot_status(bot_id)
        recordings = bot.get("recordings", [])
        if not recordings:
            print("Pas d'enregistrement disponible.")
            return None

        # Récupérer l'URL du MP4
        video_url = recordings[0]["media_shortcuts"]["video_mixed"]["data"]["download_url"]

        # Télécharger le MP4
        print("Téléchargement du MP4...")
        mp4_path = "meeting_temp.mp4"
        response = requests.get(video_url)
        with open(mp4_path, "wb") as f:
            f.write(response.content)

        # Extraire l'audio avec moviepy
        print("Extraction de l'audio...")
        video = VideoFileClip(mp4_path)
        video.audio.write_audiofile(output_path)
        video.close()

        # Supprimer le MP4 temporaire
        os.remove(mp4_path)
        print(f"Audio sauvegardé : {output_path}")
        return output_path

    def stop_bot(self, bot_id):
        response = requests.post(
            f"{self.base_url}/bot/{bot_id}/leave_call",
            headers=self.headers
        )
        return response.status_code

    def wait_for_recording(self, bot_id, timeout=300):
        print("En attente de la fin de l'enregistrement...")
        start = time.time()
        while time.time() - start < timeout:
            bot = self.get_bot_status(bot_id)
            status = bot.get("status_changes", [])
            if status:
                last_status = status[-1].get("code")
                print(f"Status : {last_status}")
                if last_status == "done":
                    return True
            time.sleep(5)
        return False


if __name__ == "__main__":
    recall = RecallAgent()

    # 1. Envoyer le bot
    result = recall.send_bot("https://meet.google.com/qmj-wnff-gkf")
    print("Bot envoyé :", result["id"])
    bot_id = result["id"]

    # 2. Attendre la fin + télécharger l'audio
    if recall.wait_for_recording(bot_id):
        audio_path = recall.download_audio(bot_id, output_path="meeting.mp3")
        print("Audio prêt :", audio_path)
    else:
        print("Timeout — l'enregistrement n'est pas encore prêt.")
    
