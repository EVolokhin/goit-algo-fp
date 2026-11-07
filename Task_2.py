import turtle

MAX_DEPTH = 12

def draw_pythagoras_tree(pen, origin, side, depth):
    """Малює квадрат і два дочірні квадрати на катетах трикутника.

    origin — нижня ліва вершина, side — вектор нижньої сторони.
    depth = 0 завершує рекурсію; depth = 1 малює лише один квадрат.
    """
    if depth <= 0:
        return

    x, y = origin
    dx, dy = side
    bottom_right = (x + dx, y + dy)
    top_left = (x - dy, y + dx)
    top_right = (x + dx - dy, y + dy + dx)

    pen.fillcolor("forestgreen" if depth <= 3 else "saddlebrown")
    pen.penup()
    pen.goto(origin)
    pen.pendown()
    pen.begin_fill()
    for vertex in (bottom_right, top_right, top_left, origin):
        pen.goto(vertex)
    pen.end_fill()

    # Прямокутний рівнобедрений трикутник над верхньою стороною.
    peak = (top_left[0] + (dx - dy) / 2,
            top_left[1] + (dy + dx) / 2)
    left_side = (peak[0] - top_left[0], peak[1] - top_left[1])
    right_side = (top_right[0] - peak[0], top_right[1] - peak[1])

    draw_pythagoras_tree(pen, top_left, left_side, depth - 1)
    draw_pythagoras_tree(pen, peak, right_side, depth - 1)

def read_depth():
    """Запитує цілий рівень; межа обмежує кількість квадратів до 4095."""
    while True:
        try:
            depth = int(input(f"Введіть рівень рекурсії (1–{MAX_DEPTH}): "))
        except ValueError:
            print("Введіть ціле число.")
            continue
        if 1 <= depth <= MAX_DEPTH:
            return depth
        print(f"Рівень має бути від 1 до {MAX_DEPTH}.")

def main():
    depth = read_depth()
    screen = turtle.Screen()
    screen.setup(width=1000, height=800)
    screen.setworldcoordinates(-450, -100, 550, 700)
    screen.title(f"Дерево Піфагора — рівень рекурсії {depth}")
    screen.bgcolor("white")
    screen.tracer(0)

    pen = turtle.Turtle(visible=False)
    pen.speed(0)
    pen.pencolor("darkgreen")
    draw_pythagoras_tree(pen, (0, 0), (100, 0), depth)

    screen.update()
    screen.mainloop()

if __name__ == "__main__":
    main()
