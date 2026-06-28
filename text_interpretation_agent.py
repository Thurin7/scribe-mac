from groq import Groq
from dotenv import load_dotenv
import os
import json


class TextInterpretationAgent:
    def __init__(self):
        load_dotenv()
        self.client = Groq(api_key=os.environ["GROQ_API_KEY"])


    @staticmethod
    def read_file(file_path):
        with open(file_path, 'r') as file:
            return file.read()
        


    def interpret_text(self, text):
        chat_completion = self.client.chat.completions.create(
            messages=[
            
                {
                     "role": "system",
                     "content": TextInterpretationAgent.read_file(file_path="./prompt_system.txt")
                },    
                {
                     "role": "user",
                     "content": text,
                }
            ],

            # The language model which will generate the completion.
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object",}
        )

        return json.loads(chat_completion.choices[0].message.content)


if __name__ == "__main__":
    story = """
    Ce matin, j'ai raté mon bus de quelques secondes et j'ai dû attendre le suivant sous la pluie. En cherchant mon téléphone pour passer le temps, je me suis rendu compte que je l'avais oublié chez moi. Finalement, j'ai profité de ce moment pour observer les gens autour de moi, et j'ai trouvé ça presque reposant.
    """ 
    text_interpretation_agent_object = TextInterpretationAgent()
    interpretation = text_interpretation_agent_object.interpret_text(text=story)

    print(interpretation)