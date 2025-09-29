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
        self.boss = Boss("Тест-Босс")
        self.boss.hp = 50  # Уменьшаем HP для тестов

    def test_character_creation(self):
        self.assertEqual(self.warrior.name, "Тест-Воин")
        self.assertTrue(self.warrior.is_alive)
        self.assertEqual(self.warrior.level, 1)

    def test_basic_attack(self):
        initial_hp = self.boss.hp
        damage = self.warrior.basic_attack(self.boss)
        self.assertEqual(self.boss.hp, initial_hp - damage)

    def test_skill_usage(self):
        initial_mp = self.mage.mp
        self.mage.use_skill(self.boss)
        self.assertLess(self.mage.mp, initial_mp)

    def test_poison_effect(self):
        poison = Poison(duration=2, damage=5)
        initial_hp = self.boss.hp
        poison.apply(self.boss)
        self.assertEqual(self.boss.hp, initial_hp - 5)

    def test_boss_phase_transition(self):
        self.boss.hp = self.boss.max_hp * 0.8  # 80% HP
        self.assertEqual(self.boss.phase, 1)

        self.boss.hp = self.boss.max_hp * 0.5  # 50% HP
        self.assertEqual(self.boss.phase, 2)

        self.boss.hp = self.boss.max_hp * 0.2  # 20% HP
        self.assertEqual(self.boss.phase, 3)


if __name__ == '__main__':
    unittest.main()