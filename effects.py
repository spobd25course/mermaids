from abc import ABC, abstractmethod


class Effect(ABC):
    """Абстрактный класс эффекта"""

    def __init__(self, name, duration):
        self.name = name
        self.duration = duration

    @abstractmethod
    def apply(self, target):
        pass


class Poison(Effect):
    """Эффект яда"""

    def __init__(self, duration=3, damage=5):
        super().__init__("Яд", duration)
        self.damage = damage

    def apply(self, target):
        target.take_damage(self.damage)
        target.add_log(f"{target.name} получает {self.damage} урона от яда")


class Shield(Effect):
    """Эффект щита"""

    def __init__(self, duration=2, shield_amount=20):
        super().__init__("Щит", duration)
        self.shield_amount = shield_amount
        self.remaining_shield = shield_amount

    def apply(self, target):
        # Щит применяется при получении урона, а не каждый ход
        pass


class Regeneration(Effect):
    """Эффект регенерации"""

    def __init__(self, duration=2, heal_amount=10):
        super().__init__("Регенерация", duration)
        self.heal_amount = heal_amount

    def apply(self, target):
        target.heal(self.heal_amount)


class Silence(Effect):
    """Эффект немоты"""

    def __init__(self, duration=2):
        super().__init__("Немота", duration)

    def apply(self, target):
        target.apply_silence(self.duration)