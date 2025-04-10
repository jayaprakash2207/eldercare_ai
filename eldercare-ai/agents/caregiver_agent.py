from utils.scheduler import Scheduler
from utils.logger import logger
from models.ollama_interface import OllamaLLM

class CaregiverAgent:
    def __init__(self, user_profile, reminders, scheduler: Scheduler):
        self.user_profile = user_profile
        self.reminders = reminders
        self.scheduler = scheduler
        self.logger = logger
        self.llm = OllamaLLM()

    def add_reminder(self, message, time_str):
        """Add a reminder dynamically."""
        try:
            self.scheduler.add_reminder(message, time_str)
        except Exception as e:
            self.logger.error(f"Failed to add reminder: {e}")

    def run_daily_tasks(self, behavior_logs):
        self.logger.info("Running caregiver daily tasks...")
        self._analyze_behavior_and_adapt(behavior_logs)

    def _analyze_behavior_and_adapt(self, behavior_logs):
        self.logger.info("Analyzing behavior for adaptive scheduling...")
        prompt = (
            f"User: {self.user_profile['name']}, Age: {self.user_profile['age']}, "
            f"Habits: {', '.join(self.user_profile['habits'])}\n"
            f"Behavior Logs: {behavior_logs}\n"
            "Based on this, suggest adaptive reminders or changes in schedule:"
        )
        suggestion = self.llm.send_prompt(prompt)
        self.logger.info(f"LLM Suggestion: {suggestion}")