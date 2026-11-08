import random

def monte_carlo(num_rolls=1_000_000, seed=None):
    """Повертає частоти та ймовірності сум 2–12.
    seed дозволяє відтворити симуляцію. Час: O(num_rolls), пам'ять: O(1).
    """
    if type(num_rolls) is not int or num_rolls <= 0:
        raise ValueError("Кількість кидків має бути додатним цілим числом.")
    rng = random.Random(seed)
    counts = {total: 0 for total in range(2, 13)}
    for _ in range(num_rolls):
        total = rng.randint(1, 6) + rng.randint(1, 6)
        counts[total] += 1
    probabilities = {
        total: count / num_rolls for total, count in counts.items()
    }
    return counts, probabilities

def analytical_probabilities():
    """Серед 36 рівноймовірних пар сума s має 6 - abs(7 - s) пар."""
    return {total: (6 - abs(7 - total)) / 36 for total in range(2, 13)}

def main():
    num_rolls = 1_000_000
    counts, simulated = monte_carlo(num_rolls, seed=42)
    analytical = analytical_probabilities()
    print(f"Кількість кидків: {num_rolls:,}; seed: 42\n")
    print("| Сума | Кількість | Монте-Карло | Аналітична | Різниця, в.п. |")
    print("| ---- | --------- | ----------- | ---------- | ------------- |")
    for total in range(2, 13):
        difference = (simulated[total] - analytical[total]) * 100
        print(
            f"| {total:4} | {counts[total]:9} | {simulated[total]:10.4%} "
            f"| {analytical[total]:9.4%} | {difference:+13.4f} |"
        )

if __name__ == "__main__":
    main()
