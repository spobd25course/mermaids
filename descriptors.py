# ursula_battle/
# ├── core.py
# ├── characters.py
# ├── skills.py
# ├── effects.py
# ├── items.py
# ├── battle.py
# ├── descriptors.py
# ├── mixins.py
# └── main.py

class BoundedStat:

    def __init__(self, min_val=0, max_val=100):
        self.min_val = min_val
        self.max_val = max_val

    def __set_name__(self, owner, name):
        self.private_name = f"_{name}"

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name, self.min_val)

    def __set__(self, obj, value):
        if not (self.min_val <= value <= self.max_val):
            raise ValueError(f"Значение должно быть между {self.min_val} и {self.max_val}")
        setattr(obj, self.private_name, value)

