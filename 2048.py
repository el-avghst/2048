import random
import os
import numpy as np


def start():
    grid = [[0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]]
    add_2(grid)
    print('Для игры используйте клавиши WASD:')
    print('W для движения вверх')
    print('S для движения вниз')
    print('A для движения влево')
    print('D для движения вправо')
    print('Чтобы остановить игру, введите команду "end".')
    print(np.array(grid))
    return grid

def status(grid):
    print(np.array(grid))
    empty_cells = False
    unmerged_cells = False
    game_lost = False
    game_won = False
    for i in range(4):
        for j in range(4):
            if grid[i][j] == 2048:
                game_won = True
            if grid[i][j] == 0:
                empty_cells = True
    for i in range(4):
        for j in range(3):
            if grid[i][j] == grid[i][j + 1]:
                unmerged_cells = True
    for i in range(3):
        for j in range(4):
            if grid[i][j] == grid[i + 1][j]:
                unmerged_cells = True
    if game_won:
        print("Вы выиграли!!!")
    elif not empty_cells and not unmerged_cells:
        game_lost = True
        print("Вы проиграли :(")
    else:
        print("Следующий ход:")
    return game_won, game_lost

def add_2(grid):
    empty_cells = False
    for i in range(4):
        for j in range(4):
            if grid[i][j] == 0:
                empty_cells = True
    if empty_cells:
        row = random.randint(0, 3)
        column = random.randint(0, 3)
        while grid[row][column] != 0:
            row = random.randint(0, 3)
            column = random.randint(0, 3)
        grid[row][column] = 2
    else:
        print('Попробуйте другой ход')

def move_left(grid):
    for i in range(4):
        for j in range(1, 4):
            if grid[i][j] != 0 and grid[i][j - 1] == 0:
                grid[i][j - 1] = grid[i][j]
                grid[i][j] = 0
    return grid

def merge_left(grid):
    for i in range(4):
        for j in range(1, 4):
            if grid[i][j] == grid[i][j - 1] and grid[i][j] != 0:
                grid[i][j - 1] = grid[i][j] * 2
                grid[i][j] = 0
                p = grid[i][j - 1]
                add_points(p)
    return grid

def move_right(grid):
    for i in range(4):
        for j in range(0, 3):
            if grid[i][j] != 0 and grid[i][j + 1] == 0:
                grid[i][j + 1] = grid[i][j]
                grid[i][j] = 0
    return grid

def merge_right(grid):
    for i in range(4):
        for j in range(3, 0, -1):
            if grid[i][j] == grid[i][j - 1] and grid[i][j] != 0:
                grid[i][j] = grid[i][j - 1] * 2
                grid[i][j - 1] = 0
                p = grid[i][j]
                add_points(p)
    return grid

def move_up(grid):
    for i in range(1, 4):
        for j in range(4):
            if grid[i][j] != 0 and grid[i - 1][j] == 0:
                grid[i - 1][j] = grid[i][j]
                grid[i][j] = 0
    return grid

def merge_up(grid):
    for i in range(1, 4):
        for j in range(4):
            if grid[i][j] == grid[i - 1][j] and grid[i][j] != 0:
                grid[i - 1][j] = grid[i][j] * 2
                grid[i][j] = 0
                p = grid[i - 1][j]
                add_points(p)
    return grid

def move_down(grid):
    for i in range(0, 3):
        for j in range(4):
            if grid[i][j] != 0 and grid[i + 1][j] == 0:
                grid[i + 1][j] = grid[i][j]
                grid[i][j] = 0
    return grid

def merge_down(grid):
    for i in range(3, 0, -1):
        for j in range(4):
            if grid[i][j] == grid[i - 1][j] and grid[i][j] != 0:
                grid[i][j] = grid[i - 1][j] * 2
                grid[i - 1][j] = 0
                p = grid[i][j]
                add_points(p)
    return grid

def take_step(grid, command):
    stop = False
    if command in ['a', 'A', 'ф', 'Ф']:
        for k in range(3):
            move_left(grid)
        merge_left(grid)
        for k in range(2):
            move_left(grid)
        add_2(grid)
    elif command in ['d', 'D', 'в', 'В']:
        for k in range(3):
            move_right(grid)
        merge_right(grid)
        for k in range(2):
            move_right(grid)
        add_2(grid)
    elif command in ['w', 'W', 'ц', 'Ц']:
        for k in range(3):
            move_up(grid)
        merge_up(grid)
        for k in range(2):
            move_up(grid)
        add_2(grid)
    elif command in ['s', 'S', 'ы', 'Ы']:
        for k in range(3):
            move_down(grid)
        merge_down(grid)
        for k in range(2):
            move_down(grid)
        add_2(grid)
    elif command == 'end':
        print('Вы остановили игру.')
        stop = True
    else:
        print('Неверная команда')
    return grid, stop

def add_points(p):
    if os.path.exists('current.txt'):
        with open('current.txt', 'r') as f:
            current = f.read()
    else:
        current = '0'
    current = str(int(current) + p)
    with open('current.txt', 'w') as f:
        f.writelines(current)
    return current

def end_game():
    new_score = add_points(0)
    if os.path.exists('best.txt'):
        with open('best.txt', 'r') as f:
            best_score = f.read()
    if not os.path.exists('best.txt') or int(new_score) > int(best_score):
        best_score = new_score
        with open('best.txt', 'w') as f:
            f.write(new_score)
    print('Ваш результат:', new_score)
    print('Лучший результат:', best_score)
    with open('current.txt', 'w') as f:
        f.write('0')

def play_game():
    grid = start()
    while True:
        command_input = input()
        grid, stop_game = take_step(grid, command_input)
        if stop_game:
            with open('current.txt', 'w') as f:
                f.write('0')
            break
        win, lose = status(grid)
        if win or lose:
            end_game()
            print('Хотите сыграть еще? Если да, нажмите клавишу Y. Чтобы завершить программу, нажмите любую другую клавишу.')
            again = input()
            return again

play_again = play_game()
while play_again in ['y', 'Y', 'н', 'Н']:
    play_game()