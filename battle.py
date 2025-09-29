import random
import json
from mixins import LoggerMixin
from characters import Boss


class TurnOrder:

    def __init__(self, characters):
        self.characters = sorted(characters, key=lambda x: x.agility, reverse=True)
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.characters):
            self.index = 0
            raise StopIteration

        character = self.characters[self.index]
        self.index += 1
        return character


class Battle(LoggerMixin):

    def __init__(self, party, boss, seed=None):
        super().__init__()
        self.party = party
        self.boss = boss
        self.round = 0
        self.turn_order = None

        if seed is not None:
            random.seed(seed)

    def start_battle(self):
        self.add_log("=== НАЧАЛО БОЯ ===")
        self.add_log(f"Русалочки: {[m.name for m in self.party]} vs {self.boss.name}")

        while not self.is_battle_over():
            self.round += 1
            self.add_log(f"\n=== РАУНД {self.round} ===")
            self.execute_round()

        self.declare_winner()

    def execute_round(self):
        all_characters = [c for c in self.party if c.is_alive] + [self.boss]
        self.turn_order = TurnOrder(all_characters)

        for character in self.turn_order:
            if not character.is_alive:
                continue

            self.add_log(f"\n--- Ход {character.name} ---")
            character.update_effects()

            if isinstance(character, Boss):
                alive_party = [p for p in self.party if p.is_alive]
                if alive_party:
                    target = random.choice(alive_party)
                    if random.random() < 0.7:
                        character.use_skill(target)
                    else:
                        character.basic_attack(target)
            else:
                self.player_turn(character)

            if self.is_battle_over():
                break

    def player_turn(self, character):
        self.add_log(f"1. Базовая атака")
        self.add_log(f"2. Использовать навык (MP: {character.mp})")

        choice = random.randint(1, 2)

        if choice == 1 or character.mp < 10:
            character.basic_attack(self.boss)
        else:
            character.use_skill(self.boss)

    def is_battle_over(self):
        boss_dead = not self.boss.is_alive
        party_dead = all(not mermaid.is_alive for mermaid in self.party)
        return boss_dead or party_dead

    def declare_winner(self):
        if not self.boss.is_alive:
            self.add_log("🎉 ПОБЕДА! Русалочки победили Урсулу!")
        else:
            self.add_log("💀 ПОРАЖЕНИЕ! Урсула победила русалочек!")

    def save_state(self, filename):
        state = {
            'round': self.round,
            'party': [char.to_dict() for char in self.party],
            'boss': self.boss.to_dict(),
            'log': self.log
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

        self.add_log(f"Сохранение создано: {filename}")