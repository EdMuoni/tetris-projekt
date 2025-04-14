import PySimpleGUI as sg
import random
import time

BOARD_WIDTH = 10
BOARD_HEIGHT = 20
NORMAL_TICK = 300
FAST_TICK = 50

TETROMINOES = {
    'O': [[1, 1], [1, 1]],
    'I': [[1, 1, 1, 1]],
    'T': [[0, 1, 0], [1, 1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'Z': [[1, 1, 0], [0, 1, 1]],
    'J': [[1, 0, 0], [1, 1, 1]],
    'L': [[0, 0, 1], [1, 1, 1]],
}

def create_board():
    return [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

def draw_board(window, board, score):
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            color = 'black' if board[y][x] == 0 else 'blue'
            window[(x, y)].update(button_color=('white', color))
    window["score_text"].update(f"Score: {score}")

def place_shape(board, shape, pos, value):
    sx, sy = pos
    for dy, row in enumerate(shape):
        for dx, val in enumerate(row):
            if val and 0 <= sy+dy < BOARD_HEIGHT and 0 <= sx+dx < BOARD_WIDTH:
                board[sy+dy][sx+dx] = value

def is_valid(board, shape, pos):
    sx, sy = pos
    for dy, row in enumerate(shape):
        for dx, val in enumerate(row):
            if val:
                x = sx + dx
                y = sy + dy
                if x < 0 or x >= BOARD_WIDTH or y >= BOARD_HEIGHT:
                    return False
                if y >= 0 and board[y][x] == 1:
                    return False
    return True

def clear_lines(board):
    new_board = [row for row in board if any(cell == 0 for cell in row)]
    lines_cleared = BOARD_HEIGHT - len(new_board)
    while len(new_board) < BOARD_HEIGHT:
        new_board.insert(0, [0] * BOARD_WIDTH)
    return new_board, lines_cleared

def rotate(shape):
    return [list(row)[::-1] for row in zip(*shape)]

def run_tetris():
    board = create_board()
    layout = [
        [sg.Button('', size=(2, 1), pad=(0, 0), key=(x, y)) for x in range(BOARD_WIDTH)]
        for y in range(BOARD_HEIGHT)
    ]
    layout.append([sg.Text("Score: 0", key="score_text"), sg.Button('Exit')])
    window = sg.Window('Tetris', layout, return_keyboard_events=True, finalize=True)

    shape = random.choice(list(TETROMINOES.values()))
    pos = [BOARD_WIDTH // 2 - len(shape[0]) // 2, 0]
    score = 0
    last_tick = time.time()
    fast_mode = False

    while True:
        event, values = window.read(timeout=10)
        now = time.time()

        # Check for speed key
        if event == 'space:32':
            fast_mode = True
        elif isinstance(event, str) and event.startswith('space:') is False:
            fast_mode = False

        current_tick = FAST_TICK if fast_mode else NORMAL_TICK

        if now - last_tick > current_tick / 1000:
            place_shape(board, shape, pos, 0)
            new_pos = [pos[0], pos[1] + 1]
            if is_valid(board, shape, new_pos):
                pos = new_pos
            else:
                place_shape(board, shape, pos, 1)
                board, cleared = clear_lines(board)
                score += cleared * 100
                shape = random.choice(list(TETROMINOES.values()))
                pos = [BOARD_WIDTH // 2 - len(shape[0]) // 2, 0]
                if not is_valid(board, shape, pos):
                    sg.popup("Game Over!", title="Tetris")
                    break
            place_shape(board, shape, pos, 1)
            draw_board(window, board, score)
            last_tick = now

        if event in (sg.WINDOW_CLOSED, 'Exit'):
            break
        elif event == 'Left:37':
            place_shape(board, shape, pos, 0)
            new_pos = [pos[0] - 1, pos[1]]
            if is_valid(board, shape, new_pos):
                pos = new_pos
            place_shape(board, shape, pos, 1)
            draw_board(window, board, score)
        elif event == 'Right:39':
            place_shape(board, shape, pos, 0)
            new_pos = [pos[0] + 1, pos[1]]
            if is_valid(board, shape, new_pos):
                pos = new_pos
            place_shape(board, shape, pos, 1)
            draw_board(window, board, score)
        elif event == 'Up:38':
            place_shape(board, shape, pos, 0)
            rotated = rotate(shape)
            if is_valid(board, rotated, pos):
                shape = rotated
            place_shape(board, shape, pos, 1)
            draw_board(window, board, score)

    window.close()

run_tetris()