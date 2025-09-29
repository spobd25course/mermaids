from characters import Warrior, Mage, Healer, Boss
from battle import Battle


def create_party():
    """Создание отряда русалочек"""
    party = [
        Warrior("Ариэль", 5),
        Mage("Андарина", 5),
        Healer("Марина", 5)
    ]
    return party


def main():
    print("🐠 МИНИ-ИГРА «РУСАЛОЧКИ ПРОТИВ УРСУЛЫ» 🐠")
    print("=" * 50)

    # Создание отряда и босса
    party = create_party()
    boss = Boss("Урсула", 10)

    # Вывод информации о команде
    print("\nВаш отряд:")
    for i, mermaid in enumerate(party, 1):
        print(f"{i}. {mermaid}")

    print(f"\nПротивник: {boss}")
    print(f"Фаза босса: {boss.phase}")

    # Начало боя
    input("\nНажмите Enter чтобы начать бой...")

    battle = Battle(party, boss, seed=42)

    try:
        battle.start_battle()

        # Сохранение результатов
        battle.save_state("battle_result.json")
        print(f"\nРезультаты боя сохранены в battle_result.json")

    except KeyboardInterrupt:
        print("\n\nБой прерван пользователем")
        battle.save_state("battle_interrupted.json")


if __name__ == "__main__":
    main()