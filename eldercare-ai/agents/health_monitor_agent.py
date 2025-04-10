from sensors.health_data_input import HealthDataSimulator
from utils.logger import logger

class HealthMonitorAgent:
    def __init__(self):
        self.simulator = HealthDataSimulator()

    def monitor(self):
        try:
            vitals = self.simulator.get_latest_vitals()
            logger.info(f"[HealthMonitorAgent] Vitals: {vitals}")
            
            # Heart rate checks
            if vitals["heart_rate"] > 100:
                logger.warning(f"[HealthMonitorAgent] ⚠️ High heart rate detected: {vitals['heart_rate']}")
            elif vitals["heart_rate"] < 60:
                logger.warning(f"[HealthMonitorAgent] ⚠️ Low heart rate detected: {vitals['heart_rate']}")

            # Blood pressure check (simple parsing of "systolic/diastolic" format)
            blood_pressure = vitals.get("blood_pressure", "").strip()
            if blood_pressure:
                try:
                    systolic, diastolic = map(int, blood_pressure.split("/"))
                    if systolic > 140 or diastolic > 90:
                        logger.warning(f"[HealthMonitorAgent] ⚠️ High blood pressure detected: {blood_pressure}")
                    elif systolic < 90 or diastolic < 60:
                        logger.warning(f"[HealthMonitorAgent] ⚠️ Low blood pressure detected: {blood_pressure}")
                except (ValueError, IndexError):
                    logger.warning(f"[HealthMonitorAgent] ⚠️ Invalid blood pressure format: {blood_pressure}")

            # Temperature check
            if vitals["temperature"] > 38.0:
                logger.warning(f"[HealthMonitorAgent] ⚠️ High temperature detected: {vitals['temperature']}")
            elif vitals["temperature"] < 35.0:
                logger.warning(f"[HealthMonitorAgent] ⚠️ Low temperature detected: {vitals['temperature']}")
        except Exception as e:
            logger.error(f"[HealthMonitorAgent] Error monitoring vitals: {e}")

    def get_alerts(self):
        """Return a list of current health alerts."""
        alerts = []
        vitals = self.simulator.get_latest_vitals()
        if vitals["heart_rate"] > 100:
            alerts.append("High heart rate detected")
        elif vitals["heart_rate"] < 60:
            alerts.append("Low heart rate detected")
        return alerts