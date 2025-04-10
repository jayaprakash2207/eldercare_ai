from models.ollama_interface import OllamaLLM
from models.emotion_analysis import EmotionAnalyzer
from sensors.voice_input import VoiceInputSimulator
from utils.logger import logger

class CompanionAgent:
    def __init__(self, user_profile: dict):
        self.user_profile = user_profile
        self.llm = OllamaLLM()
        self.emotion_analyzer = EmotionAnalyzer(use_llm=True)  # Use LLM for emotion detection
        self.logger = logger
        self.conversation_log = []

    def detect_emotion(self, voice_text: str):
        """
        Analyze emotional tone from user speech.
        """
        emotion = self.emotion_analyzer.analyze_emotion(voice_text)
        self.logger.log(f"Detected emotion: {emotion}")
        return emotion

    def generate_response(self, user_input: str, emotion: str):
        """
        Use LLM to respond empathetically based on detected emotion and context.
        """
        prompt = (
            f"You are a kind, empathetic voice assistant for elderly care. "
            f"The user seems to be feeling {emotion}. They said: '{user_input}'. "
            f"Reply in a supportive, simple, and comforting way considering their age (~{self.user_profile['age']} yrs). "
            f"Keep it short, like a warm sentence or two."
        )
        response = self.llm.send_prompt(prompt)
        self.logger.log(f"Generated response: {response}")
        return response

    def engage(self):
        """
        Main loop for passive emotional engagement.
        """
        self.logger.log("Listening for user voice input...")
        try:
            voice_input = VoiceInputSimulator()
            user_input = voice_input.listen()
            if not user_input:
                self.logger.log("No input detected.")
                return None

            emotion = self.detect_emotion(user_input)
            response = self.generate_response(user_input, emotion)

            self.conversation_log.append({
                "user": user_input,
                "emotion": emotion,
                "response": response
            })

            return {
                "user_input": user_input,
                "emotion": emotion,
                "response": response
            }
        except Exception as e:
            self.logger.error(f"Error in engage: {e}")
            return None