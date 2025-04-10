import pandas as pd
import random
from utils.logger import logger

class HealthDataSimulator:
    def __init__(self, csv_path="data/health_monitoring.csv"):
        try:
            self.data = pd.read_csv(csv_path)
            logger.info(f"Loaded health data from {csv_path} with {len(self.data)} rows")
        except FileNotFoundError:
            logger.error(f"CSV file not found: {csv_path}")
            self.data = pd.DataFrame(columns=["heart_rate", "blood_pressure", "temperature"])
        except pd.errors.EmptyDataError:
            logger.error(f"CSV file is empty: {csv_path}")
            self.data = pd.DataFrame(columns=["heart_rate", "blood_pressure", "temperature"])
        except Exception as e:
            logger.error(f"Error loading CSV: {e}")
            self.data = pd.DataFrame(columns=["heart_rate", "blood_pressure", "temperature"])
        self.index = 0

    def get_latest_vitals(self):
        if self.index >= len(self.data):
            self.index = 0
            logger.info("Reset index to start of health data cycle")
        try:
            row = self.data.iloc[self.index]
            self.index += 1
            vitals = {
                "heart_rate": float(row.get("heart_rate", random.uniform(50, 120))),
                "blood_pressure": str(row.get("blood_pressure", f"{random.randint(90, 150)}/{random.randint(60, 100)}")),
                "temperature": float(row.get("temperature", round(random.uniform(35.0, 39.0), 1)))
            }
            if not (50 <= vitals["heart_rate"] <= 120):
                logger.warning(f"Invalid heart_rate: {vitals['heart_rate']}, clamping to range")
                vitals["heart_rate"] = max(50, min(120, vitals["heart_rate"]))
            if not (35.0 <= vitals["temperature"] <= 39.0):
                logger.warning(f"Invalid temperature: {vitals['temperature']}, clamping to range")
                vitals["temperature"] = max(35.0, min(39.0, vitals["temperature"]))
            return vitals
        except IndexError:
            logger.error("Index out of range in health data")
            return {
                "heart_rate": random.uniform(50, 120),
                "blood_pressure": f"{random.randint(90, 150)}/{random.randint(60, 100)}",
                "temperature": round(random.uniform(35.0, 39.0), 1)
            }
        except Exception as e:
            logger.error(f"Error retrieving vitals: {e}")
            return {
                "heart_rate": random.uniform(50, 120),
                "blood_pressure": f"{random.randint(90, 150)}/{random.randint(60, 100)}",
                "temperature": round(random.uniform(35.0, 39.0), 1)
            }