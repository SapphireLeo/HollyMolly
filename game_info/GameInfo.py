bGameInfo = bytearray(20)
set_mode_index = dict(
    player_num=1,
    turn_start=2,
    spare_card_num=3,
    card_num={
        'client1':4,
        'client2':5,
        'client3':6,
        'client4':7
    }
)

open_mode_index = dict(
    open_player=1,
    current_turn=2,
    card_type=3,
    card_num=4
)

bell_mode_index = dict(
    bell_player=1,
    is_it_valid=2,
    go_to_spare=3,
    current_turn=4
)
