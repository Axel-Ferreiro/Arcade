import pygame


# COLORS

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255,255,255)
BLACK = (0,0,0)
YELLOW = (255,255,0)
CYAN = (0,255,255)
MAGENTA = (255,0,255)
GOLD = (234,223,21)

colores = [RED, GREEN, BLUE, WHITE, YELLOW, CYAN, MAGENTA]

# SIZE SCREEN
WIDTH = 800
HEIGHT = 600
SIZE_SCREEN = (WIDTH, HEIGHT)

CENTER_SCREEN = (WIDTH // 2 , HEIGHT // 2)
CENTER_SCREEN_X = WIDTH // 2
CENTER_SCREEN_Y = HEIGHT // 2



# MEDIDA PERSONAJE RECTANGULO

rec_widht = 50
rec_height = 50

# CANTIDAD DE ENEMIGOS

cant_enemies = 10

#FPS 

FPS = 60

# VELOCIDAD

SPEED = 8

#VELOCIDAD LASER

speed_laser = 20


# CONFIGURO LA DIRECCION

UR = 9
DR = 3
DL  =1
UL = 7

direcciones = (UR,DR,DL,UL)

# DIRECCION
move_up = False
move_down = False





# MEDIDA RECTANGULO BOTON
screen = pygame.display.set_mode(SIZE_SCREEN)

SIZE_BUTTON = (200,50)
rect_entrar = pygame.Rect(screen.get_width() // 2 - SIZE_BUTTON[0] // 2 ,370,SIZE_BUTTON[0],SIZE_BUTTON[1])
rect_controles = pygame.Rect(screen.get_width() // 2 - SIZE_BUTTON[0] // 2 ,440,SIZE_BUTTON[0],SIZE_BUTTON[1])
rect_salir = pygame.Rect(screen.get_width() // 2 - SIZE_BUTTON[0] // 2 ,510,SIZE_BUTTON[0],SIZE_BUTTON[1])

#NUEVO EVENTO
EVENT_NEW_LIFE = pygame.USEREVENT + 1 # creo vida aleatoria
pygame.time.set_timer(EVENT_NEW_LIFE , 16000)