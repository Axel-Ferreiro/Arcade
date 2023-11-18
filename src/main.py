import pygame
from pygame.locals import *
import sys
from config import *
from funciones import *
from random import *
from assets_1 import *



# INICIO EL JUEGO
pygame.init()

pygame.mixer.music.load("./src/assets/music_fondo_pcman.mp3") 

pygame.mixer.music.play(-1)# estoo es para q quede en un loop infinito

pygame.mixer.music.set_volume(0.1) # esto es para controlar el volumen

fuente = pygame.font.SysFont("Cambria", 36)

pygame.display.set_caption("Arcade")

clock = pygame.time.Clock()

screen = pygame.display.set_mode(SIZE_SCREEN)

playing_music = True

pygame.display.flip()


while True:

    lives=3
    score = 0
    laser = None
    trick_stop = False

    pygame.mixer.music.play(-1)
    screen.blit(pantalla_inicial_image,(0,0))
    mostrar_texto(screen,"Pac Man - Shoot",fuente,(WIDTH // 2, 50), WHITE)

    logo_vidas = []
    enemies = []
    load_enemies(enemies, fantasma_2, randint(200, WIDTH - rec_widht),randint(0,HEIGHT - rec_height), 50, 50)
    wait_click_start(rect_entrar,rect_controles,rect_salir,screen,BLUE,WHITE,BLACK)

    block = get_blocks(pac_man, 0, 150, rec_widht, rec_height)
    is_running = True

    pygame.display.flip()


    while is_running:

        clock.tick(FPS)

        # DETECTO EVENTOS
        for event in pygame.event.get():
            if event.type == QUIT:
                terminar()

        # CUANDO PRESIONO TECLA
            if event.type == KEYDOWN:
                if event.key == K_UP or event.key == K_w:
                    move_up = True
                    move_down = False
                if event.key == K_DOWN or event.key == K_s:
                    move_down = True
                    move_up = False
                if event.key == K_r:
                    trick_stop = True

        # DISPAROS
                if event.key == K_SPACE:
                    if not laser:
                        laser = get_laser(block["rect"].midright,speed_laser)
                        disparo_sound.play()
                if event.key == K_ESCAPE:
                    terminar()

        # MUSICA
                if event.key == K_m:
                    if playing_music:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                    playing_music = not playing_music

        # PAUSA JUEGO
                if event.key == K_p:
                    if playing_music:
                        pygame.mixer.music.pause()
                        mostrar_texto(screen,"Pausa", fuente , CENTER_SCREEN , BLACK)
                        pygame.display.flip()
                    wait_user()
                    if playing_music:
                        pygame.mixer.music.unpause()

        # CUANDO LEVANTO TECLA
            if event.type == KEYUP:
                if event.key == K_UP or event.key == K_w:
                    move_up = False
                if event.key == K_DOWN or event.key == K_s:
                    move_down = False
                if event.key == K_r:
                    trick_stop = False

        # NUEVO EVENTO LOGO DE VIDAS
            if event.type == EVENT_NEW_LIFE:
                logo_vidas.append(get_blocks(full_vida_image,700,randint(0,HEIGHT - rec_height),rec_widht,rec_height))


        # ACTUALIZO DIRECCION DE LOS ENEMIGOS CUANDO REBOTA
        for enemie in enemies:
                if enemie["rect"].right >= WIDTH:
                    if enemie["dir"] == DR:
                        enemie["dir"] = choice(direcciones)
                    elif enemie["dir"] == UR:
                        enemie["dir"] = UL
                elif enemie["rect"].left <= 0:
                    if enemie["dir"] == UL:
                        enemie["dir"] = UR
                    elif enemie["dir"] == DL:
                        enemie["dir"] = choice(direcciones)
                elif enemie["rect"].top <= 0:
                    if enemie["dir"] == UL:
                        enemie["dir"] = choice(direcciones)
                    elif enemie["dir"] == UR:
                        enemie["dir"] = choice(direcciones)
                elif enemie["rect"].bottom >= HEIGHT:
                    if enemie["dir"] == DR:
                        enemie["dir"] = choice(direcciones)
                    elif enemie["dir"] == DL:
                        enemie["dir"] = choice(direcciones)


        # MUEVO LOS BLOQUES ENEMIGOS DE ACUERDO A SU DIRECCION
        for enemie in enemies:
            if not trick_stop:
                if enemie["dir"] == DR:
                    enemie["rect"].top += SPEED
                    enemie["rect"].left += SPEED
                if enemie["dir"] == DL:
                    enemie["rect"].top += SPEED
                    enemie["rect"].left -= SPEED
                if enemie["dir"] == UL:
                    enemie["rect"].top -= SPEED
                    enemie["rect"].left -= SPEED
                if enemie["dir"] == UR:
                    enemie["rect"].top -= SPEED
                    enemie["rect"].left += SPEED

        # MUEVO EL PERSONAJE
        if move_up and block["rect"].top - SPEED >= 0:
            block["rect"].top -= SPEED

        if move_down and block["rect"].bottom + SPEED <= HEIGHT:
            block["rect"].top += SPEED



        # DETECTAR COLISICIONES ENTRE PERSONAJE Y ENEMIGOS
    
        for enemie in enemies[:]:

            if detectar_colision(enemie["rect"], block["rect"]):
                enemies.remove(enemie)
                lives -= 1
                plop.play()
                texto_lives = fuente.render(f"Lives: {lives}", True , WHITE)
            if len(enemies) == 0:
                load_enemies(enemies, fantasma_1, 300,randint(0,HEIGHT - 
                rec_height), 50, 50)
            if lives == 0:
                is_running = False

        # DETECTAR COLISIONES ENTRE DISPARO Y ENEMIGOS
        if laser:
            if laser["rect"].right <= WIDTH:
                laser["rect"].move_ip(laser["speed_x"], 0)
            else:
                laser = None
        if laser:        
            colision = False
            for enemie in enemies[:]:
                if detectar_colision(enemie["rect"], laser["rect"]):
                    enemies.remove(enemie)
                    score += 10
                    texto_score = fuente.render(f"Score: {score}", True , WHITE)
                    colision = True
                    if len(enemies) == 0:
                        load_enemies(enemies, fantasma_1, 300,randint(0,HEIGHT - rec_height), 50, 50)

        # DETECTAR COLISION ENTRE DISPARO Y LOGO VIDA
            for logo_vida in logo_vidas[:]:
                if detectar_colision(logo_vida["rect"], laser["rect"]):
                    logo_vidas.remove(logo_vida)
                    lives += 1
                    texto_lives = fuente.render(f"Lives: {lives}", True , WHITE)
                    colision = True
                    if len(enemies) == 0:
                        load_enemies(enemies, fantasma_1, 300,randint(0,HEIGHT - rec_height), 50, 50)
            
            if colision:
                laser = None

        texto_lives,rect_lives = mostrar_valores("Lives", lives, WHITE, fuente, (700, HEIGHT - 25))
        texto_score,rect_score = mostrar_valores("Score", score, WHITE, fuente, (100, HEIGHT - 25))
        screen.fill(BLACK)
        screen.blit(fondo_pantalla,(0,0))
        dibujar_personajes(screen, enemies)
        dibujar_personajes(screen, logo_vidas)
        screen.blit(block["imagen"], block["rect"])
        screen.blit(texto_lives,rect_lives)
        screen.blit(texto_score,rect_score)

        if laser:
            pygame.draw.rect(screen,GOLD,laser["rect"])


        pygame.display.flip()

        
    pygame.mixer.music.stop()
    screen.fill(BLACK)
    end_sound.play()
    mostrar_texto(screen,f"Score: {score}",fuente,(WIDTH // 2 , 60), WHITE)
    mostrar_texto(screen,"Game Over",fuente,CENTER_SCREEN, RED)
    mostrar_texto(screen,"Presione tecla para continuar...",fuente,(WIDTH // 2, HEIGHT - 50), WHITE)
    pygame.display.flip()

    wait_user()

terminar()
