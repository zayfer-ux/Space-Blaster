import pygame
from personaje import Cubo
from enemigo import Enemigo
import random
import os
from bala import Bala

pygame.init()

ANCHO = 1000
ALTO = 800
VENTANA = pygame.display.set_mode([ANCHO,ALTO])
FPS = 60
FUENTE = pygame.font.SysFont("Comic Sans", 30)

jugando = True
reloj = pygame.time.Clock()  

vidas = 5
puntos = 0

tiempo_pasado = 0 
tiempo_entre_enemigos = 300

cubo = Cubo(ANCHO/2,ALTO-75)

enemigos = []
balas = []

ultima_bala = 0
tiempo_entre_balas = 500

enemigos.append(Enemigo(ANCHO/2, 100))


def crear_bala():
    global ultima_bala
    if pygame.time.get_ticks() - ultima_bala > tiempo_entre_balas:
        balas.append(Bala(cubo.rect.centerx, cubo.rect.centery))
        ultima_bala = pygame.time.get_ticks()
    
def gestionar_teclas(teclas):
    if teclas[pygame.K_a] and cubo.x > 0:
        cubo.x -= cubo.velocidad
    if teclas[pygame.K_d] and cubo.x + cubo.ancho < ANCHO:
        cubo.x += cubo.velocidad
    if teclas[pygame.K_SPACE]:
        crear_bala()

while jugando and vidas > 0:
    tiempo_pasado += reloj.tick(FPS)

    if tiempo_pasado > tiempo_entre_enemigos:
        enemigos.append(Enemigo(random.randint(0,ANCHO),-100))
        tiempo_pasado = 0
        
    eventos = pygame.event.get()
    teclas = pygame.key.get_pressed()
    
    texto_vida = FUENTE.render(f"Vidas: {vidas}", True, "white")
    texto_puntos = FUENTE.render(f"Puntos: {puntos}", True, "white")

    gestionar_teclas(teclas)

    for evento in eventos:
        if evento.type == pygame.QUIT:
            jugando = False 

    VENTANA.fill("black")
    cubo.dibujar(VENTANA)
 
    # Bucle de enemigos
    for enemigo in enemigos[:]:
        enemigo.dibujar(VENTANA)
        enemigo.movimiento()

        # Colisión con el jugador
        if pygame.Rect.colliderect(cubo.rect, enemigo.rect):
            vidas -= 1 
            print(f"Te quedan {vidas} vidas")
            if enemigo in enemigos:
                enemigos.remove(enemigo)
            continue 

        # Enemigo sale de la pantalla
        if enemigo.y + enemigo.alto > ALTO:
            if enemigo in enemigos:
                enemigos.remove(enemigo)
            continue

        # Colisión con balas
        for bala in balas[:]:
            if pygame.Rect.colliderect(bala.rect, enemigo.rect):
                puntos += 10 
                if enemigo in enemigos:
                    enemigos.remove(enemigo)
                if bala in balas:
                    balas.remove(bala)

    # Mover y dibujar las balas en la pantalla (Alineado con el bucle de enemigos)
    for bala in balas[:]:
        bala.dibujar(VENTANA)
        bala.movimiento()

    # Actualización de pantalla (Alineado DENTRO del bucle while principal)
    VENTANA.blit(texto_vida, (40,20))
    VENTANA.blit(texto_puntos, (20,50))
    
    pygame.display.update()

quit()