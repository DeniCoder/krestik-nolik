import tkinter as tk
from tkinter import messagebox

# Настройки цветов
BACKGROUND_COLOR = 'black'
BUTTON_COLOR = 'yellow'
TEXT_COLOR = '#00FF00'  # Кислотный зеленый

# Начальные значения счета
player_x_score = 0
player_o_score = 0

# Состояние игры
game_mode = None  # Человек-человек или человек-компьютер
current_player = "X"
buttons = []
winner_message_shown = False  # Чтобы избежать повторного вывода сообщений

# Игра заканчивается, когда кто-то выигрывает 3 раза
max_wins = 3

# Глобальная переменная для выбранного символа
selected_symbol = None


def reset_game():
    """Очищаем игровое поле и начинаем новую игру."""
    global winner_message_shown, current_player

    # Очистка всех кнопок
    for row in buttons:
        for button in row:
            button['text'] = ''
            button.config(bg=BUTTON_COLOR)

    # Устанавливаем начального игрока
    current_player = "X"
    winner_message_shown = False


def show_winner(winner):
    """Показываем окно с победителем"""
    messagebox.showinfo("Победитель", f"Победил игрок '{winner}'! Поздравляем!")


def check_draw():
    """Проверяем, закончилось ли поле, но победитель не выявлен"""
    for row in buttons:
        for button in row:
            if button['text'] == '':
                return False
    return True


def check_winner():
    """Проверяет наличие победителя на поле"""
    global winner_message_shown

    # Проверка строк
    for i in range(3):
        if buttons[i][0]['text'] == buttons[i][1]['text'] == buttons[i][2]['text'] != '':
            show_winner(buttons[i][0]['text'])
            winner_message_shown = True
            return True

    # Проверка столбцов
    for i in range(3):
        if buttons[0][i]['text'] == buttons[1][i]['text'] == buttons[2][i]['text'] != '':
            show_winner(buttons[0][i]['text'])
            winner_message_shown = True
            return True

    # Диагонали
    if buttons[0][0]['text'] == buttons[1][1]['text'] == buttons[2][2]['text'] != '':
        show_winner(buttons[0][0]['text'])
        winner_message_shown = True
        return True
    elif buttons[0][2]['text'] == buttons[1][1]['text'] == buttons[2][0]['text'] != '':
        show_winner(buttons[0][2]['text'])
        winner_message_shown = True
        return True

    # Ничья
    if check_draw():
        messagebox.showinfo("Ничья", "Все клетки заполнены, но победителя нет.")
        winner_message_shown = True
        return True

    return False


def update_scores(winner):
    """Обновляет счет победителей"""
    global player_x_score, player_o_score
    if winner == 'X':
        player_x_score += 1
    elif winner == 'O':
        player_o_score += 1
    score_label.config(text=f"Счёт: X={player_x_score}, O={player_o_score}")


def game_over():
    """Завершаем игру, если один из игроков выиграл 3 раза"""
    global player_x_score, player_o_score
    if player_x_score >= max_wins or player_o_score >= max_wins:
        messagebox.showinfo("Игра окончена",
                            f"Игра окончена. Победил игрок {'X' if player_x_score > player_o_score else 'O'}!")
        reset_game()


def on_click(row, col):
    """Обработчик нажатия на клетку"""
    global current_player

    # Игнорируем клики, если уже определился победитель
    if winner_message_shown:
        return

    # Проверяем, пуста ли ячейка
    if buttons[row][col]['text'] != '':
        return

    # Заполняем ячейку текущим игроком
    buttons[row][col]['text'] = current_player
    buttons[row][col].config(bg='green')  # Изменение фона клетки

    # Проверяем состояние игры
    if check_winner():
        update_scores(current_player)
        game_over()

    # Меняем текущего игрока
    current_player = 'O' if current_player == 'X' else 'X'


def select_symbol():
    """Окно выбора символа для игрока"""
    global selected_symbol  # Глобальное объявление

    def set_symbol(symbol):
        global selected_symbol  # Используем глобальную переменную
        selected_symbol = symbol
        selection_window.destroy()

    selection_window = tk.Toplevel(window)
    selection_window.title('Выберите символ')
    selection_window.geometry('300x200')

    label = tk.Label(selection_window, text="Выберите символ:", fg=TEXT_COLOR, bg=BACKGROUND_COLOR)
    label.pack(pady=(10, 0))

    x_button = tk.Button(selection_window, text='X', command=lambda: set_symbol('X'), bg=BUTTON_COLOR, fg=TEXT_COLOR)
    o_button = tk.Button(selection_window, text='O', command=lambda: set_symbol('O'), bg=BUTTON_COLOR, fg=TEXT_COLOR)

    x_button.pack(pady=(10, 5))
    o_button.pack(pady=(5, 10))

    # Ждем закрытия окна
    selection_window.wait_window()
    print(f"Выбранный символ: {selected_symbol}")  # Для отладки


def start_new_game():
    """Запуск новой партии"""
    global current_player, player_x_score, player_o_score, winner_message_shown

    reset_game()
    select_symbol()


# Создание главного окна
window = tk.Tk()
window.title("Крестики-нолики")
window.geometry("600x650")
window.configure(background=BACKGROUND_COLOR)

# Добавление кнопки "Начать заново"
reset_button = tk.Button(window, text="Начать заново", command=start_new_game, bg=BUTTON_COLOR, fg=TEXT_COLOR)
reset_button.grid(row=3, column=0, padx=5, pady=5)

# Отображение счета
score_label = tk.Label(window, text=f"Счёт: X={player_x_score}, O={player_o_score}", fg=TEXT_COLOR, bg=BACKGROUND_COLOR)
score_label.grid(row=0, column=3, padx=5, pady=5)

# Генерация игрового поля
for i in range(3):
    row = []
    for j in range(3):
        btn = tk.Button(window, text='', font=("Arial", 30), width=5, height=2, command=lambda r=i, c=j: on_click(r, c),
                        bg=BUTTON_COLOR, fg=TEXT_COLOR)
        btn.grid(row=i, column=j, padx=5, pady=5)
        row.append(btn)
    buttons.append(row)

start_new_game()  # Начинаем игру сразу после запуска

window.mainloop()