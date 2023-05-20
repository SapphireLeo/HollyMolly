from socket import *
import threading
import pygame

import Graphic
import Rule_default as Rule
import Chatting as Chat
printLock = threading.Lock()

port1 = 1234
port2 = 1235
ipfile = open('./ip.txt', 'r')
host = ipfile.readline()  # read ip information from text file
ipfile.close()

Graphic.buffer_to_server = ''

def receiver_game(sock_game):
    try:
        while True:
            recv_data = sock_game.recv(2048)

            # if received command is 'set':
            if recv_data[0] == 0:
                card_num_list = recv_data[4:8]
                spare_num = recv_data[3]
                my_index = recv_data[1]
                Graphic.game_set(card_num_list, spare_num, my_index)

            # if received command is 'open':
            elif recv_data[0] == 1:
                open_player_index = recv_data[1]
                Graphic.current_turn = recv_data[2]
                card_type = Rule.types[recv_data[3]]
                card_num = recv_data[4]
                Graphic.game_card_open(open_player_index, card_type, card_num)

            # if received command is 'bell':
            elif recv_data[0] == 2:
                bell_player_index = recv_data[1]
                is_it_valid = recv_data[2]
                go_to_spare = recv_data[3]
                current_turn = recv_data[4]
                Graphic.current_turn = current_turn
                if is_it_valid == 1:
                    Graphic.game_valid_bell(bell_player_index)
                else:
                    if go_to_spare == 1:
                        Graphic.game_invalid_bell(bell_player_index, True)
                    else:
                        Graphic.game_invalid_bell(bell_player_index, False)

            # if received command is 'update client state(win/lose)':
            elif recv_data[0] == 3:
                for player_index, state in enumerate(recv_data[1:5]):
                    Graphic.player_state[player_index] = state
                Graphic.commit_display()

            # if received command is 'disconnect':
            elif recv_data[0] == 4:
                Graphic.player_state[recv_data[1]] = 0
                print(Graphic.player_state)
                Graphic.disconnect(recv_data[1])
                Graphic.current_turn = recv_data[2]
                Graphic.commit_display()

    except ConnectionAbortedError:
        print('클라이언트 사용자가 게임 연결을 중단했습니다.')
    except ConnectionResetError:
        print('서버가 게임 연결을 종료했습니다.')
    exit(0)


client_socket_game = socket(AF_INET, SOCK_STREAM)
client_socket_game.connect((host, port1))

client_socket_chat = socket(AF_INET, SOCK_STREAM)
client_socket_chat.connect((host, port2))

receiver_thread_game = threading.Thread(target=receiver_game, args=(client_socket_game,))
receiver_thread_game.daemon = True

receiver_thread_game.start()


# sender_thread_chat.start()
# receiver_thread_chat.start()

chatting = Chat.Chat(client_socket_game, client_socket_chat)
chatting.run()
pygame.quit()