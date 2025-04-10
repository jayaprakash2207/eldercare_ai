import warnings
from utils.logger import logger

class VoiceInputSimulator:
    """
    Simulates a voice input system for zero-UI interaction.
    Useful for testing or simulating passive listening behavior.
    """
    def __init__(self):
        logger.info("🎤 VoiceInputSimulator initialized (simulate voice input)")

    def listen(self):
        try:
            user_input = input("👂 Say something (simulate voice input): ")
            logger.info(f"Received simulated voice input: {user_input}")
            return user_input
        except KeyboardInterrupt:
            logger.info("Voice input interrupted by user")
            return None
        except Exception as e:
            logger.error(f"Error during voice input simulation: {e}")
            return None

def get_passive_voice_input():
    """Legacy function-based approach. Use VoiceInputSimulator.listen() instead."""
    warnings.warn("get_passive_voice_input is deprecated. Use VoiceInputSimulator.listen() instead.", DeprecationWarning)
    try:
        return input("👂 Listening (simulate voice input): ")
    except KeyboardInterrupt:
        return None