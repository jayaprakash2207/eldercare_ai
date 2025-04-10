import datetime
import json
import os
import time
from utils.logger import logger

class Scheduler:
    def __init__(self, storage_file="data/scheduled_tasks.json"):
        self.storage_file = storage_file
        self.scheduled_tasks = []
        self._load_tasks()

    def _load_tasks(self):
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, "r") as f:
                    self.scheduled_tasks = json.load(f)
                logger.info(f"Loaded {len(self.scheduled_tasks)} tasks from {self.storage_file}")
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding tasks file: {e}")
            self.scheduled_tasks = []
        except Exception as e:
            logger.error(f"Error loading tasks: {e}")
            self.scheduled_tasks = []

    def _save_tasks(self):
        try:
            with open(self.storage_file, "w") as f:
                json.dump(self.scheduled_tasks, f)
            logger.debug(f"Saved tasks to {self.storage_file}")
        except Exception as e:
            logger.error(f"Error saving tasks: {e}")

    def add_reminder(self, message, time_str):
        """Schedule a reminder task with a message and time (HH:MM format)"""
        try:
            now = datetime.datetime.now()
            hour, minute = map(int, time_str.split(":"))
            reminder_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

            if reminder_time < now:
                reminder_time += datetime.timedelta(days=1)  # Schedule for next day

            task = {"message": message, "time": reminder_time}
            self.scheduled_tasks.append(task)
            self._save_tasks()
            logger.info(f"🗓️ Reminder Scheduled: '{message}' at {reminder_time.strftime('%H:%M')}")
        except Exception as e:
            logger.error(f"Failed to schedule reminder: {e}")

    def get_due_reminders(self):
        """Return all reminders due at the current time with a small time window"""
        try:
            now = datetime.datetime.now().replace(second=0, microsecond=0)
            time_window = datetime.timedelta(seconds=30)
            due_tasks = [task for task in self.scheduled_tasks if now - time_window <= task["time"] <= now + time_window]
            return due_tasks
        except Exception as e:
            logger.error(f"Error getting due reminders: {e}")
            return []

    def run_scheduler(self, interval=60):  # Check every minute
        """Continuously check and trigger due reminders"""
        while True:
            try:
                due = self.get_due_reminders()
                for task in due:
                    logger.info(f"🔔 Triggered Reminder: {task['message']} at {task['time'].strftime('%H:%M')}")
                    print(f"🔔 Reminder: {task['message']}")
                    self.scheduled_tasks.remove(task)
                    self._save_tasks()
                time.sleep(interval)
            except Exception as e:
                logger.error(f"Error in scheduler loop: {e}")
                time.sleep(interval)

    def cancel_reminder(self, message):
        """Remove a reminder by message (partial match)."""
        try:
            initial_count = len(self.scheduled_tasks)
            self.scheduled_tasks = [task for task in self.scheduled_tasks if message not in task["message"]]
            if len(self.scheduled_tasks) < initial_count:
                logger.info(f"Cancelled reminder containing '{message}'")
                self._save_tasks()
            else:
                logger.warning(f"No reminder found matching '{message}'")
        except Exception as e:
            logger.error(f"Error cancelling reminder: {e}")