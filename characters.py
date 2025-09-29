from abc import ABC, abstractmethod
from descriptors import BoundedStat
from mixins import LoggerMixin, CritMixin, SilenceMixin
from effects import Effect, Poison, Shield, Regeneration, Silence


class Mermaid(LoggerMixin):
    """Базовый класс русалочки"""

    hp = BoundedStat(0, 1000)
    mp = BoundedStat(0, 500)
    strength = BoundedStat(1, 100)
    agility = BoundedStat(1, 100)
    intelligence = BoundedStat(1, 100)

    def __init__(self, name, level=1):
        self.name = name
        self.level = level
        self._hp = 100
        self._mp = 50
        self._strength = 10
        self._agility = 10
        self._intelligence = 10
        self.max_hp = 100
        self.max_mp = 50
        super().__init__()

    @property
    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        self.hp = max(0, self.hp - damage)
        self.add_log(f"{self.name} получает {damage} урона! HP: {self.hp}")

    def heal(self, amount):
        old_hp = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        actual_heal = self.hp - old_hp
        self.add_log(f"{self.name} восстанавливает {actual_heal} HP!")
        return actual_heal

    def __str__(self):
        return f"{self.name} (Ур. {self.level}) - HP: {self.hp}/{self.max_hp} MP: {self.mp}/{self.max_mp}"

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}', {self.level})"

    def to_dict(self):
        return {
            'name': self.name,
            'level': self.level,
            'hp': self.hp,
            'max_hp': self.max_hp,
            'mp': self.mp,
            'max_mp': self.max_mp,
            'strength': self.strength,
            'agility': self.agility,
            'intelligence': self.intelligence
        }


class Character(Mermaid, ABC):
    """Абстрактный класс персонажа"""

    def __init__(self, name, level=1):
        super().__init__(name, level)
        self.effects = []
        self.cooldowns = {}
        self.skills_used = 0

    @abstractmethod
    def basic_attack(self, target):
        pass

    @abstractmethod
    def use_skill(self, target):
        pass

    def update_effects(self):
        """Обновление эффектов в начале хода"""
        new_effects = []
        for effect in self.effects:
            effect.duration -= 1
            if effect.duration > 0:
                new_effects.append(effect)
                effect.apply(self)
        self.effects = new_effects

    def add_effect(self, effect):
        self.effects.append(effect)
        self.add_log(f"{self.name} получает эффект: {effect.name}")


class Warrior(Character, CritMixin):
    """Класс воина-русалочки"""

    def __init__(self, name, level=1):
        super().__init__(name, level)
        self._strength = 20
        self._agility = 15
        self._intelligence = 5
        self.max_hp = 150
        self.hp = 150
        self.max_mp = 30
        self.mp = 30

    def basic_attack(self, target):
        if hasattr(self, 'is_silenced') and self.is_silenced:
            self.add_log(f"{self.name} нема и не может атаковать!")
            return 0

        damage = self.strength + self.level * 2
        crit_damage = self.calculate_crit(damage, 0.2)
        target.take_damage(crit_damage)
        return crit_damage

    def use_skill(self, target):
        if hasattr(self, 'is_silenced') and self.is_silenced:
            self.add_log(f"{self.name} нема и не может использовать навык!")
            return 0

        if self.mp < 15:
            self.add_log(f"Недостаточно MP для использования навыка!")
            return 0

        self.mp -= 15
        damage = self.strength * 2 + self.level * 3
        self.add_log(f"{self.name} использует МОРСКОЙ ШТОРМ!")
        target.take_damage(damage)

        # Шанс оглушить цель
        import random
        if random.random() < 0.3:
            target.add_log(f"{target.name} оглушена на 1 ход!")

        return damage


class Mage(Character, CritMixin, SilenceMixin):
    """Класс мага-русалочки"""

    def __init__(self, name, level=1):
        super().__init__(name, level)
        self._strength = 5
        self._agility = 10
        self._intelligence = 25
        self.max_hp = 80
        self.hp = 80
        self.max_mp = 100
        self.mp = 100
        SilenceMixin.__init__(self)

    def basic_attack(self, target):
        if self.is_silenced:
            self.add_log(f"{self.name} нема и не может атаковать!")
            return 0

        damage = self.intelligence + self.level
        target.take_damage(damage)
        return damage

    def use_skill(self, target):
        if self.is_silenced:
            self.add_log(f"{self.name} нема и не может использовать навык!")
            return 0

        if self.mp < 25:
            self.add_log(f"Недостаточно MP для использования навыка!")
            return 0

        self.mp -= 25
        self.add_log(f"{self.name} использует ВОДЯНОЙ ВИХРЬ!")

        # Наносит урон и накладывает яд
        damage = self.intelligence * 1.5
        crit_damage = self.calculate_crit(damage, 0.15)
        target.take_damage(crit_damage)

        poison = Poison(duration=3, damage=5)
        target.add_effect(poison)

        return crit_damage


class Healer(Character, SilenceMixin):
    """Класс лекаря-русалочки"""

    def __init__(self, name, level=1):
        super().__init__(name, level)
        self._strength = 8
        self._agility = 12
        self._intelligence = 20
        self.max_hp = 100
        self.hp = 100
        self.max_mp = 80
        self.mp = 80
        SilenceMixin.__init__(self)

    def basic_attack(self, target):
        if self.is_silenced:
            self.add_log(f"{self.name} нема и не может атаковать!")
            return 0

        damage = self.intelligence * 0.7
        target.take_damage(damage)
        return damage

    def use_skill(self, target):
        if self.is_silenced:
            self.add_log(f"{self.name} нема и не может использовать навык!")
            return 0

        if self.mp < 20:
            self.add_log(f"Недостаточно MP для использования навыка!")
            return 0

        self.mp -= 20
        self.add_log(f"{self.name} использует ЦЕЛЕБНЫЙ РОДНИК!")

        heal_amount = self.intelligence * 2 + self.level * 3
        actual_heal = target.heal(heal_amount)

        # Накладывает регенерацию
        regen = Regeneration(duration=2, heal_amount=10)
        target.add_effect(regen)

        return -actual_heal  # Отрицательное значение для обозначения лечения


class BossStrategy(ABC):
    """Абстрактная стратегия босса"""

    @abstractmethod
    def execute(self, boss, targets):
        pass


class AggressiveStrategy(BossStrategy):
    """Агрессивная стратегия"""

    def execute(self, boss, targets):
        boss.add_log("Урсула в ярости! Агрессивная атака!")
        # Атакует самого слабого персонажа
        weakest = min(targets, key=lambda x: x.hp)
        damage = boss.strength * 2
        weakest.take_damage(damage)
        return damage


class DefensiveStrategy(BossStrategy):
    """Защитная стратегия"""

    def execute(self, boss, targets):
        boss.add_log("Урсула защищается и лечится!")
        heal_amount = boss.intelligence * 1.5
        actual_heal = boss.heal(heal_amount)

        # Накладывает щит на себя
        shield = Shield(duration=2, shield_amount=30)
        boss.add_effect(shield)

        return -actual_heal


class DebuffStrategy(BossStrategy):
    """Стратегия наложения дебаффов"""

    def execute(self, boss, targets):
        boss.add_log("Урсула насылает проклятие!")
        for target in targets[:2]:  # Первым двум целям
            if target.is_alive:
                silence = Silence(duration=2)
                target.add_effect(silence)
        return 0


class Boss(Character, CritMixin):
    """Класс босса Урсулы"""

    def __init__(self, name="Урсула", level=10):
        super().__init__(name, level)
        self._strength = 30
        self._agility = 20
        self._intelligence = 25
        self.max_hp = 500
        self.hp = 500
        self.max_mp = 200
        self.mp = 200

        self.strategies = {
            'aggressive': AggressiveStrategy(),
            'defensive': DefensiveStrategy(),
            'debuff': DebuffStrategy()
        }
        self.current_strategy = 'aggressive'

    def basic_attack(self, target):
        damage = self.strength + self.level
        crit_damage = self.calculate_crit(damage, 0.25)
        target.take_damage(crit_damage)
        return crit_damage

    def use_skill(self, target):
        # Босс меняет стратегию в зависимости от HP
        if self.hp < self.max_hp * 0.3:  # Меньше 30% HP
            self.current_strategy = 'aggressive'
        elif self.hp < self.max_hp * 0.6:  # Меньше 60% HP
            self.current_strategy = 'debuff'
        else:
            self.current_strategy = 'defensive'

        strategy = self.strategies[self.current_strategy]
        return strategy.execute(self, [target] if target else [])

    @property
    def phase(self):
        if self.hp > self.max_hp * 0.7:
            return 1
        elif self.hp > self.max_hp * 0.4:
            return 2
        else:
            return 3