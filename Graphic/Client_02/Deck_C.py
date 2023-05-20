import Card_C as Card


class Deck:
    def __init__(self, x, y, rotation):
        self.card_set = []
        self.top_grid = {'x': x, 'y': y}
        self.rotation_degree = rotation

    def deck_clear(self):
        self.card_set.clear()

    def deck_set(self, card_type, card_num, total_num):
        for i in range(total_num):
            self.push_card(Card.Card(card_type, card_num, 0, 0, self.rotation_degree))

    def get_size(self):
        return len(self.card_set)

    def push_card(self, card):
        # add the card to the deck
        self.card_set.append(card)

        # refactor the coordinates of the card to the top of deck
        card.change_position(self.top_grid['x'], self.top_grid['y'])

        card.change_rotation(self.rotation_degree)

        # increase the graphic heights of deck
        self.top_grid['x'] += 0.5
        self.top_grid['y'] += 0.5

    def pop_card(self):
        # decrease the graphic heights of private deck
        self.top_grid['x'] -= 0.5
        self.top_grid['y'] -= 0.5

        return self.card_set.pop()


class MovingDeck:
    def __init__(self, dest_x, dest_y):
        self.card_queue = []
        self.source_grid = []
        self.step_grid = []
        self.step_repeat = []
        self.step_num = 75
        self.step_speed = 100
        self.destination_grid = (dest_x, dest_y)

    def card_enq(self, card):
        self.card_queue.insert(0, card)
        self.source_grid.insert(0, card.get_position())
        self.step_grid.insert(0, self.get_step_to(card.get_position()))
        self.step_repeat.insert(0, 0)

    def card_deq(self):
        self.source_grid.pop()
        self.step_grid.pop()
        self.step_repeat.pop()
        return self.card_queue.pop()

    def get_step_to(self, source_grid):
        step_x = (self.destination_grid[0] - source_grid[0]) / self.step_num
        step_y = (self.destination_grid[1] - source_grid[1]) / self.step_num
        return step_x, step_y

    def step_forward(self):
        if self.step_repeat:
            if self.step_repeat[-1] >= self.step_num:
                return self.card_deq()
        for index, card in enumerate(self.card_queue):
            card.move_position(self.step_grid[index][0], self.step_grid[index][1])
            self.step_repeat[index] += 1
        return None
