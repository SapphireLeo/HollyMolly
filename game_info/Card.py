class Card:
    def __init__(self, fruit_name, fruit_num, card_image):
        self.__fruit = fruit_name
        self.__num = fruit_num
        self.__image = card_image

    def get_card(self):
        return self.__fruit, self.__num

    def card_info(self):
        if self.__fruit == 'strawberry':
            fruit_name = ' berry'
        elif self.__fruit == 'banana':
            fruit_name = 'banana'
        elif self.__fruit == 'lime':
            fruit_name = '  lime'
        elif self.__fruit == 'plum':
            fruit_name = '  plum'
        else:
            fruit_name = 'default'
        return ' ' + fruit_name + ' - ' + str(self.__num) + ' '

    # change info of card, but it will be not used.
    def set_card(self, fruit_name, fruit_num, card_image):
        self.__fruit = fruit_name
        self.__num = fruit_num
        self.__image = card_image
