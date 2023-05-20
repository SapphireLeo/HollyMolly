import time
from socket import *
import threading
from game_info import Board
from game_info import GameInfo as gi
from rules import Rule_default as Rule

port1 = 1234
port2 = 1235
ipfile = open('./ip.txt', 'r')
host = ipfile.readline()  # read ip information from text file
ipfile.close()

game_lock = threading.Lock()
print_lock = threading.Lock()

main_board = Board.Board()

server_command = ['set', 'open', 'bell']

def chatting(c_socket_chat, client_key):
    print_lock.acquire()
    print(client_key + '와의 채팅 연결 완료')
    print_lock.release()
    game_lock.acquire()
    num = len(main_board.clients) - list(main_board.clients.values()).count([])
    game_lock.release()
    start_message = "한 명이 게임에 접속했습니다. 현재 참가자 수: " + str(num)
    for sockets in list(main_board.clients.values()):
        if sockets:
            sockets[0][1].send(start_message.encode('utf-8'))
    try:
        while True:
            recv_data = c_socket_chat.recv(2048).decode('utf-8')

            if recv_data == "/시작":
                main_board.clients[client_key][1].start_vote = True
                response_chat = "한 명이 게임 시작/재시작에 투표했습니다."
                game_lock.acquire()
                if main_board.check_vote(main_board.sum_vote('start')):
                    main_board.game_fixed = False
                    main_board.reset_vote('start')
                    response_chat = "마지막 투표로 인해 이제 F12를 눌러 게임 시작이 가능합니다."
                game_lock.release()
            # elif recv_data == "/턴":
            #     main_board.clients[client_key][1].start_vote = True
            #     response_chat = "턴 넘기기에 한 명이 투표!"
            #     if main_board.check_vote(main_board.sum_vote('turn')):
            #         main_board.card_open(main_board.get_turn_key())
            #         main_board.reset_vote('turn')
            #         response_chat += "투표가 종료되었습니다."
            else:
                response_chat = 'PLAYER ' + str(list(main_board.clients.keys()).index(client_key)+1) + ' : ' + recv_data
            print('server echo:', response_chat)
            for sockets in list(main_board.clients.values()):
                if sockets:
                    sockets[0][1].send(response_chat.encode('utf-8'))
    except ConnectionResetError:
        end_message = '한 명이 게임을 종료했습니다.'
        game_lock.acquire()
        for client_idx, client_value in main_board.clients.items():
            if client_value and client_key != client_idx:
                client_value[0][1].send(end_message.encode('utf-8'))
        game_lock.release()
        print_lock.acquire()
        print(client_key + '와의 채팅 연결이 끊겼습니다.', flush=True)
        print_lock.release()

    c_socket_chat.close()
    exit(0)


is_request_available = True


def gaming(c_socket_game, client_key):
    game_info_header = bytearray(20)
    print_lock.acquire()
    print(client_key + '와의 게임 연결 완료')
    print_lock.release()
    try:
        while True:
            recv_data = c_socket_game.recv(1024).decode('utf-8')
            if recv_data in server_command:
                global is_request_available

                # entering game control, only when it is available.
                game_lock.acquire()
                if is_request_available:
                    # ignore the invalid bell request from player who do not have cards.
                    if main_board.clients[client_key][1].private_deck.get_card_num() == 0 and recv_data == 'bell':
                        if not main_board.check_valid_ring():
                            game_lock.release()
                            continue
                    # ignore the open request from player who are not his turn.
                    if main_board.get_turn_key() != client_key and recv_data == 'open':
                        print('wrong open request: ', client_key)
                        game_lock.release()
                        continue
                    # ignore the set request when game is already fixed.
                    if recv_data == 'set' and main_board.game_fixed:
                        print('wrong game set request: ', client_key)
                        game_lock.release()
                        continue
                    # block other requests
                    is_request_available = False
                else:
                    game_lock.release()
                    continue
                game_lock.release()
                if recv_data == 'set':
                    main_board.set_board()
                    # send set mode message
                    game_info_header[0] = 0
                    game_info_header[gi.set_mode_index['turn_start']] = main_board.turn
                    game_info_header[gi.set_mode_index['spare_card_num']] = main_board.spare_deck.get_card_num()
                    for client_name, client_player in main_board.clients.items():
                        if client_player:
                            game_info_header[gi.set_mode_index['card_num'][client_name]] = \
                                client_player[1].private_deck.get_card_num()

                elif recv_data == 'open':

                    main_board.card_open(client_key)
                    main_board.next_turn()
                    card_type, card_num = main_board.get_public_top(client_key)

                    # send open mode message
                    game_info_header[0] = 1
                    game_info_header[gi.open_mode_index['open_player']] = main_board.get_client_index(client_key)
                    game_info_header[gi.open_mode_index['current_turn']] = main_board.turn
                    game_info_header[gi.open_mode_index['card_type']] = Rule.types.index(card_type)
                    game_info_header[gi.open_mode_index['card_num']] = card_num

                elif recv_data == 'bell':

                    is_it_valid, go_to_spare = main_board.bell_ring(client_key)

                    # send bell mode message
                    game_info_header[0] = 2
                    game_info_header[gi.bell_mode_index['bell_player']] = main_board.get_client_index(client_key)
                    if is_it_valid:
                        game_info_header[gi.bell_mode_index['is_it_valid']] = 1
                    else:
                        game_info_header[gi.bell_mode_index['is_it_valid']] = 0
                    if go_to_spare:
                        game_info_header[gi.bell_mode_index['go_to_spare']] = 1
                    else:
                        game_info_header[gi.bell_mode_index['go_to_spare']] = 0
                    game_info_header[gi.bell_mode_index['current_turn']] = main_board.turn
                # broadcast the game state and change information to all connected clients.
                for client_index, client_socket in enumerate(list(main_board.clients.values())):
                    if client_socket:
                        if game_info_header[0] == 0:    # if game set
                            game_info_header[gi.set_mode_index['player_num']] = client_index
                        client_socket[0][0].send(game_info_header)
                print(main_board.get_board())

                # if bell event occurred:
                if game_info_header[0] == 2:
                    # if it is valid ring:
                    if is_it_valid:
                        # get ready to send player alive state.
                        game_info_header[0] = 3
                        # update alive state of players:
                        main_board.update_alive_players()
                        # get alive state from board:
                        player_alive_state = main_board.check_alive_players()
                        for index, state in enumerate(player_alive_state):
                            game_info_header[index+1] = state
                        time.sleep(3)
                        # send alive state to all clients:
                        for client_socket in list(main_board.clients.values()):
                            if client_socket:
                                client_socket[0][0].send(game_info_header)
                    # else it was invalid:
                    else:
                        time.sleep(1.5)

                game_lock.acquire()
                is_request_available = True
                game_lock.release()
    except ConnectionResetError:
        game_lock.acquire()
        main_board.disconnect(client_key)
        print(main_board.get_board())
        game_lock.release()
        print_lock.acquire()
        print(client_key + '와의 게임 연결이 끊겼습니다.')
        print_lock.release()

    game_lock.acquire()
    game_info_header[0] = 4
    game_info_header[1] = list(main_board.clients.keys()).index(client_key)
    game_info_header[2] = main_board.turn
    for client_socket in list(main_board.clients.values()):
        if client_socket:
            client_socket[0][0].send(game_info_header)
    game_lock.release()
    print_lock.acquire()
    print("현재 참가자 수 : ", str(len(main_board.connected_members)), flush=True)
    print_lock.release()

    c_socket_game.close()
    exit(0)


server_socket_game = socket(AF_INET, SOCK_STREAM)
server_socket_game.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server_socket_game.bind((host, port1))
server_socket_game.listen(6)

server_socket_chat = socket(AF_INET, SOCK_STREAM)
server_socket_chat.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server_socket_chat.bind((host, port2))
server_socket_chat.listen(6)

# cmdThread = threading.Thread(target=cmd)
# cmdThread.daemon = True
# cmdThread.start()

# try:
while True:
    print_lock.acquire()
    print('>> Wait')
    print_lock.release()

    # accept new client
    client_socket_game, addr_game = server_socket_game.accept()

    # accept new chat connection from the just-connected client
    client_socket_chat, addr_chat = server_socket_chat.accept()

    # allocate new client key to a new user
    user_key = main_board.add_client(client_socket_game, client_socket_chat)

    if not user_key:
        continue

        # start the chat communication thread
    thread_gaming = threading.Thread(target=gaming, args=(client_socket_game, user_key))

    thread_chat = threading.Thread(target=chatting, args=(client_socket_chat, user_key))

    # start the thread
    thread_gaming.start()

    thread_chat.start()

    print_lock.acquire()
    print("참가자 수 : ", len(main_board.clients) - list(main_board.clients.values()).count([]))
    print_lock.release()

# except Exception as e:
#    print('에러 : ', e)


server_socket_game.close()

exit(0)
