from textblob import TextBlob
from models.ollama_interface import OllamaLLM
from utils.logger import logger

class EmotionAnalyzer:
    def __init__(self, use_llm=False, model_name="llama3:latest"):
        self.logger = logger
        self.use_llm = use_llm
        self.llm = OllamaLLM(model_name=model_name) if use_llm else None  # Changed 'model' to 'model_name'

    def analyze_emotion(self, text_input: str) -> str:
        """
        Analyze the emotional tone of the user's voice input using sentiment analysis or LLM.
        Returns one of: ['happy', 'sad', 'neutral', 'angry', 'anxious']
        """
        self.logger.log(f"Analyzing emotion from input: {text_input}")

        if not text_input.strip():
            return "neutral"

        if self.use_llm:
            return self._analyze_with_llm(text_input)
        else:
            return self._analyze_with_textblob(text_input)

    def _analyze_with_textblob(self, text_input: str) -> str:
        analysis = TextBlob(text_input)
        polarity = analysis.sentiment.polarity

        self.logger.log(f"TextBlob Polarity: {polarity}")

        if polarity > 0.3:
            return "happy"
        elif polarity < -0.3:
            return "sad"
        elif -0.3 <= polarity <= -0.1:
            return "anxious"
        elif -0.1 < polarity < 0.1:
            return "neutral"
        else:
            return "angry"

    def _analyze_with_llm(self, text_input: str) -> str:
        prompt = f"""
        Analyze the emotional state in the following message and respond with a single word: 
        happy, sad, anxious, angry, or neutral.

        Message: "{text_input}"
        Response:
        """

        try:
            emotion = self.llm.send_prompt(prompt).lower().strip()
            if any(keyword in emotion for keyword in ['happy', 'sad', 'anxious', 'angry', 'neutral']):
                return emotion
            else:
                self.logger.warning(f"LLM returned invalid emotion: {emotion}")
                return "neutral"
        except Exception as e:
            self.logger.error(f"Error analyzing emotion with LLM: {e}")
            return "neutral"