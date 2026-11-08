items = {
    "pizza": {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog": {"cost": 30, "calories": 200},
    "pepsi": {"cost": 10, "calories": 100},
    "cola": {"cost": 15, "calories": 220},
    "potato": {"cost": 25, "calories": 350},
}

def validate_inputs(items, budget):
    """Бюджет і ціни — цілі числа; калорійність невід'ємна."""
    if type(budget) is not int or budget < 0:
        raise ValueError("Бюджет має бути невід'ємним цілим числом.")
    for food in items.values():
        if type(food["cost"]) is not int or food["cost"] <= 0:
            raise ValueError("Вартість страви має бути додатним цілим числом.")
        if food["calories"] < 0:
            raise ValueError("Калорійність не може бути від'ємною.")

def greedy_algorithm(items, budget):
    """Повертає список страв за спаданням calories/cost.
    Час: O(n log n), пам'ять: O(n). Оптимальність не гарантована.
    """
    validate_inputs(items, budget)
    ranked_items = sorted(
        items, key=lambda name: items[name]["calories"] / items[name]["cost"],
        reverse=True,
    )
    selected = []
    remaining = budget
    for name in ranked_items:
        if items[name]["cost"] <= remaining:
            selected.append(name)
            remaining -= items[name]["cost"]
    return selected

def dynamic_programming(items, budget):
    """Повертає оптимальний список страв для задачі рюкзака 0/1.
    Час і пам'ять: O(n * budget). Таблиця дозволяє відновити вибір.
    """
    validate_inputs(items, budget)
    names = list(items)
    dp = [[0] * (budget + 1) for _ in range(len(names) + 1)]
    for index, name in enumerate(names, start=1):
        cost = items[name]["cost"]
        calories = items[name]["calories"]
        for capacity in range(budget + 1):
            dp[index][capacity] = dp[index - 1][capacity]
            if cost <= capacity:
                dp[index][capacity] = max(
                    dp[index][capacity],
                    dp[index - 1][capacity - cost] + calories,
                )

    selected = []
    remaining = budget
    for index in range(len(names), 0, -1):
        if dp[index][remaining] != dp[index - 1][remaining]:
            name = names[index - 1]
            selected.append(name)
            remaining -= items[name]["cost"]
    selected.reverse()
    return selected

def main():
    budget = 100
    print(f"Бюджет: {budget}")
    for label, algorithm in (
        ("Жадібний алгоритм", greedy_algorithm),
        ("Динамічне програмування", dynamic_programming),
    ):
        selected = algorithm(items, budget)
        cost = sum(items[name]["cost"] for name in selected)
        calories = sum(items[name]["calories"] for name in selected)
        print(f"{label}: {', '.join(selected)}")
        print(f"  Вартість: {cost}; калорійність: {calories}")

if __name__ == "__main__":
    main()
