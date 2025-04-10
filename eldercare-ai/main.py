from agents.caregiver_agent import CaregiverAgent
from agents.companion_agent import CompanionAgent
from agents.health_monitor_agent import HealthMonitorAgent
from utils.scheduler import Scheduler
from utils.logger import logger
from sensors.voice_input import VoiceInputSimulator
from models.ollama_interface import OllamaLLM
import threading
import time

def collect_initial_profile():
    print("👤 Please enter initial details (or press Enter to skip):")
    name = input("Name: ").strip() or "Elder"
    age = input("Age: ").strip() or "70"
    habits = input("Daily Habits (comma separated, or press Enter): ").split(',') or ["rest", "walk"]
    return {"name": name, "age": age, "habits": [h.strip() for h in habits if h.strip()]}

def process_user_input(user_input, llm, caregiver, companion, health_monitor, scheduler):
    if not user_input:
        return "No input detected. Please say something!"

    prompt = f"""
      You are an AI assistant for elderly care. Analyze the user's input and determine the intent.
      Possible intents: 'reminder', 'emotion', 'health', or 'other'.
      Respond ONLY in this JSON format:
      {{"intent": "<intent>", "details": {{...}}}}

      Do not include any other text or commentary. Just return a JSON object.

      Input: "{user_input}"
     """

    response = llm.send_prompt(prompt)
    
    try:
        import json
        intent_data = json.loads(response)
        intent = intent_data.get("intent", "other").lower()
        details = intent_data.get("details", {})

        if intent == "reminder":
            message = details.get("message", user_input)
            time_str = details.get("time", "09:00")
            caregiver.add_reminder(message, time_str)
            return f"Reminder '{message}' set for {time_str}."
        elif intent == "emotion":
            emotion = details.get("emotion", "neutral")
            response = companion.generate_response(user_input, emotion)
            return response
        elif intent == "health":
            health_monitor.monitor()
            return "Checked health vitals. See logs for details."
        else:
            return llm.send_prompt(f"Respond kindly to: '{user_input}' (keep it short).")
    except json.JSONDecodeError:
        logger.error(f"Invalid LLM response format: {response}")
        return "Sorry, I didn’t understand that. Please try again!"

def main():
    # Step 1: Collect initial profile
    user_profile = collect_initial_profile()

    # Step 2: Initialize dependencies
    scheduler = Scheduler()
    voice_input = VoiceInputSimulator()
    llm = OllamaLLM(model_name="llama3:latest")
    caregiver = CaregiverAgent(user_profile, [], scheduler)
    companion = CompanionAgent(user_profile)
    health_monitor = HealthMonitorAgent()

    # Step 3: Start scheduler in a separate thread
    scheduler_thread = threading.Thread(target=scheduler.run_scheduler, args=(60,), daemon=True)
    scheduler_thread.start()
    logger.info("Scheduler thread started")

    # Step 4: Main AI-driven loop
    logger.info("AI assistant started. Say something to interact...")
    while True:
        try:
            user_input = voice_input.listen()
            if user_input:
                response = process_user_input(user_input, llm, caregiver, companion, health_monitor, scheduler)
                print(f"🤖: {response}")
                logger.info(f"User input: {user_input}, Response: {response}")
            time.sleep(1)  # Prevent tight loop
        except KeyboardInterrupt:
            logger.info("Program terminated by user")
            break
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()