import pygame  # pygame import
from Player_C import *
import Screen_info as SC

game_rule = 'default'

if game_rule == 'somethingelse':
    pass
else:
    import Rule_default as Rule

# initiating pygame
pygame.init()

screen = pygame.display.set_mode(SC.screen_size)

# main board display information. it is array of class Player.
board_display = []

player_state=[1,1,1,1]

current_turn = 0
my_index = 0

spare_deck = Deck.Deck(SC.spare_grid['x'], SC.spare_grid['y'], 90)

directory = './'
bell_image = pygame.image.load(directory + "images/bell.png")
hand_image = pygame.image.load(directory + "images/hand.png")
user_image = pygame.image.load(directory + "images/me.png")

# text information of each players
board_info = []

# define font information of title/content.
# pygame.font.SysFont(font name, size, bold=False, italic=False)
font = {
    'title': pygame.font.SysFont("arial", 35, True, True),
    'public': pygame.font.SysFont("arial", 25, True, True),
    'private': pygame.font.SysFont("arial", 25, True, True),
    'game end': pygame.font.SysFont("arial", 55, True, False)
}

game_done = False
clock = pygame.time.Clock()


def game_set(card_num, spare_num, index_mine):
    # clear the board
    board_display.clear()
    board_info.clear()
    global player_state
    player_state = [1,1,1,1]
    global my_index
    my_index = index_mine
    print('reset')
    for player_index in range(4):
        board_display.append(Player(player_index))
        board_display[player_index].set_card(card_num[player_index], 0)
        if card_num[player_index] == 0:
            player_state[player_index] = 0
        board_info.append({
            'title': ["Player " + str(player_index + 1), SC.BLACK],
            'private': [card_num[player_index], SC.BLACK],
            'public': [0, SC.BLACK]
        })

    spare_deck.deck_set('back', 1, spare_num)

    screen_init()
    board_update()
    info_update()
    commit_display()


def game_card_open(player_index, card_type, card_num):
    board_display[player_index].open_card(card_type, card_num)

    board_info[player_index]['title'][1] = SC.BLUE
    screen_init()
    board_update()
    info_update()
    commit_display()
    board_info[player_index]['title'][1] = SC.BLACK


def game_valid_bell(player_num):
    current_frame = 0

    moving_deck_list = []
    for i in range(4):
        # create a moving deck. coordinates of destination is defined at Screen_info.
        moving_deck_list.append(Deck.MovingDeck(SC.move_dest[player_num]['x'], SC.move_dest[player_num]['y']))

    # create a moving deck, which is moving from spare deck.
    moving_deck_from_spare = Deck.MovingDeck(SC.move_dest[player_num]['x'], SC.move_dest[player_num]['y'])
    board_info[player_num]['title'][1] = SC.GREEN


    done = False
    while not done:
        done = True
        clock.tick(1000)
        screen_init()
        for index, moving_deck in enumerate(moving_deck_list):
            if current_frame % 10 == 0:
                if board_display[index].public_deck.card_set:
                    moving_deck.card_enq(board_display[index].pop_card('public'))
            move_end_card = moving_deck.step_forward()
            if move_end_card:
                board_display[player_num].push_card(move_end_card, 'private')
            for card in moving_deck.card_queue:
                card.display(screen)
                done = False

        # move from spare deck
        if current_frame % 10 == 0:
            if spare_deck.card_set:
                moving_deck_from_spare.card_enq(spare_deck.pop_card())
        move_end_card = moving_deck_from_spare.step_forward()
        if move_end_card:
            board_display[player_num].private_deck.push_card(move_end_card)
        for card in moving_deck_from_spare.card_queue:
            card.display(screen)
            done = False

        info_update()
        board_update()
        display_hand(player_num)
        commit_display()
        current_frame += 1

    board_info[player_num]['title'][1] = SC.BLACK


def display_bell():
    rect = bell_image.get_rect()
    rect.center = (350, 350)
    screen.blit(bell_image, rect)


def display_hand(player_index):
    rotated = pygame.transform.rotate(hand_image, (6 - player_index) % 4 * 90)
    rect = rotated.get_rect()
    rect.center = (350, 325)
    screen.blit(rotated, rect)


def game_invalid_bell(player_num, goto_spare):
    current_frame = 0
    print('invalid bell!')
    if not goto_spare:
        moving_deck_list = []
        for player_index, player in enumerate(board_display):
            moving_deck_list.append(Deck.MovingDeck(SC.move_dest[player_index]['x'], SC.move_dest[player_index]['y']))

        board_info[player_num]['title'][1] = SC.RED

        total_popped_card = 0
        done = False
        while not done:
            done = True
            clock.tick(1000)
            screen_init()
            for index, moving_deck in enumerate(moving_deck_list):
                # do not move card from the player's own original deck.
                if index is not player_num:
                    if total_popped_card < (sum(player_state)- 1) * Rule.bell_penalty:
                        if current_frame % 10 == 0 and player_state[index] == 1:
                            moving_deck.card_enq(board_display[player_num].pop_card('private'))
                            total_popped_card += 1

                # if there is a card which ended its move, push it to the destination.
                move_end_card = moving_deck.step_forward()
                if move_end_card:
                    board_display[index].push_card(move_end_card, 'private')

                for card in moving_deck.card_queue:
                    card.display(screen)
                    done = False

            info_update()
            board_update()
            display_hand(player_num)
            commit_display()
            current_frame += 1

    # if there is not enough card for penalty, then move the deck to spare deck:
    else:
        moving_deck = Deck.MovingDeck(SC.spare_dest['x'], SC.spare_dest['y'])
        done = False
        while not done:
            done = True
            clock.tick(1000)
            screen_init()

            if current_frame % 10 == 0:
                # if there is card left in the player's private deck:
                if board_display[player_num].private_deck.card_set:
                    moving_deck.card_enq(board_display[player_num].pop_card('private'))
            move_end_card = moving_deck.step_forward()
            if move_end_card:
                spare_deck.push_card(move_end_card)
            for card in moving_deck.card_queue:
                card.display(screen)
                done = False

            info_update()
            board_update()
            display_hand(player_num)
            commit_display()
            current_frame += 1
    board_info[player_num]['title'][1] = SC.BLACK


def disconnect(player_index):
    if player_index >= len(board_display):
        return
    current_frame = 0
    moving_deck_from_public = Deck.MovingDeck(SC.spare_dest['x'], SC.spare_dest['y'])
    moving_deck_from_private = Deck.MovingDeck(SC.spare_dest['x'], SC.spare_dest['y'])
    done = False
    while not done:
        done = True
        clock.tick(1000)
        screen_init()

        if current_frame % 10 == 0:
            # if there is card left in the player's private deck:
            if board_display[player_index].public_deck.card_set:
                moving_deck_from_public.card_enq(board_display[player_index].pop_card('public'))
            if board_display[player_index].private_deck.card_set:
                moving_deck_from_private.card_enq(board_display[player_index].pop_card('private'))
        move_end_card_public = moving_deck_from_public.step_forward()
        move_end_card_private = moving_deck_from_private.step_forward()

        if move_end_card_public:
            move_end_card_public.change_image('back', 1)
            spare_deck.push_card(move_end_card_public)
        if move_end_card_private:
            spare_deck.push_card(move_end_card_private)

        for card in moving_deck_from_public.card_queue:
            card.display(screen)
            done = False
        for card in moving_deck_from_private.card_queue:
            card.display(screen)
            done = False

        info_update()
        board_update()
        commit_display()
        current_frame += 1


def screen_init():
    screen.fill(SC.WHITE)


def board_update():
    for player in board_display:
        for card in player.public_deck.card_set:
            card.display(screen)
        for card in player.private_deck.card_set:
            card.display(screen)
    for card in spare_deck.card_set:
        card.display(screen)
    display_bell()


def info_update():
    global my_index
    for index, info in enumerate(board_info):
        # if player is dead, show his name in GREY color.
        if player_state[index] == 0:
            board_info[index]['title'][1] = SC.GREY

        info['private'][0] = board_display[index].private_deck.get_size()
        info['public'][0] = board_display[index].public_deck.get_size()
        for menu, text in info.items():
            # text[0] is content, text[1] is color. print the text by .render()
            text_display = font[menu].render(str(text[0]), True, text[1])
            # get x and y coordinates of title
            x = SC.text_display_grid[index][menu]['x']
            y = SC.text_display_grid[index][menu]['y']
            rect = text_display.get_rect()
            rect.center = x, y
            screen.blit(text_display, rect)
    turn_text = font['title'].render("Turn: "+str(current_turn+1), True, SC.BLACK)
    rect = turn_text.get_rect()
    rect.topright = SC.screen_size_x, 0
    screen.blit(turn_text, rect)
    my_index_text = font['title'].render("Me: "+str(my_index+1), True, SC.BLACK)
    rect = turn_text.get_rect()
    rect.bottomright = SC.screen_size_x, SC.screen_size_y
    screen.blit(my_index_text, rect)


def commit_display():
    if player_state[my_index] == 0:
        lose_text = font['title'].render("You Lost the game.", True, SC.RED)
        rect = lose_text.get_rect()
        rect.topleft = 0, 0
        screen.blit(lose_text, rect)
    if player_state.count(1) == 1:
        win_text = font['game end'].render("Winner : Player " + str(player_state.index(1)+1), True, SC.GREEN)
        rect = win_text.get_rect()
        rect.center = 350, 350
        screen.blit(win_text, rect)
    x = SC.text_display_grid[current_turn]['title']['x']
    y = SC.text_display_grid[current_turn]['title']['y']
    pygame.draw.rect(screen, SC.BLUE, [x-70, y-40, 140, 80], 2)

    x = SC.image_display_grid[my_index]['title']['x']
    y = SC.image_display_grid[my_index]['title']['y']
    user_image_rect = user_image.get_rect()
    user_image_rect.center = x, y
    screen.blit(user_image, user_image_rect)

    pygame.display.update()
