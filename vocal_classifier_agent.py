from speech_to_text_agent import SpeechToTextAgent
from text_interpretation_agent import TextInterpretationAgent



class VocalClassifierAgent:
    def __init__(self):
        self.speech_to_text_agent = SpeechToTextAgent()
        self.text_interpretation_agent = TextInterpretationAgent()


    def classify_audio(self, file_path):
        text = self.speech_to_text_agent.get_text_from_audio(file_path)
        interpretation = self.text_interpretation_agent.interpret_text(text)
        return text, interpretation


if __name__ == "__main__":
    file_path = "./AUDIO.mp3"
    vocal_classifier_agent_object = VocalClassifierAgent()
    text, interpretation = vocal_classifier_agent_object.classify_audio(file_path)


    print(text)
    print("-"*50)
    for type_info, info in interpretation.items():
        print(f"{type_info.replace('_', ' ')} : {info}")