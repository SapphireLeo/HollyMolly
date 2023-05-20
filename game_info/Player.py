from game_info import Deck


class Player:
    def __init__(self):
        self.private_deck = Deck.Deck()
        self.public_deck = Deck.Deck()
        self.start_vote = False
        self.turn_vote = True

    def get_private_deck(self):
        return self.private_deck.get_deck()

    def get_public_deck(self):
        return self.public_deck.get_deck()

    def set_player(self, new_private, new_public):
        self.private_deck.set_deck(new_private)
        self.public_deck.set_deck(new_public)

    def card_open(self):
        if self.private_deck.get_card_num == 0:
            return False
        else:
            self.public_deck.card_enq(self.private_deck.card_deq())
            return True

    def get_public_top(self):
        return self.public_deck.get_public_top()

    def player_info(self):
        return 'private:\n'+self.private_deck.deck_info() + '\npublic:\n'+self.public_deck.deck_info()+'\n'
