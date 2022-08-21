import tensorflow as tf
from PIL import Image, ImageOps
from tensorflow import keras
from torchvision import transforms
from Class_Names import class_names
import matplotlib.pyplot as plt
import numpy as np
import pygame


model = keras.models.load_model("Model")

# Initializing pygame
pygame.init()

# finals
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 600

# colors
BG_COLOR = (0, 0, 0)
WHITE = (255, 255, 255)
SAVE_BTN = (124, 205, 235)
SAVE_FONT = (255, 82, 99)
CHAR_LABEL = (242, 238, 111)

# Setting up main screen
display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Character Recognition - Devanagari")
display.fill(BG_COLOR)


class Spot:
    def __init__(self, pos_x=0, pos_y=0, color=WHITE):
        # validating whether the coordinates of the spots will fit in the grid
        if pos_x <= SCREEN_WIDTH - 20:
            self.pos_x = pos_x
        else:
            self.pos_x = 0
        if pos_y <= SCREEN_HEIGHT - 20:
            self.pos_y = pos_y
        else:
            self.pos_y = 0
        self.color = color

    def draw(self):
        """this method will draw the spot on the grid"""
        pygame.draw.rect(display, self.color, [self.pos_x, self.pos_y, 20, 20])


# drawing save button
def draw_save():
    pygame.draw.rect(display, SAVE_BTN, [0, 560, 700, 40])
    font = pygame.font.Font('freesansbold.ttf', 20)
    save_text = font.render("SAVE", True, SAVE_FONT)
    text_rect = save_text.get_rect()
    text_rect.center = (350, 580)
    display.blit(save_text, text_rect)


def draw_identified_number(num):
    pygame.draw.rect(display, CHAR_LABEL, [0, 0, 700, 40])
    font = pygame.font.Font('freesansbold.ttf', 35)
    num_text = font.render(str(num), True, SAVE_FONT)
    text_rect = num_text.get_rect()
    text_rect.center = (340, 20)
    display.blit(num_text, text_rect)


# number spots
char_spots = []

once = False

# run loop for pygame
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if pygame.mouse.get_pressed()[0]:
        if ((event.pos[1] // 20) * 20 < 560) and ((event.pos[1] // 20) * 20 > 40):
            char_spots.append(((event.pos[0] // 20) * 20, (event.pos[1] // 20) * 20))
            once = False
        try:
            # number spot instance
            number_spot = Spot(char_spots[-1][0], char_spots[-1][1])
            number_spot.draw()
        except IndexError:
            pass
    # removing obstacles with right-click
    if pygame.mouse.get_pressed()[2]:
        if ((event.pos[0] // 20) * 20, (event.pos[1] // 20) * 20) in char_spots:
            char_spots.remove(((event.pos[0] // 20) * 20, (event.pos[1] // 20) * 20))
            Spot(pos_x=(event.pos[0] // 20) * 20, pos_y=(event.pos[1] // 20) * 20, color=BG_COLOR).draw()

    # detecting save btn click
    if pygame.mouse.get_pressed()[0]:
        if (event.pos[1] // 20) * 20 >= 560:
            if not once:
                # saving drawn image
                pygame.image.save(display, "drawn_char.png")
                # RECOGNIZING THE CHARACTER DRAWN
                # grabbing the saved image
                test_img = Image.open('drawn_char.png', mode='r')
                test_img = ImageOps.grayscale(test_img)
                # cropping the image to not include the blue save btn on the bottom
                border = (0, 40, 700, 560)
                test_img = test_img.crop(border)
                # resizing the image to a 32 x 32
                p = transforms.Compose([transforms.Resize((32, 32))])
                test_img = p(test_img)
                # prediction
                img_array = tf.keras.utils.img_to_array(test_img)
                plt.imshow(img_array, cmap='gray', vmin=0, vmax=255)
                plt.show()
                img_array = tf.expand_dims(img_array, 0)  # Create a batch
                predictions = model.predict(img_array)
                score = tf.nn.softmax(predictions[0])
                x = class_names[np.argmax(score)]
                display.fill(BG_COLOR)
                draw_identified_number(x)
                char_spots.clear()
                once = True

    # drawing save button
    draw_save()

    # updating pygame
    pygame.display.update()
pygame.display.quit()
