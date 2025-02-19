import tkinter as tk
from tkinter import messagebox
import random

# Создание окна
window = tk.Tk()
window.title("Крестики-нолики")
window.geometry("350x450")
window.configure(bg="black")

# Глобальные переменные
current_player = "X"
buttons = [[None for _ in range(3)] for _ in range(3)]
player_score = {"X": 0, "O": 0}
game_mode = None  # 'PvP' или 'PvC'
ai_symbol = "O"  # Символ компьютера
win_count = {"X": 0, "O": 0}

# Функции
def check_winner():
    """Проверка победителя"""
    for i in range(3):
        if buttons[i][0]["text"] == buttons[i][1]["text"] == buttons[i][2]["text"] != "":
            return buttons[i][0]["text"]
        if buttons[0][i]["text"] == buttons[1][i]["text"] == buttons[2][i]["text"] != "":
            return buttons[0][i]["text"]
    if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] != "":
        return buttons[0][0]["text"]
    if buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] != "":
        return buttons[0][2]["text"]
    return None

def check_draw():
    """Проверка ничьей"""
    for row in buttons:
        for btn in row:
            if btn["text"] == "":
                return False
    return True

def on_click(row, col):
    """Обработка клика на кнопку"""
    global current_player
    if buttons[row][col]['text'] != "" or game_mode is None:
        return

    # Игрок делает ход
    buttons[row][col]['text'] = current_player
    update_score()

    # Проверка победителя
    winner = check_winner()
    if winner:
        win_count[winner] += 1
        if win_count[winner] == 3:
            messagebox.showinfo("Игра окончена", f"Игрок {winner} выиграл серию!")
            reset_scores()
        else:
            messagebox.showinfo("Игра окончена", f"Игрок {winner} победил!")
        reset_board()
        return

    # Проверка ничьи
    if check_draw():
        messagebox.showinfo("Игра окончена", "Ничья!")
        reset_board()
        return

    # Ход компьютера (если PvC)
    if game_mode == "PvC":
        make_ai_move()
    else:  # PvP - меняем текущего игрока
        current_player = "O" if current_player == "X" else "X"

def make_ai_move():
    """Ход компьютера"""
    empty_cells = [(i, j) for i in range(3) for j in range(3) if buttons[i][j]["text"] == ""]
    if empty_cells:
        row, col = random.choice(empty_cells)
        buttons[row][col]["text"] = ai_symbol
        update_score()

        # Проверка победителя
        winner = check_winner()
        if winner:
            win_count[winner] += 1
            if win_count[winner] == 3:
                messagebox.showinfo("Игра окончена", f"Игрок {winner} выиграл серию!")
                reset_scores()
            else:
                messagebox.showinfo("Игра окончена", f"Игрок {winner} победил!")
            reset_board()

        # Проверка ничьи
        if check_draw():
            messagebox.showinfo("Игра окончена", "Ничья!")
            reset_board()

def reset_board():
    """Сброс игрового поля"""
    for row in buttons:
        for btn in row:
            btn["text"] = ""

def reset_scores():
    """Сброс счета"""
    global win_count
    win_count = {"X": 0, "O": 0}
    update_score()

def update_score():
    """Обновление счета"""
    score_label.config(text=f"Счет: X - {win_count['X']} | O - {win_count['O']}", fg="lime", bg="black", font=("Arial", 16))

def choose_game_mode(mode):
    """Выбор режима игры"""
    global game_mode, current_player
    game_mode = mode
    if mode == "PvC":
        symbol_choice_window()
    else:  # PvP
        current_player = "X"  # Начинает первый игрок с X

def symbol_choice_window():
    """Окно выбора символа для PvC"""
    def set_symbol(symbol):
        global current_player, ai_symbol
        current_player = symbol
        ai_symbol = "O" if symbol == "X" else "X"
        choice_window.destroy()

    choice_window = tk.Toplevel(window)
    choice_window.title("Выберите символ")
    choice_window.geometry("200x100")
    choice_window.configure(bg="black")

    tk.Label(choice_window, text="Выберите символ:", fg="lime", bg="black", font=("Arial", 12)).pack(pady=5)
    tk.Button(choice_window, text="X", command=lambda: set_symbol("X"), bg="yellow", fg="black", font=("Arial", 12)).pack(side=tk.LEFT, padx=10, pady=10)
    tk.Button(choice_window, text="O", command=lambda: set_symbol("O"), bg="yellow", fg="black", font=("Arial", 12)).pack(side=tk.RIGHT, padx=10, pady=10)

# Интерфейс
score_label = tk.Label(window, text="Счет: X - 0 | O - 0", fg="lime", bg="black", font=("Arial", 16))
score_label.grid(row=0, column=0, columnspan=3, pady=10)

for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(
            window,
            text="",
            font=("Arial", 20),
            width=5,
            height=2,
            bg="yellow",
            fg="lime",
            command=lambda r=i, c=j: on_click(r, c)
        )
        buttons[i][j].grid(row=i + 1, column=j, padx=5, pady=5)

reset_button = tk.Button(
    window,
    text="Новая игра",
    font=("Arial", 12),
    bg="red",
    fg="white",
    command=reset_board
)
reset_button.grid(row=4, column=0, columnspan=3, pady=10)

mode_frame = tk.Frame(window, bg="black")
mode_frame.grid(row=5, column=0, columnspan=3, pady=10)

tk.Button(
    mode_frame,
    text="Человек vs Человек",
    font=("Arial", 10),
    bg="yellow",
    fg="black",
    command=lambda: choose_game_mode("PvP")
).pack(side=tk.LEFT, padx=5)

tk.Button(
    mode_frame,
    text="Человек vs Компьютер",
    font=("Arial", 10),
    bg="yellow",
    fg="black",
    command=lambda: choose_game_mode("PvC")
).pack(side=tk.RIGHT, padx=5)

# Запуск приложения
window.mainloop()