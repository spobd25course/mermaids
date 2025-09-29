import unittest
import sys
import os

# Добавляем текущую директорию в путь для импорта
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from characters import Warrior, Mage, Healer, Boss
from battle import Battle
from effects import Poison


class TestBattle(unittest.TestCase):

    def setUp(self):
        self.warrior = Warrior("Тест-Воин")
        self.mage = Mage("Тест-Маг")
        self.healer = Healer("Тест-Лекарь")
        self.boss = Boss("Тест-Босс")
        self.boss.hp = 50  # Уменьшаем HP для тестов

    def test_character_creation(self):
        self.assertEqual(self.warrior.name, "Тест-Воин")
        self.assertTrue(self.warrior.is_alive)
        self.assertEqual(self.warrior.level, 1)
        self.assertEqual(self.warrior.max_hp, 150)

    def test_basic_attack(self):
        initial_hp = self.boss.hp
        damage = self.warrior.basic_attack(self.boss)
        self.assertGreater(damage, 0)
        self.assertEqual(self.boss.hp, initial_hp - damage)

    def test_skill_usage(self):
        initial_mp = self.mage.mp
        self.mage.use_skill(self.boss)
        self.assertLess(self.mage.mp, initial_mp)

    def test_healer_skill(self):
        # Проверяем лечение
        injured_warrior = Warrior("Раненый воин")
        injured_warrior.hp = 50  # Раненый персонаж
        initial_hp = injured_warrior.hp

        self.healer.use_skill(injured_warrior)
        self.assertGreater(injured_warrior.hp, initial_hp)

    def test_poison_effect(self):
        poison = Poison(duration=2, damage=5)
        initial_hp = self.boss.hp
        poison.apply(self.boss)
        self.assertEqual(self.boss.hp, initial_hp - 5)

    def test_boss_phase_transition(self):
        # Фаза 1
        self.boss.hp = self.boss.max_hp * 0.8  # 80% HP
        self.assertEqual(self.boss.phase, 1)

        # Фаза 2
        self.boss.hp = self.boss.max_hp * 0.5  # 50% HP
        self.assertEqual(self.boss.phase, 2)

        # Фаза 3
        self.boss.hp = self.boss.max_hp * 0.2  # 20% HP
        self.assertEqual(self.boss.phase, 3)

    def test_character_death(self):
        self.warrior.hp = 10
        self.warrior.take_damage(20)
        self.assertEqual(self.warrior.hp, 0)
        self.assertFalse(self.warrior.is_alive)

    def test_battle_creation(self):
        party = [self.warrior, self.mage, self.healer]
        battle = Battle(party, self.boss)
        self.assertEqual(len(battle.party), 3)
        self.assertEqual(battle.boss.name, "Тест-Босс")

    def test_turn_order(self):
        # Создаем персонажей с разной ловкостью
        fast_warrior = Warrior("Быстрый воин")
        fast_warrior._agility = 20

        slow_mage = Mage("Медленный маг")
        slow_mage._agility = 5

        characters = [slow_mage, fast_warrior]

        # Должны отсортироваться по убыванию ловкости
        from battle import TurnOrder
        turn_order = TurnOrder(characters)
        ordered = list(turn_order)

        self.assertEqual(ordered[0].name, "Быстрый воин")
        self.assertEqual(ordered[1].name, "Медленный маг")


if __name__ == '__main__':
    unittest.main(verbosity=2)