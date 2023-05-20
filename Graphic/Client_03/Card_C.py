import cv2
import pygame  # pygame import

game_rule = 'default'

if game_rule == 'somethingelse':
    pass
else:
    import Rule_default as Rule

directory = './'

card_image = {}
for card_type in Rule.types:
    card_image[card_type] = [[] for nums in Rule.number]

for card_type in Rule.types:
    for card_num in range(len(Rule.number)):
        file_name = directory + 'images/' + str(card_type) + '_' + str(card_num + 1) + '.png'
        # add image information
        card_image[card_type][card_num].append(file_name)

        # add shape information. it is tuple (height, weight)
        file_image = cv2.imread(file_name)
        card_image[card_type][card_num].append(file_image.shape)

# add image and shape information of card backside.
file_name = directory + 'images/card_back.png'
card_image['back'] = [file_name, cv2.imread(file_name).shape]


def card_image_load(load_card_type, load_card_num, *image_scaling):
    load_card_num -= 1
    image_origin_height = 100
    image_origin_width = 100
    scaling_factor = 1

    # get image.
    if load_card_type in Rule.types:
        image_entity = pygame.image.load(card_image[load_card_type][load_card_num][0])
    elif load_card_type == 'back':
        image_entity = pygame.image.load(card_image['back'][0])

    # if there is scaling option:
    if len(image_scaling) > 0:

        # and the scaling is defined by rate(%):
        if len(image_scaling) == 1:
            if load_card_type in Rule.types:
                image_origin_height = card_image[load_card_type][load_card_num][1][0]
                image_origin_width = card_image[load_card_type][load_card_num][1][1]
            elif load_card_type == 'back':
                image_origin_height = card_image['back'][1][0]
                image_origin_width = card_image['back'][1][1]

            # get scaling factor(n %)
            if image_scaling[0][-1] == '%':
                # if image scaling is %:
                scaling_factor = int(image_scaling[0][0:-1]) / 100
            elif image_scaling[0][-1] == 'x':
                # if image scaling standard is x:
                scaling_factor = int(image_scaling[0][0:-1]) / card_image[load_card_type][load_card_num][1][0]
            elif image_scaling[0][-1] == 'y':
                # if image scaling standard is y:
                scaling_factor = int(image_scaling[0][0:-1]) / card_image[load_card_type][load_card_num][1][1]
            # define the accurate image size by scaling factor
            image_size_height = image_origin_height * scaling_factor
            image_size_width = image_origin_width * scaling_factor
        # if scaling is defined by fixed size:
        elif len(image_scaling) == 2:
            image_size_height = image_scaling[0]
            image_size_width = image_scaling[1]

        # resize the image and return image
        image_entity = pygame.transform.scale(image_entity, (image_size_width, image_size_height))

    return image_entity


class Card:
    def __init__(self, load_card_type, load_card_num, grid_x, grid_y, rotation):
        self.rotation_degree = 0
        self.image_file = card_image_load(load_card_type, load_card_num)
        self.change_rotation(rotation)
        self.grid = {'x': grid_x, 'y': grid_y}

    def change_image(self, load_card_type, load_card_num):
        self.__init__(load_card_type, load_card_num, self.grid['x'], self.grid['y'], self.rotation_degree)

    def change_position(self, position_x, position_y):
        self.grid['x'] = position_x
        self.grid['y'] = position_y

    def change_rotation(self, rotation):
        self.image_file = pygame.transform.rotate(self.image_file, rotation-self.rotation_degree)
        self.rotation_degree = rotation

    def move_position(self, step_x, step_y):
        self.grid['x'] += step_x
        self.grid['y'] += step_y

    def get_position(self):
        return self.grid['x'], self.grid['y']

    def display(self, screen):
        image_rect = self.image_file.get_rect()
        image_rect.center = self.grid['x'], self.grid['y']
        screen.blit(self.image_file, image_rect)
