import json
from groq import Groq

from dotenv import load_dotenv
import os



def get_text_from_audio(file_path):
    with open(file_path, "rb") as file:
       # Create a transcription of the audio file
       transcription = client.audio.transcriptions.create(
         file=file, # Required audio file
         model="whisper-large-v3-turbo", # Required model to use for transcription
         # prompt="Specify context or spelling",  # Optional
         response_format="verbose_json",  # Optional
         timestamp_granularities = ["word", "segment"], # Optional (must set response_format to "json" to use and can specify "word", "segment" (default), or both)
         language="fr",  # Optional
         temperature=0.0  # Optional
         )
       # To print only the transcription text, you'd use print(transcription.text) (here we're printing the entire transcription object to access timestamps)
    return transcription.text


if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    #specify the path to your audio file here
    file_path = "./AUDIO.mp3" # Replace with your audio file!
    text_transcription = get_text_from_audio(file_path)

    print(text_transcription)
