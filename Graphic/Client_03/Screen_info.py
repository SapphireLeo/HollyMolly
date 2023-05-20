# define color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREY = (190, 190, 190)

# define the size of total screen
screen_size_x = 700
screen_size_y = 700
screen_size = (screen_size_x, screen_size_y)

# define the position of card of each player.
board_display_grid = []
for i in range(4):
    board_display_grid.append({})

y_margin = 65
x_margin = 65
board_size = ((0, 700), (0, 700))

board_display_grid[0] = {
    'private': {'x': sum(board_size[0]) / 2,
                'y': board_size[1][0] + y_margin},
    'public': {'image_set': [],
               'x': sum(board_size[0]) / 2,
               'y': board_size[1][0] + y_margin * 3}}

board_display_grid[1] = {
    'private': {'image_set': [],
                'x': board_size[0][1] - x_margin,
                'y': sum(board_size[1]) / 2},
    'public': {'image_set': [],
               'x': board_size[0][1] - x_margin * 3,
               'y': sum(board_size[1]) / 2}}

board_display_grid[2] = {
    'private': {'image_set': [],
                'x': sum(board_size[0]) / 2,
                'y': board_size[1][1] - y_margin},
    'public': {'image_set': [],
               'x': sum(board_size[0]) / 2,
               'y': board_size[1][1] - y_margin * 3}}

board_display_grid[3] = {
    'private': {'image_set': [],
                'x': board_size[0][0] + x_margin,
                'y': sum(board_size[1]) / 2},
    'public': {'image_set': [],
               'x': board_size[0][0] + x_margin * 3,
               'y': sum(board_size[1]) / 2}}

move_dest = []
for i in range(4):
    move_dest.append({
        'x': sum(board_size[0]) / 2,
        'y': sum(board_size[1]) / 2
    })
move_dest[0]['y'] = board_size[1][0] - y_margin
move_dest[2]['y'] = board_size[1][1] + y_margin
move_dest[1]['x'] = board_size[0][1] + x_margin
move_dest[3]['x'] = board_size[0][0] - x_margin

spare_grid = {
    'x': board_size[0][0] + x_margin,
    'y': board_size[1][1] - y_margin
}
spare_dest = {
    'x': board_size[0][0] - x_margin,
    'y': board_size[1][1] + y_margin
}

text_display_grid = []
for i in range(4):
    text_display_grid.append({})
text_margin_content = 65
text_margin_title_x = 125
text_margin_title_y = 80

text_display_grid[0] = {
    'title': {'x': board_display_grid[0]['private']['x'] + text_margin_title_x,
              'y': board_display_grid[0]['private']['y']},
    'private': {'x': board_display_grid[0]['private']['x'] - text_margin_content,
                'y': board_display_grid[0]['private']['y']},
    'public': {'x': board_display_grid[0]['public']['x'] - text_margin_content,
               'y': board_display_grid[0]['public']['y']}
}

text_display_grid[1] = {
    'title': {'x': board_display_grid[1]['private']['x'],
              'y': board_display_grid[1]['private']['y'] + text_margin_title_y},
    'private': {'x': board_display_grid[1]['private']['x'],
                'y': board_display_grid[1]['private']['y'] - text_margin_content},
    'public': {'x': board_display_grid[1]['public']['x'],
               'y': board_display_grid[1]['public']['y'] - text_margin_content}
}

text_display_grid[2] = {
    'title': {'x': board_display_grid[2]['private']['x'] + text_margin_title_x,
              'y': board_display_grid[2]['private']['y']},
    'private': {'x': board_display_grid[2]['private']['x'] - text_margin_content,
                'y': board_display_grid[2]['private']['y']},
    'public': {'x': board_display_grid[2]['public']['x'] - text_margin_content,
               'y': board_display_grid[2]['public']['y']}
}

text_display_grid[3] = {
    'title': {'x': board_display_grid[3]['private']['x'],
              'y': board_display_grid[3]['private']['y'] + text_margin_title_y},
    'private': {'x': board_display_grid[3]['private']['x'],
                'y': board_display_grid[3]['private']['y'] - text_margin_content},
    'public': {'x': board_display_grid[3]['public']['x'],
               'y': board_display_grid[3]['public']['y'] - text_margin_content}
}

image_display_grid = []
for i in range(4):
    image_display_grid.append({})
image_margin_content = 65
image_margin_title_x = 150
image_margin_title_y = 150

image_display_grid[0] = {
    'title': {'x': sum(board_size[0]) / 2 - image_margin_title_x,
              'y': text_display_grid[0]['title']['y']}
}

image_display_grid[1] = {
    'title': {'x': text_display_grid[1]['title']['x'],
              'y': sum(board_size[1]) / 2 - image_margin_title_y}
}

image_display_grid[2] = {
    'title': {'x': sum(board_size[0]) / 2 - image_margin_title_x,
              'y': text_display_grid[2]['title']['y']}
}

image_display_grid[3] = {
    'title': {'x': text_display_grid[3]['title']['x'],
              'y': sum(board_size[1]) / 2 - image_margin_title_y}
}
