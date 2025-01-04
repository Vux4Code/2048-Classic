import pygame
from sys import exit
import random
import math

pygame. init ()

scale_factor = 5
game_active = True
win = True
board_size = 4
num_block_type = 12

file_data = 'data.txt'

pos_score = 0
max_score = 0

with open (file_data, 'r') as file :
    max_score = int(file. read ())
clock = pygame. time. Clock ()

font_size = 40
font = pygame. font. Font ('Font/Pixeltype.ttf', 40)

screen = pygame. display. set_mode ((10, 10))

title_surf = pygame. image. load ('Image/title.png')
title_surf = pygame. transform. scale (title_surf, (title_surf. get_width() * scale_factor, title_surf. get_height() * scale_factor)). convert_alpha ()
title_rect = title_surf. get_rect (topleft = (0, 0))

board_surf = pygame. image. load ('Image/board.png')
board_surf = pygame. transform. scale (board_surf, (board_surf. get_width() * scale_factor, board_surf. get_height() * scale_factor)). convert_alpha ()
board_rect = board_surf. get_rect (topleft = (0, title_rect. bottom))

blocks = []
for i in range (num_block_type) :
    tmp = pygame. image. load (f'Image/block/{i}.png')
    tmp = pygame. transform. scale (tmp, (tmp. get_width() * scale_factor, tmp. get_height() * scale_factor)). convert_alpha()
    blocks. append (tmp)
del tmp

reload_surf = pygame. image. load ('Image/reload.png')
reload_surf = pygame. transform. scale (reload_surf, (reload_surf. get_width () * scale_factor, reload_surf. get_height () * scale_factor)). convert_alpha()
reload_rect = reload_surf. get_rect (center = board_rect. center)

congra_surf = font. render ('Congratulation !', False, 'red')
congra_rect = congra_surf. get_rect (center = board_rect. center)
congra_rect. bottom -= blocks [0]. get_height()

troll_surf = font. render ('Youre black n*gga !', False, 'black')
troll_rect = congra_surf. get_rect (center = board_rect. center)
troll_rect. bottom += blocks [0]. get_height()

back2_surf = pygame. image. load ('Image/back2.png')
back2_surf = pygame. transform. scale (back2_surf, (back2_surf. get_width() * scale_factor, back2_surf. get_height() * scale_factor)). convert_alpha ()
back2_rect = back2_surf. get_rect (topleft = (0, title_rect. bottom))

screen = pygame. display. set_mode (board_rect. bottomright)

def get_pos (pos) :
    return ((board_rect.left + 1 * scale_factor * (pos[0] + 1) + blocks[0].get_width() * pos[0]),
            (board_rect.top + 1 * scale_factor * (pos[1] + 1) + blocks[0].get_height() * pos[1]))

def rotate_cell (pos) :
    return (board_size - 1 - pos [1], pos [0])

class Cell () :
    def __init__ (self) :
        super (). __init__ ()
        self. type = 0
        self. merge = False
        self. move = False
        self. moving = 0
    def print (self, pos) :
        screen. blit (blocks [self. type], get_pos (pos))
cells = [[Cell () for i in range (board_size)] for j in range (board_size)]

num_frame = 3
class Move () :
    def __init__ (self, st, en, type) :
        super (). __init__ ()
        self. start = st
        self. end = en
        self. type = type
        self. frame = 0
    def print (self) :
        st_pos = get_pos (self. start)
        en_pos = get_pos (self. end)
        pos = ((en_pos [0] * self. frame + st_pos [0] * (num_frame - self. frame)) / num_frame,
               (en_pos [1] * self. frame + st_pos [1] * (num_frame - self. frame)) / num_frame)
        self. frame += 1
        screen. blit (blocks [self. type], pos)
def rotate_move (pos) :
    return Move(rotate_cell(pos.start), rotate_cell(pos.end), pos.type)
moves = []

pygame. display. set_caption ('Classic 2048 by Vux2Code')
pygame. display. set_icon (pygame. image. load ('Image/icon.png'). convert_alpha())

score_text_size = 40
score_text_font = pygame. font. Font ('Font/Pixeltype.ttf', score_text_size)

def print_score () :
    pos_score_text = font. render (f'Score : {pos_score}', False, 'black')
    pos_score_rect = pos_score_text. get_rect (bottomleft = title_rect. center)
    pos_score_rect. bottom -= (3 * scale_factor)
    max_score_text = font.render(f'Max : {max_score}', False, 'red')
    max_score_rect = max_score_text.get_rect(bottomleft=title_rect.midbottom)
    max_score_rect.bottom -= (3 * scale_factor)
    screen. blit (pos_score_text, pos_score_rect)
    screen. blit (max_score_text, max_score_rect)

def spawn_cell () :
    global cells
    empty_cell = []
    for i in range (board_size) :
        for j in range (board_size) :
            if cells [i] [j]. type == 0 :
                empty_cell. append ((i, j))
    if len (empty_cell) == 0 : return
    new_cell = random. randrange (0, len (empty_cell))
    new_cell_type = random. randrange (0, 10)
    if new_cell_type == 0 : cells [empty_cell [new_cell] [0]] [empty_cell [new_cell] [1]]. type = 2
    else : cells [empty_cell [new_cell] [0]] [empty_cell [new_cell] [1]]. type = 1

def reset () :
    global cells, game_active, pos_score, moves
    cells = [[Cell() for i in range(board_size)] for j in range(board_size)]
    moves = []
    game_active = True
    pos_score = 0
    spawn_cell ();
    spawn_cell ();

def rotate_clockwise () :
    global cells, moves
    new_cells = [[Cell() for i in range(board_size)] for j in range(board_size)]
    for i in range (board_size) :
        for j in range (board_size) :
            new_cells [i] [j] = cells [j] [board_size - 1 - i]
    cells = new_cells
    moves = [rotate_move(i) for i in moves]

def up () :
    global cells, pos_score, max_score, moves
    for i in range (board_size) :
        for j in range (board_size) :
            cells [i] [j]. merge = False
            cells [i] [j]. move = False
    for i in range (board_size) :
        for j in range (board_size) :
            if cells [i] [j]. type == 0 : continue
            pos = j
            if pos > 0 and cells [i] [pos - 1]. type == 0 :
                cells [i] [j]. move = True
            while pos > 0 and cells [i] [pos - 1]. type == 0 :
                cells [i] [pos - 1], cells [i] [pos] = cells [i] [pos], cells [i] [pos - 1]
                pos -= 1
            if pos > 0 and cells [i] [pos - 1]. type == cells [i] [pos]. type and cells [i] [pos - 1]. merge == False :
                cells [i] [pos - 1]. moving += 1
                moves. append (Move ((i, j), (i, pos - 1), cells [i] [pos]. type))
                cells [i] [pos - 1]. type += 1
                cells [i] [pos - 1]. merge = True
                cells [i] [pos] = Cell ()
                pos_score += pow (2, cells [i] [pos - 1]. type)
            else :
                cells [i] [pos]. moving += 1
                moves. append (Move((i, j), (i, pos), cells [i] [pos]. type))
    max_score = max (max_score, pos_score)

def left () :
    rotate_clockwise()
    up ()
    rotate_clockwise()
    rotate_clockwise()
    rotate_clockwise()

def down () :
    rotate_clockwise()
    rotate_clockwise()
    up ()
    rotate_clockwise()
    rotate_clockwise()

def right () :
    rotate_clockwise()
    rotate_clockwise()
    rotate_clockwise()
    up ()
    rotate_clockwise()

def check_diff () :
    global cells
    diff = False
    for i in range (board_size) :
        for j in range (board_size) :
            if cells [i] [j]. type == 0 : continue
            if cells [i] [j]. move == True or cells [i] [j]. merge == True :
                diff = True
    return diff

def update_after_key () :
    if check_diff() :
        spawn_cell()

def update_after_frame () :
    global game_active, win, moves
    game_active = False
    win = False
    for i in range (board_size) :
        for j in range (board_size) :
            if cells [i] [j]. type == 11 : win = True
            if cells [i] [j]. type == 0 : game_active = True
            if j + 1 < board_size and cells [i] [j]. type == cells [i] [j + 1]. type : game_active = True
            if i + 1 < board_size and cells [i] [j]. type == cells [i + 1] [j]. type : game_active = True
    while len (moves) > 0 and moves [0]. frame == num_frame :
        cells [moves [0]. end [0]] [moves [0]. end [1]]. moving -= 1
        moves. pop (0)


def save_data () :
    with open (file_data, 'w') as file :
        file. write (str (max_score))

# ----- MAIN -----

reset()
while True:
    if game_active :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_data ()
                pygame.quit()
                exit()
            elif event.type == pygame. KEYDOWN :
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    up()
                    update_after_key()
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    left()
                    update_after_key()
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    down()
                    update_after_key()
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    right()
                    update_after_key()
        screen. fill ('white')
        screen. blit (title_surf, title_rect)
        screen. blit (board_surf, board_rect)
        print_score()
        for i in range (board_size) :
            for j in range (board_size) :
                if cells [i] [j]. type == 0 or cells [i] [j]. moving > 0: continue
                cells [i] [j]. print ((i, j))
        for i in range (len (moves)) : moves [i] . print ()
        update_after_frame()
    else :
        for event in pygame. event. get () :
            if event. type == pygame. QUIT :
                save_data ()
                pygame. quit ()
                exit ()
            elif event. type == pygame. KEYDOWN and event. key == pygame. K_SPACE : reset ()
            elif event. type == pygame. MOUSEBUTTONDOWN and reload_rect. collidepoint (event. pos) : reset ()
        screen. fill ('white')
        screen. blit (title_surf, title_rect)
        print_score()
        screen. blit (back2_surf, back2_rect)
        screen. blit (reload_surf, reload_rect)
        if win == True :
            screen. blit (congra_surf, congra_rect)
            screen. blit (troll_surf, troll_rect)

    pygame. display. update ()
    clock. tick (60)