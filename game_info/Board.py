from game_info import Player, Deck, Card
import time
import copy
import random
# from concurrent import futures
from tkinter import messagebox

game_rule = 'default'

if game_rule == 'somethingelse':
    pass
else:
    from rules import Rule_default as Rule

# check if the rule is valid
if Rule.min_member < 2:
    messagebox.showinfo("오류", "규칙이 잘못되었습니다:\n최소 플레이 인원은 2명 이상이어야 합니다.")
    exit(0)


# creating initial total game deck
def initial_deck():
    init = []
    for type_name in Rule.types:
        for num_in_a_card, total_num_of_the_cards in enumerate(Rule.number):
            for i in range(total_num_of_the_cards):
                # add the card, but number in a card must be + 1, because index begins at 0.
                init.append(Card.Card(type_name, num_in_a_card + 1, 0))
    random.shuffle(init)
    return init


def wait_after_bell():
    time.sleep(2)
    return True


class Board:
    def __init__(self):
        self.bell = 0
        self.clients = dict(
            client1=[],
            client2=[],
            client3=[],
            client4=[],
            client5=[],
            client6=[]
        )
        self.connected_members = []
        self.alive_players = []
        self.spare_deck = Deck.Deck()
        self.turn = 0
        self.game_fixed = True

    def add_client(self, new_client_socket_game, new_client_socket_chat):
        for key, value in self.clients.items():
            if not value:
                self.clients[key].append((new_client_socket_game, new_client_socket_chat))
                self.clients[key].append(Player.Player())
                self.connected_members.append(key)
                return key
        return False

    def disconnect(self, client_key):
        if client_key == self.get_turn_key():
            self.next_turn()
        if len(self.clients[client_key]) > 0:
            self.spare_deck.merge_deck(self.clients[client_key][1].public_deck)
            self.spare_deck.merge_deck(self.clients[client_key][1].private_deck)
        self.clients[client_key].clear()
        if client_key in self.alive_players:
            self.alive_players.remove(client_key)
        if client_key in self.connected_members:
            self.connected_members.remove(client_key)

    def set_board(self):
        self.game_fixed = True

        if not Rule.min_member <= len(self.connected_members) <= Rule.max_member:
            return False

        self.alive_players = copy.deepcopy(self.connected_members)

        # give first turn to the first connected player.
        self.turn = list(self.clients.keys()).index(self.alive_players[0])

        # shuffle init deck and divide
        init_deck = initial_deck()

        # Rule.total_card is total number of card.
        # divide all card by the total number of player.
        # first, get the divided card number.
        partial_card_num = Rule.total_card // len(self.connected_members)

        for i in range(0, Rule.total_card, partial_card_num):

            # first, divide the initial deck into partial deck.

            if i + partial_card_num > Rule.total_card:
                # if there is card left, move it to the 'spare deck'
                self.spare_deck.set_deck(init_deck[i:Rule.total_card])
            else:
                # if there is no spare cards, make partial deck for a player.
                partial_deck = init_deck[i:i + partial_card_num]

                # find a player name who will get a partial deck.
                # the name of player is in the list "alive_players".
                player_name = self.alive_players[i // partial_card_num]

                # set the player's private deck to the partial deck, and public deck to empty.
                self.clients[player_name][1].set_player(partial_deck, [])

    def get_turn_key(self):
        return list(self.clients.keys())[self.turn]

    def get_client_index(self, client_key):
        return list(self.clients.keys()).index(client_key)

    def next_turn(self):
        # find the next turn player.
        for i in range(1, len(self.clients) + 1):
            # search index of next turn player. when it reaches end of the dictionary, go back to first.
            idx = (i + self.turn) % len(self.clients)
            # if there is next turn player, give turn to him.
            if list(self.clients.keys())[idx] in self.alive_players:
                if list(self.clients.values())[idx][1].private_deck.get_card_num() > 0:
                    self.turn = idx
                    return list(self.clients.keys())[idx]

    def card_open(self, player_key):
        if self.clients[player_key]:
            self.clients[player_key][1].card_open()
            return True
        else:
            print("error: there isn't", player_key)
            return False

    def get_public_top(self, player_key):
        return self.clients[player_key][1].public_deck.get_public_top()

    def try_bell(self):
        if self.bell == 0:
            self.bell = 1
            return True
        else:
            return False

    def check_valid_ring(self):

        # check_dict is active allocation of dictionary,
        # because there can be more sort and rules
        check_dict = {}
        for players in self.alive_players:
            card_type, card_num = self.clients[players][1].get_public_top()

            # if there is no existing numer of the card type of input, add it to the dictionary.
            if card_type not in check_dict:
                check_dict[card_type] = card_num

            # if there is already an existing card type and its total number, add number to the card type.
            else:
                check_dict[card_type] += card_num

        # if there is a card type that total number of it is 5, bell ring is VALID >>> return True.
        if Rule.number_for_valid_bell in check_dict.values():
            return True
        # else, bell ring is NOT VALID >>> return False.
        else:
            return False

    def bell_ring(self, player_key):
        # with futures.ThreadPoolExecutor() as executor:
        #    waited = executor.submit(wait_after_bell)

        # if the bell ring of the player was valid:
        if self.check_valid_ring():
            # move all players' public deck to the bottom of bell ringer's private deck.
            if self.spare_deck.get_deck():
                self.clients[player_key][1].private_deck.merge_deck(self.spare_deck)
            for player in self.alive_players:
                self.clients[player_key][1].private_deck.merge_deck(self.clients[player][1].public_deck)
            return True, False

        # if the bell ring of the player was NOT valid:
        else:
            # if there is enough card, the player give the penalty card to all players' private deck.
            if Rule.bell_penalty * (len(self.alive_players) - 1) <= \
                    self.clients[player_key][1].private_deck.get_card_num():
                for player in self.alive_players:
                    if player is player_key:
                        continue
                    for i in range(Rule.bell_penalty):
                        self.clients[player][1].private_deck.card_enq(
                            self.clients[player_key][1].private_deck.card_deq())
                if self.clients[self.get_turn_key()][1].private_deck.get_card_num() == 0:
                    self.next_turn()
                return False, False

            # if there is not enough card, the player give the private deck to the spare deck.
            else:
                self.spare_deck.merge_deck(self.clients[player_key][1].private_deck)
                # if the player who lost all card is current turn player:
                if self.clients[self.get_turn_key()][1].private_deck.get_card_num() == 0:
                    self.next_turn()
                return False, True

        # if futures.as_completed(waited):
        #    pass

    def check_alive_players(self):
        player_state_array=[]
        for player_key in list(self.clients.keys()):
            if player_key in self.alive_players:
                player_state_array.append(True)
            else:
                player_state_array.append(False)
        return player_state_array

    def update_alive_players(self):
        for player_key in list(self.clients.keys()):
            if self.clients[player_key]:
                if self.clients[player_key][1].private_deck.get_card_num() == 0:
                    self.kill_player(player_key)

    def kill_player(self, player_key):
        print(player_key + ' has been killed.')
        if player_key in self.alive_players:
            self.alive_players.remove(player_key)

    def check_vote(self, vote_sum):
        if vote_sum >= len(self.connected_members) - 1:
            return True
        else:
            return False

    def sum_vote(self, vote):
        vote_sum = 0
        for player in list(self.clients.values()):
            if player:
                if vote == 'start':
                    if player[1].start_vote:
                        vote_sum += 1
                elif vote == 'turn':
                    if player[1].turn_vote:
                        vote_sum += 1
        return vote_sum

    def reset_vote(self, vote):
        for player in list(self.clients.values()):
            if player:
                if vote == 'start':
                    player[1].start_vote=False
                elif vote == 'turn':
                    player[1].turn_vote=False

    def get_board(self):
        board_info_str = ''
        # board_info_str = board_info_str + str(self.connected_members)
        for member in self.alive_players:
            board_info_str = board_info_str + '-' * 50 + member + '-' * 50 + '\n' + self.clients[member][
                1].player_info()
        board_info_str = board_info_str + '-' * 51 + 'spare' + '-' * 51 + '\n' + self.spare_deck.deck_info()
        board_info_str = board_info_str + '\n' + '-' * 51 + 'turn' + '-' * 52 + '\n' \
                         + 'current turn:  ' + list(self.clients.keys())[self.turn]

        return board_info_str
