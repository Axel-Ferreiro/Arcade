import pygame
from config import *
from pygame.locals import *


# FUNCION TERMINAR

def terminar():
    """
    Cierra la ventana de Pygame y finaliza la ejecución del programa.
    """
    pygame.quit()
    exit()       


#FUNCION CREAR BLOQUE

def get_blocks(imagen = None,left=0, top=0, width =40, height=40, color=(255,255,255), dir = 3 )-> dict:
    if imagen:
        imagen = pygame.transform.scale(imagen, (width, height))


    block = {"rect": pygame.Rect(left, top, width, height),"color" : color,"imagen": imagen,"dir": dir}

    return block



# FUNCION PARA DIBUJAR PERSONAJES
def dibujar_personajes(superficie ,personajes):
        for personaje in personajes:
            if personaje["imagen"]:
                superficie.blit(personaje["imagen"], personaje["rect"])
            else:
                pygame.draw.rect(superficie, personaje["color"], personaje["rect"],personaje["borde"],personaje["radio"])

#FUNCION PARA CARGAR ENEMIGOS A LISTA
def load_enemies(lista, imagen, left, top, width, height):
    for i in range(cant_enemies):
        lista.append(get_blocks(imagen, left, top, width, height))


# FUNCION TOCAR BOTON PARA INICIAR
def wait_click_start(rect_boton,rect_boton2,rect_boton3,screen,color_fondo,color_letra,color_rect):
    import pygame
    pantalla_inicial_image =pygame.transform.scale(pygame.image.load("./src/assets/presentacion_pcman.jpg"),SIZE_SCREEN)
    while True:
        fuente = pygame.font.SysFont("comicsans", 36)
        crear_boton(screen,"Jugar", color_fondo, color_letra, rect_boton,color_rect, fuente)
        crear_boton(screen,"Controles", color_fondo, color_letra, rect_boton2,color_rect, fuente)
        crear_boton(screen,"Salir", color_fondo, color_letra, rect_boton3,color_rect, fuente)
        pygame.display.flip()
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminar()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        terminar()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if rect_boton.collidepoint(event.pos): 
                            return None
                        elif rect_boton2.collidepoint(event.pos):
                            mostrar_controles()
                            wait_user()
                            screen.blit(pantalla_inicial_image,(0,0))
                        elif rect_boton3.collidepoint(event.pos):
                            terminar()



#FUNCION MOSTRAR TEXTO CENTRADO
def mostrar_texto_centrado(screen, texto, center_x, center_y, color, fuente):
    """
    Muestra un texto centrado en una superficie de pygame.

    Parámetros:
    - screen: La superficie de pygame en la que se mostrará el texto.
    - texto: El texto que se mostrará.
    - center_x: La coordenada x del centro donde se mostrará el texto.
    - center_y: La coordenada y del centro donde se mostrará el texto.
    - color: El color del texto.
    - fuente: La fuente de pygame a utilizar para el texto.

    Ejemplo de uso:
    font = pygame.font.Font(None, 36)
    mostrar_texto_centrado(mi_superficie, "Hola, Mundo!", 400, 300, (255, 255, 255), font)
    """
    render = fuente.render(texto, True, color )
    rect_text= render.get_rect(center = (center_x, center_y))
    screen.blit(render,rect_text)



#FUNCION CREAR BOTON
def crear_boton(screen,texto, bg_color,bg_color_hover, rect_boton: pygame.Rect,font_color, fuente):
    """
    Crea un botón en la pantalla con la capacidad de cambiar de color al pasar el mouse por encima.

    Parámetros:
    - screen: La superficie de pygame en la que se creará el botón.
    - texto: El texto que se mostrará en el botón.
    - bg_color: El color de fondo del botón.
    - bg_color_hover: El color de fondo del botón cuando el mouse está sobre él.
    - rect_boton: El rectángulo que define la posición y el tamaño del botón.
    - font_color: El color del texto en el botón.
    - fuente: La fuente de pygame a utilizar para el texto.

    """
    if rect_boton.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, bg_color_hover,rect_boton , border_radius = 5)
    else:
        pygame.draw.rect(screen, bg_color,rect_boton , border_radius = 5)
    mostrar_texto_centrado(
        screen, texto, *rect_boton.center, font_color, fuente)
    

#FUNCION PARA CREAR LASERS
def get_laser(mid_right, speed_x =5 ):

    rec = pygame.Rect(mid_right[0],mid_right[1] - 6, 6 ,8)
    return{"rect": rec, "speed_x": speed_x}


# DETECTAR COLISIONES

def calcular_radio(rect):
    return rect.height // 2

def distancia_entre_puntos(punto_1 , punto_2):
    x1, y1 = punto_1
    x2, y2 = punto_2
    return ((x2 -x1) ** 2 + (y2 - y1)** 2) ** 0.5

def detectar_colision(rect_1, rect_2):


    distancia = distancia_entre_puntos(rect_1.center, rect_2.center)

    return distancia <= (calcular_radio(rect_1) +  calcular_radio(rect_2) )


# MOSTRAR TEXTO EN PAUSA

def mostrar_texto(superficie,texto, fuente , coordenadas ,color_fuente  ):
        sup_texto = fuente.render(texto, True , color_fuente)
        rect_texto = sup_texto.get_rect()
        rect_texto.center = coordenadas
        superficie.blit(sup_texto, rect_texto)


# FUNCION ESPERAR A TOCAR TECLA PARA ARRANCAR

def wait_user():
    """
    Espera la interacción del usuario. Sale del bucle cuando se presiona una tecla o se cierra la ventana.

    """
    while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminar()

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        terminar()
                    return


#  MOSTRAR VALORES DEL  JUEGO

def mostrar_valores(texto, valor, color, fuente, posicion):
    texto_valor = fuente.render(f"{texto}: {valor}", True, color)
    rectangulo = texto_valor.get_rect()
    rectangulo.center = posicion
    return texto_valor, rectangulo


# MOSTRAR CONTROLES

def mostrar_controles():
    fuente = pygame.font.SysFont("Cambria", 36)
    screen.fill(BLACK)

    text = fuente.render("Controles del Juego.", True, WHITE)
    rect = text.get_rect(center=(WIDTH // 2, 50))
    screen.blit(text, rect)

    instrucciones = [
        "Presiona W/flecha arriba: para mover hacia arriba.",
        "Presiona S/flecha abajo: para mover hacia abajo.",
        "Presiona Barra Espaciadora: para disparar.",
        "Presiona P: para pausar.",
        "Presiona M: para silenciar la música.",
        "Presiona Esc: para salir.",
        "Presione cualquier tecla para continuar..."
    ]

    for i in range(len(instrucciones)):
        instruccion = instrucciones[i]
        text = fuente.render(instruccion, True, WHITE)
        rect = text.get_rect(center=(WIDTH // 2, 200 + i * 40))
        screen.blit(text, rect)

    pygame.display.flip()




