import Deck_C as Deck
import Screen_info as Sci


class Player:
    def __init__(self, index):
        # get card-image rotation degree of this player. !!(counterclockwise)!!
        rotation_degree = (6 - index) % 4 * 90

        x = Sci.board_display_grid[index]['private']['x']
        y = Sci.board_display_grid[index]['private']['y']
        self.private_deck = Deck.Deck(x, y, rotation_degree)

        x = Sci.board_display_grid[index]['public']['x']
        y = Sci.board_display_grid[index]['public']['y']
        self.public_deck = Deck.Deck(x, y, rotation_degree)

    def set_card(self, private_num, public_num):
        self.private_deck.deck_clear()
        self.public_deck.deck_clear()

        self.private_deck.deck_set('back', 1, private_num)
        self.public_deck.deck_set('back', 1, public_num)

    def push_card(self, card, sort):
        if sort == 'private':
            card.change_image('back', 1)
            # add the card to the private deck
            self.private_deck.push_card(card)
        elif sort == 'public':
            # add the card to the public deck
            self.public_deck.push_card(card)

    def pop_card(self, sort):
        if sort == 'private':
            return self.private_deck.pop_card()
        elif sort == 'public':
            return self.public_deck.pop_card()

    def open_card(self, card_type, card_num):
        # pop a card from private deck, and push it to the public deck.
        popped_card = self.pop_card('private')
        popped_card.change_image(card_type, card_num)
        self.push_card(popped_card, 'public')
