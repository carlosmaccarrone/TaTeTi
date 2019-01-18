#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame, sys, random
from bibliottt.opcion import *

colorNegro = (0,0,0)
colorGris = (192,192,192)
colorRojo = (250,0,0)
colorNaranja = (250,150,50)

def quienVaPrimero():
	if random.randint(0, 1) == 0:
		return 'X'
	else:
		return 'O'

turno = quienVaPrimero()
ganador = None
casilleros = [' '] * 10
juegoEnCurso = True
volverAJugar = None
cantiO_ = 0
cantiX_ = 0

def funcionParaSalirAlMenu(ventana_):
	global juegoEnCurso
	juegoEnCurso = False

def funcionParaVolverAJugar(ventana_):
	global volverAJugar
	volverAJugar = True

def esCasillaLibre(_casilleros, casilla):
	return _casilleros[casilla] == ' '

def seLlenoTablero():
	global casilleros
	for casilla in range(1, 10):
		if esCasillaLibre(casilleros, casilla):
			return False
	return True

def inicializarTablero(ventana_,):
	fondoPantalla = pygame.Surface(ventana_.get_size())
	fondoPantalla = fondoPantalla.convert()
	fondoPantalla.fill(colorGris)

	# lineas verticales
	pygame.draw.line(fondoPantalla, colorNegro, (166,0), (166,500), 10)
	pygame.draw.line(fondoPantalla, colorNegro, (332,0), (332,500), 10)
	# lineas horizontales
	pygame.draw.line(fondoPantalla, colorNegro, (0,166), (500,166), 10)
	pygame.draw.line(fondoPantalla, colorNegro, (0,332), (500,332), 10)
	# esquema
	pygame.draw.line(fondoPantalla, colorRojo, (501,0), (501,501), 2) #vertical
	pygame.draw.line(fondoPantalla, colorRojo, (0,501), (502,501), 2) #horizontal
	pygame.draw.line(fondoPantalla, colorNaranja, (501,503), (501,600), 2)

	return fondoPantalla

def dibujarEstado(tablero):
	global cantiO_, cantiX_

	if ganador is None:
		mensaje = 'Turno de ' + turno
	else:
		mensaje = 'Ganador ' + ganador
	if seLlenoTablero() and not ganador:
		mensaje = 'Empate'

	font = pygame.font.Font(None, 24)
	text = font.render(mensaje, 1, colorRojo)

	tablero.fill(colorGris, (0, 510, 100, 25))
	tablero.blit(text, (10, 510))
	
	mensajeCantidadesX = 'X: ' + str( cantiX_ )
	mensajeCantidadesO = 'O: ' + str( cantiO_)
	fuenteNone = pygame.font.Font(None, 48)
	textoCantidadesX = fuenteNone.render(mensajeCantidadesX, 1, colorRojo)
	textoCantidadesO = fuenteNone.render(mensajeCantidadesO, 1, colorRojo)
	tablero.fill(colorGris, (550, 0, 100, 800))
	tablero.blit(textoCantidadesX, (550, 25))
	tablero.blit(textoCantidadesO, (550, 75))


	if juegoGanado(tablero) or seLlenoTablero():
		tablero.fill(colorGris, (0, 535, 450, 25))
		volverAJugar_msj = 'Volver a jugar? ' 
		fuenteVolver = pygame.font.Font(None, 24)
		textoVolver = fuenteVolver.render(volverAJugar_msj, 1, colorNegro,)
		tablero.blit(textoVolver, (185, 530))

def mostrarTablero(ventana_, tablero):

	fuenteParaMenu = pygame.font.Font('bibliottt/AtoZ.ttf', 40)
	fuenteParaVolver = pygame.font.Font('bibliottt/AtoZ.ttf', 25)
	opcionMenu = [ 
		Opcion('Menu', (650, 540), 'menu', funcionParaSalirAlMenu, fuenteParaMenu, ventana_)
					   ]

	opcionesVolverAJugar = [
		Opcion('Si', (200, 560), 'si', funcionParaVolverAJugar, fuenteParaVolver, ventana_),
		Opcion('No', (250, 560), 'no', funcionParaSalirAlMenu, fuenteParaVolver, ventana_)
									]

	dibujarEstado(tablero)
	ventana_.blit(tablero, (0,0))
	
	for o in opcionMenu:
		if o.rect.collidepoint( pygame.mouse.get_pos() ):
			o.hover = True
			if pygame.mouse.get_pressed()[0]:
				o.funcion(ventana_)
		else:
			o.hover = False

		o.imprimir()

	if juegoGanado(tablero) or seLlenoTablero():

		for o in opcionesVolverAJugar:
			if o.rect.collidepoint( pygame.mouse.get_pos() ):
				o.hover = True
				if pygame.mouse.get_pressed()[0]:
					o.funcion(ventana_)
			else:
				o.hover = False

			o.imprimir()

	pygame.display.flip()

def posicionTablero(mouseX, mouseY):
	fila = None
	col = None

	if mouseY < 166:
		fila = 0
	elif mouseY < 332:
		fila = 1
	elif mouseY < 500:
		fila = 2

	if mouseX < 166:
		col = 0
	elif mouseX < 332:
		col = 1
	elif mouseX < 500:
		col = 2

	casilla = None
	if fila is not None and col is not None:
		if fila is 0 and col is 0: casilla = 1
		if fila is 0 and col is 1: casilla = 2
		if fila is 0 and col is 2: casilla = 3
		if fila is 1 and col is 0: casilla = 4
		if fila is 1 and col is 1: casilla = 5
		if fila is 1 and col is 2: casilla = 6
		if fila is 2 and col is 0: casilla = 7
		if fila is 2 and col is 1: casilla = 8
		if fila is 2 and col is 2: casilla = 9

	return casilla, fila, col

def dibujarJugada(tablero, tFila, tCol, casilla, letra):
	centroX = tCol * 166 + 83
	centroY = tFila * 166 + 83

	if letra == 'O':
		pygame.draw.circle(tablero, colorNegro, (centroX, centroY), 44, 10)
	else:
		pygame.draw.line(tablero, colorNegro, (centroX - 22, centroY - 22), \
			(centroX + 22, centroY + 22), 10)

		pygame.draw.line(tablero, colorNegro, (centroX + 22, centroY - 22), \
			(centroX - 22, centroY + 22), 10)

	casilleros[casilla] = letra


def clickTablero(tablero):
	global turno

	mouseX, mouseY = pygame.mouse.get_pos()
	casilla, fila, col = posicionTablero(mouseX, mouseY)

	if casilla is None:	return
	if casilleros[casilla] == 'X' or casilleros[casilla] == 'O': return

	dibujarJugada(tablero, fila, col, casilla, turno)

	if turno == 'X':
		turno = 'O'
	else:
		turno = 'X'


def juegoGanado(tablero):
	global ganador

# FILAS ..........................
	if casilleros[1] == casilleros[2] == casilleros[3] and casilleros[1] is not ' ':
		pygame.draw.line(tablero, colorRojo, (0, 83), (500, 83), 5)
		ganador = casilleros[1]
		return True

	if casilleros[4] == casilleros[5] == casilleros[6] and casilleros[4] is not ' ':
		pygame.draw.line(tablero, colorRojo, (0, 249), (500, 249), 5)
		ganador = casilleros[4]
		return True

	if casilleros[7] == casilleros[8] == casilleros[9] and casilleros[7] is not ' ':
		pygame.draw.line(tablero, colorRojo, (0, 415), (500, 415), 5)
		ganador = casilleros[7]
		return True

# COLUMNAS ........................
	if casilleros[1] == casilleros[4] == casilleros[7] and casilleros[1] is not ' ':
		pygame.draw.line(tablero, colorRojo, (83, 0), (83, 500), 5)
		ganador = casilleros[1]
		return True

	if casilleros[2] == casilleros[5] == casilleros[8] and casilleros[2] is not ' ':
		pygame.draw.line(tablero, colorRojo, (249, 0), (249, 500), 5)
		ganador = casilleros[2]
		return True

	if casilleros[3] == casilleros[6] == casilleros[9] and casilleros[3] is not ' ':
		pygame.draw.line(tablero, colorRojo, (415, 0), (415, 500), 5)
		ganador = casilleros[3]
		return True

# DIAGONAL IZQUIERDA A DERECHA .................
	if casilleros[1] == casilleros[5] == casilleros[9] and casilleros[1] is not ' ':
		pygame.draw.line(tablero, colorRojo, (83,83), (415,415), 5)
		ganador = casilleros[1]
		return True

# DIAGONAL DERECHA A IZQUIERDA ...................
	if casilleros[3] == casilleros[5] == casilleros[7] and casilleros[3] is not ' ':
		pygame.draw.line(tablero, colorRojo, (415,83), (83,415), 5)
		ganador = casilleros[3]
		return True

def jugarContraJugadorPC(ventana_, letraJugador):
	global turno, ganador, casilleros, juegoEnCurso, volverAJugar, cantiO_, cantiX_
	turno = quienVaPrimero()
	ganador = None
	casilleros = [' '] * 10
	juegoEnCurso = True
	volverAJugar = None
	cantiO_ = 0
	cantiX_ = 0
	# ----------------------------------------------------------------
	tableroContraCPU = inicializarTablero(ventana_)
	ventana_.blit(tableroContraCPU, (0, 0))
	pygame.display.update()
	# ----------------------------------------------------------------



	while juegoEnCurso:
		eventos = pygame.event.get()

		for e in eventos:
			if e.type == pygame.QUIT:
				try:
					reactor.stop()
				except: pass				
				sys.exit(0)

			elif e.type is pygame.MOUSEBUTTONDOWN:
				if not juegoGanado(tableroContraCPU) and not seLlenoTablero():
					clickTablero(tableroContraCPU)

			respuestaDeGanar = juegoGanado(tableroContraCPU)
			respuestaDeEmpatar = seLlenoTablero()

			if respuestaDeGanar and volverAJugar:
				casilleros = [' '] * 10
				turno = ganador
				if ganador == 'X':	cantiX_ += 1
				else:				cantiO_ += 1
				ganador = None
				volverAJugar = None
				tableroContraCPU = inicializarTablero(ventana_)

			if respuestaDeEmpatar and volverAJugar:
				casilleros = [' '] * 10
				if turno == 'X':	turno = 'O'
				else:				turno = 'X'
				ganador = None
				volverAJugar = None
				tableroContraCPU = inicializarTablero(ventana_)


			mostrarTablero(ventana_, tableroContraCPU)


	return True