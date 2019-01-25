#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame, os
from bibliottt.opcion import *
#from twisted.internet import reactor

# Declaro antes de linea49 pantalla = iniciarPantalla(ventana)
colorNegro = (0,0,0)
colorGris = (192,192,192)
colorRojo = (250,0,0)
# ----------------------------------------------------------------

def salirDelJuego(ttt, indice_):
	try:
		reactor.stop()
	except: pass
	os._exit(0)

def escribirTitulo(pantalla_):
	fuenteTitulo = pygame.font.Font('bibliottt/AtoZ.ttf', 60)
	textoTitulo = 'TA TE TI'
	tituloFormateado = fuenteTitulo.render(textoTitulo, 1, colorRojo)
	pantalla_.blit(tituloFormateado, (263, 75))

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
	pygame.display.set_caption('Ta-Te-Ti de Carlitos')
	ventana = pygame.display.set_mode((800,600))
	pantalla = iniciarPantalla(ventana)

	fuenteMenu = pygame.font.Font('bibliottt/AtoZ.ttf', 40)
	opciones = [ 
				Opcion('Jugador vs Cpu', (215, 230), 'i1', funcionParaElegirLetra, fuenteMenu, ventana),
				Opcion('Jugador vs Jugador PC', (130, 285), 'i2', funcionParaElegirLetra, fuenteMenu, ventana),
				Opcion('Jugador vs Jugador LAN', (120, 335), 'i3', funcionParaElegirModoDeJuegoRED, fuenteMenu, ventana),
				Opcion('Salir', (345, 390), 'i4', salirDelJuego, fuenteMenu, ventana)
			   ]

	seleccionado = 0
	totalOP = 4
	posi_ = 'i-'
	pulsoTecla = False
	pygame.mouse.set_pos((400,180))
	respuesta = False
	while True:

		evento = pygame.event.get()
		
		for e in evento:
			if e.type == pygame.QUIT:
				try:
					reactor.stop()
				except: pass
				os._exit(0)

			if e.type == pygame.KEYDOWN:
				pygame.mouse.set_visible(False)
				pygame.mouse.set_pos((400,180))
				if e.key == pygame.K_UP:
					seleccionado -= 1
				
				if e.key == pygame.K_DOWN:
					seleccionado += 1

				if e.key == pygame.K_RETURN:
					#print 'llamada'
					if posi_ != 'i-':
						pulsoTecla = True
				else:

					if seleccionado < 1:
						seleccionado = totalOP
					elif seleccionado > totalOP:
						seleccionado = 1

					if seleccionado == 1:
						posi_ = 'i1'
					if seleccionado == 2:
						posi_ = 'i2'
					if seleccionado == 3:
						posi_ = 'i3'
					if seleccionado == 4:
						posi_ = 'i4'	

			elif e.type == pygame.MOUSEMOTION:
				pygame.mouse.set_visible(True)
				seleccionado = 0
				posi_ = 'i-'

			elif e.type == pygame.MOUSEBUTTONDOWN and (
				opciones[0].rect.collidepoint(pygame.mouse.get_pos()) or
				opciones[1].rect.collidepoint(pygame.mouse.get_pos()) or
				opciones[2].rect.collidepoint(pygame.mouse.get_pos()) or
				opciones[3].rect.collidepoint(pygame.mouse.get_pos())):
				#print 'llamada'
				pulsoTecla = True

		pygame.event.pump()
		ventana.blit(pantalla, (0, 0))

		for o in opciones:
			if o.rect.collidepoint( pygame.mouse.get_pos() ) or bool(o.indice == posi_):
				o.hover = True
				if pulsoTecla == True:
					#if posi_ == 'i4' or opciones[3].rect.collidepoint(pygame.mouse.get_pos()):
					#	o.funcion(ventana) 
					respuesta = o.funcion(ventana, o.indice)
					#pygame.display.flip()
					pulsoTecla = False
			else:
				o.hover = False

			o.imprimir()

		pygame.display.flip()
		mostrarPantalla(ventana, pantalla)
