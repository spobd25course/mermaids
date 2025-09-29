from abc import ABC, abstractmethod


class Effect(ABC):

    def __init__(self, name, duration):
        self.name = name
        self.duration = duration

    @abstractmethod
    def apply(self, target):
        pass


class Poison(Effect):

    def __init__(self, duration=3, damage=5):
        super().__init__("Яд", duration)
        self.damage = damage

    def apply(self, target):
        target.take_damage(self.damage)
        target.add_log(f"{target.name} получает {self.damage} урона от яда")


class Shield(Effect):

    def __init__(self, duration=2, shield_amount=20):
        super().__init__("Щит", duration)
        self.shield_amount = shield_amount
        self.remaining_shield = shield_amount

    def apply(self, target):
        # Щит применяется при получении урона, а не каждый ход
        pass


class Regeneration(Effect):

    def __init__(self, duration=2, heal_amount=10):
        super().__init__("Регенерация", duration)
        self.heal_amount = heal_amount

    def apply(self, target):
        target.heal(self.heal_amount)
        target.add_log(f"{target.name} восстанавливает {self.heal_amount} HP от регенерации")


class Silence(Effect):

    def __init__(self, duration=2):
        super().__init__("Немота", duration)

    def apply(self, target):
        if hasattr(target, 'apply_silence'):
            target.apply_silence(self.duration)
            target.add_log(f"{target.name} получила немоту на {self.duration} хода!")
        else:
            target.add_log(f"{target.name} сопротивляется эффекту немоты!")