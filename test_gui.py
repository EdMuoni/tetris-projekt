import PySimpleGUI as sg

# Game board settings
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
CELL_SIZE = 20
WINDOW_WIDTH = BOARD_WIDTH * CELL_SIZE
WINDOW_HEIGHT = BOARD_HEIGHT * CELL_SIZE

# Colors
COLOR_EMPTY = 'black'
COLOR_BLOCK = 'blue'

# Simple demo: draws an empty board
layout = [
    [sg.Graph(canvas_size=(WINDOW_WIDTH, WINDOW_HEIGHT),
              graph_bottom_left=(0, WINDOW_HEIGHT),
              graph_top_right=(WINDOW_WIDTH, 0),
              background_color='black',
              key='graph')],
    [sg.Button('Exit')]
]

window = sg.Window("Tetris - demo", layout, finalize=True)
graph = window['graph']

# Draw empty game board
for y in range(BOARD_HEIGHT):
    for x in range(BOARD_WIDTH):
        x0 = x * CELL_SIZE
        y0 = y * CELL_SIZE
        x1 = x0 + CELL_SIZE
        y1 = y0 + CELL_SIZE
        graph.draw_rectangle((x0, y0), (x1, y1), line_color='gray', fill_color=COLOR_EMPTY)

# Main loop
while True:
    event, _ = window.read(timeout=100)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

window.close()