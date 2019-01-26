#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame, sys
from scripts.opcion import *

colorNegro = (0,0,0)
colorGris = (192,192,192)
colorRojo = (250,0,0)
# ----------------------------------------------------------------

def salirDelJuego(ttt):
	sys.exit(0)

def escribirTitulo(pantalla_):
	fuenteTitulo = pygame.font.Font('AtoZ.ttf', 60)
	textoTitulo = 'TA TE TI en RED'
	tituloFormateado = fuenteTitulo.render(textoTitulo, 1, colorRojo)
	pantalla_.blit(tituloFormateado, (160, 75))

def mostrarPantalla(ventana_, pantalla_):
	escribirTitulo(pantalla_)
	ventana_.blit(pantalla_, (0,0))

def iniciarPantalla(ventana_):
	fondoPantalla = pygame.Surface(ventana_.get_size())
	fondoPantalla = fondoPantalla.convert()
	fondoPantalla.fill(colorGris)
	return fondoPantalla

if __name__ == '__main__':
	pygame.init()
	pygame.display.set_caption('Ta Te Ti en RED')
	ventana = pygame.display.set_mode((800,600))
	pantalla = iniciarPantalla(ventana)

	fuenteMenu = pygame.font.Font('AtoZ.ttf', 40)

	opciones = [ 
				Opcion('Crear partida', (230, 230), funcionParaElegirLetra, fuenteMenu, ventana),
				Opcion('Unirse a partida', (205, 285), funcionMostrarPantallaParaUnirse, fuenteMenu, ventana),
				Opcion('Salir', (345, 390), salirDelJuego, fuenteMenu, ventana)
			   ]


	pulsoTecla = False

	while True:

		evento = pygame.event.get()

		for e in evento:
			if e.type == pygame.MOUSEBUTTONDOWN and (
				opciones[0].rect.collidepoint(pygame.mouse.get_pos()) or
				opciones[1].rect.collidepoint(pygame.mouse.get_pos()) or
				opciones[2].rect.collidepoint(pygame.mouse.get_pos())):
				pulsoTecla = True

		for o in opciones:
			if o.rect.collidepoint( pygame.mouse.get_pos() ):
				o.hover = True
				if pulsoTecla is True:
					o.funcion(ventana)
					pulsoTecla = False
			else:
				o.hover = False

			o.imprimir()

		pygame.display.flip()
		mostrarPantalla(ventana, pantalla)
