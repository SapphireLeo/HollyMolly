import random
import copy


class Deck:
    def __init__(self):
        self.__card_list = []

    def set_deck(self, new_list):
        self.__card_list = copy.deepcopy(new_list)

    def get_deck(self):
        return self.__card_list

    # add_deck : add source deck into this deck.
    def add_deck(self, new_deck):
        shuffled_deck = new_deck.get_deck()
        random.shuffle(shuffled_deck)
        self.__card_list = shuffled_deck + self.__card_list

    # merge_deck : add source deck into this deck, and clear the source deck
    def merge_deck(self, new_deck):
        self.add_deck(new_deck)
        new_deck.deck_clear()

    def card_enq(self, new_card):
        self.__card_list.insert(0, new_card)

    def card_deq(self):
        return self.__card_list.pop()

    def get_public_top(self):
        # if there is at least 1 card in the deck, return top of the public deck.
        if self.__card_list:
            return self.__card_list[0].get_card()
        # if there is no card in the deck, return null.
        else:
            return 'none', 0

    def get_card_num(self):
        return len(self.__card_list)

    def deck_shuffle(self):
        random.shuffle(self.__card_list)

    def deck_clear(self):
        self.__card_list.clear()

    def deck_info(self):
        deck_info_str = '|'
        for i, card in enumerate(self.__card_list):
            deck_info_str = deck_info_str + card.card_info() + '|'
            if i % 8 == 7:
                deck_info_str = deck_info_str + '\n|'
        return deck_info_str
