

import json
from datetime import datetime


class LoggerMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log = []

    def add_log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.log.append(log_entry)
        print(log_entry)


class CritMixin:

    def calculate_crit(self, base_damage, crit_chance=0.1):
        import random
        if random.random() < crit_chance:
            self.add_log(f"⭐ КРИТИЧЕСКИЙ УРОН!")
            return base_damage * 2
        return base_damage


class SilenceMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._is_silenced = False

    @property
    def is_silenced(self):
        return self._is_silenced

    def apply_silence(self, duration=2):
        self._is_silenced = True
        self.silence_duration = duration
        self.add_log(f"{self.name} получила немоту на {duration} хода!")

    def update_silence(self):
        if self._is_silenced:
            self.silence_duration -= 1
            if self.silence_duration <= 0:
                self._is_silenced = False
                self.add_log(f"{self.name} больше не нема!")
