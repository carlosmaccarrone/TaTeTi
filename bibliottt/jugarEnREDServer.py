#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame, os, random
from bibliottt.opcion import *
from twisted.internet import reactor, protocol, task
# [10]Estado(noseusa), [11]LetraServer, [12]LetraCliente, [13]VolverAJugar, [14]LetraGanadora, [15]Turno

colorNegro = (0,0,0)
colorGris = (192,192,192)
colorRojo = (250,0,0)
colorNaranja = (250,150,50)

ganador = None
casilleros = [' '] * 20
cantiO_ = 0
cantiX_ = 0


def funcionParaSalirAlMenuSERVENT(ventana_):
	global casilleros, REACTORBANDERASERVER, conexion_

	casilleros[13] = False

	try:
		conexion_.pasadorBandera = True
		conexion_.transport.write(str( casilleros ))	
	except: pass
	
	for i in range(1,20):
		casilleros[i] = ' '		
	REACTORBANDERASERVER = False

def funcionParaSalirDosSERVENT():
	global casilleros, REACTORBANDERASERVER, conexion_
	try:
		conexion_.pasadorBandera = True
	except: pass
	for i in range(1,20):
		casilleros[i] = ' '	
	REACTORBANDERASERVER = False

def funcionParaVolverAJugarSERVENT(ventana_):
	global casilleros, conexion_	

	if casilleros[13] is False:
		funcionParaSalirDosSERVENT()
		return

	if casilleros[14] is not letraServer:
		casilleros[13] = True
		try:
			conexion_.transport.write(str( casilleros ))
		except: pass

	if casilleros[14] is letraServer:
		conexion_.pasadorBandera = True
		casilleros[15] = casilleros[11]
		if casilleros[13] is True:
			for i in range(1,10):
				casilleros[i] = ' '
			try:	
				conexion_.transport.write( str(casilleros) )
			except: pass
		casilleros[13] = None


def esCasillaLibre(_casilleros, casilla):
	return _casilleros[casilla] == ' '

def seLlenoTablero():
	global casilleros
	for casilla in range(1, 10):
		if esCasillaLibre(casilleros, casilla):
			return False
	return True

def esGanador(ta, le):
	return (    (ta[7] == le and ta[8] == le and ta[9] == le) or
				(ta[4] == le and ta[5] == le and ta[6] == le) or
				(ta[1] == le and ta[2] == le and ta[3] == le) or
				(ta[7] == le and ta[4] == le and ta[1] == le) or
				(ta[8] == le and ta[5] == le and ta[2] == le) or
				(ta[9] == le and ta[6] == le and ta[3] == le) or
				(ta[7] == le and ta[5] == le and ta[3] == le) or
				(ta[9] == le and ta[5] == le and ta[1] == le)   )

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

def dibujarEstadoSERVENT(tablero):
	global cantiO_, cantiX_, casilleros, ganador

	if ganador is None:
		mensaje = 'Turno de ' + casilleros[15]
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

def mostrarTableroSERVENT(ventana_, tablero):

	fuenteParaMenu = pygame.font.Font('bibliottt/AtoZ.ttf', 40)
	fuenteParaVolver = pygame.font.Font('bibliottt/AtoZ.ttf', 25)
	opcionMenu = [ 
		Opcion('Menu', (650, 540), 'menu', funcionParaSalirAlMenuSERVENT, fuenteParaMenu, ventana_)
					   ]

	opcionesVolverAJugar = [
		Opcion('Si', (200, 560), 'si', funcionParaVolverAJugarSERVENT, fuenteParaVolver, ventana_),
		Opcion('No', (250, 560), 'no', funcionParaSalirAlMenuSERVENT, fuenteParaVolver, ventana_)
									]

	dibujarEstadoSERVENT(tablero)
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

def clickTableroSERVENT(tablero):
	global conexion_, letraServer, ganador, cantiO_, cantiX_

	mouseX, mouseY = pygame.mouse.get_pos()
	casilla, fila, col = posicionTablero(mouseX, mouseY)

	if casilla is None:	return
	if casilleros[casilla] == 'X' or casilleros[casilla] == 'O': return

	dibujarJugada(tablero, fila, col, casilla, letraServer)

	if juegoGanado(tablero):
		casilleros[14] = ganador
		casilleros[15] = ganador
		conexion_.pasadorBandera = False
	if seLlenoTablero():
		casilleros[15] = casilleros[14]
		conexion_.pasadorBandera = False

	if casilleros[15] is 'X':
		casilleros[15] = 'O'
	elif casilleros[15] is 'O':
		casilleros[15] = 'X'

	if esGanador(casilleros, casilleros[11]):
		if casilleros[11] == 'X':
			cantiX_ += 1
		elif casilleros[11] == 'O':
			cantiO_ += 1

	conexion_.transport.write(str( casilleros ))

	return True

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

def jugarContraJugadorSERVENT(ventana_):
	global REACTORBANDERASERVER

	if REACTORBANDERASERVER:
		global ganador, casilleros, letraServer, conexion_
		tableroExp = inicializarTablero(ventana_)
		ventana_.blit(tableroExp, (0, 0))

		if not juegoGanado(tableroExp):
			ganador = None

		if casilleros[1] is not ' ':
			if casilleros[1] is 'X':
				pygame.draw.line(tableroExp, colorNegro, (61,61), (105,105), 10)
				pygame.draw.line(tableroExp, colorNegro, (105,61), (61,105), 10)
			elif casilleros[1] is 'O':
				pygame.draw.circle(tableroExp, colorNegro, (83,83), 44, 10)

		if casilleros[2] is not ' ':
			if casilleros[2] is 'X':
				pygame.draw.line(tableroExp, colorNegro, (227,61), (271,105), 10)
				pygame.draw.line(tableroExp, colorNegro, (271,61), (227,105), 10)
			elif casilleros[2] is 'O':
				pygame.draw.circle(tableroExp, colorNegro, (249,83), 44, 10)

		if casilleros[3] is not ' ':
			if casilleros[3] is 'X':
				pygame.draw.line(tableroExp, colorNegro, (393,61), (437,105), 10)
				pygame.draw.line(tableroExp, colorNegro, (437,61), (393,105), 10)
			elif casilleros[3] is 'O':
				pygame.draw.circle(tableroExp, colorNegro, (415,83), 44, 10)

		if casilleros[4] is not ' ':
			if casilleros[4] is 'X':
				pygame.draw.line(tableroExp, colorNegro, (61,227), (105,271), 10)
				pygame.draw.line(tableroExp, colorNegro, (105,227), (61,271), 10)
			elif casilleros[4] is 'O':
				pygame.draw.circle(tableroExp, colorNegro, (83,249), 44, 10)

		if casilleros[5] is not ' ':
			if casilleros[5] is 'X':
				pygame.draw.line(tableroExp, colorNegro, (227,227), (271,271), 10)
				pygame.draw.line(tableroExp, colorNegro, (271,227), (227,271), 10)
			elif casilleros[5] is 'O':
				pygame.draw.circle(tableroExp, colorNegro, (249,249), 44, 10)

		if casilleros[6] is not ' ':
			if casilleros[6] is 'X':
				pygame.draw.line(tableroExp, colorNegro, (393,227), (437,271), 10)
				pygame.draw.line(tableroExp, colorNegro, (437,227), (393,271), 10)
			elif casilleros[6] is 'O':
				pygame.draw.circle(tableroExp, colorNegro, (415,249), 44, 10)

		if casilleros[7] is not ' ':
			if casilleros[7] is 'X':
				pygame.draw.line(tableroExp, colorNegro, (61,393), (105,437), 10)
				pygame.draw.line(tableroExp, colorNegro, (105,393), (61,437), 10)
			elif casilleros[7] is 'O':
				pygame.draw.circle(tableroExp, colorNegro, (83,415), 44, 10)

		if casilleros[8] is not ' ':
			if casilleros[8] is 'X':
				pygame.draw.line(tableroExp, colorNegro, (227,393), (271,437), 10)
				pygame.draw.line(tableroExp, colorNegro, (271,393), (227,437), 10)
			elif casilleros[8] is 'O':
				pygame.draw.circle(tableroExp, colorNegro, (249,415), 44, 10)

		if casilleros[9] is not ' ':
			if casilleros[9] is 'X':
				pygame.draw.line(tableroExp, colorNegro, (393,393), (437,437), 10)
				pygame.draw.line(tableroExp, colorNegro, (437,393), (393,437), 10)
			elif casilleros[9] is 'O':
				pygame.draw.circle(tableroExp, colorNegro, (415,415), 44, 10)

		eventos = pygame.event.get()

		for e in eventos:
			if e.type == pygame.QUIT:
				try:
					reactor.stop()
				except: pass
				os._exit(0)

			if e.type is pygame.MOUSEBUTTONDOWN:
				if casilleros[15] == letraServer:
					if not juegoGanado(tableroExp) and not seLlenoTablero():
							clickTableroSERVENT(tableroExp)

		mostrarTableroSERVENT(ventana_, tableroExp)


class Conexiones(protocol.Protocol):

	pasadorBandera = True

	def __init__(self, fabrica_, tabla_=[' '] * 20):
		self.fabrica = fabrica_
		self.elTablero = tabla_
		casilleros = self.elTablero
		global conexion_
		conexion_ = self

	def connectionMade(self):
		self.elTablero[10] = True
		self.elTablero[11] = letraServer
		self.elTablero[12] = letraClient 
		self.elTablero[13] = None
		self.elTablero[14] = None
		self.elTablero[15] = letraServer
		self.transport.write( str(self.elTablero) )
		global casilleros
		casilleros = self.elTablero
		global cantiX_, cantiO_
		cantiX_ = 0
		cantiO_ = 0

	def dataReceived(self, datos):
		global casilleros
		var = datos.split(", ")

		if len(var) == 39:
			#print datos
			sumador = 0
			for i in range(19, 38):
				if 'X' in var[i]:
					self.elTablero[sumador] = 'X'
				elif 'O' in var[i]:
					self.elTablero[sumador] = 'O'
				elif 'True' in var[i]:
					self.elTablero[sumador] = True
				elif 'False' in var[i]:
					self.elTablero[sumador] = False
				elif 'None' in var[i]:
					self.elTablero[sumador] = None
				else:
					self.elTablero[sumador] = ' '
				sumador += 1	

		if len(var) == 20:
			for i in range(1, 20):
				if 'X' in var[i]:
					self.elTablero[i] = 'X'
				elif 'O' in var[i]:
					self.elTablero[i] = 'O'
				elif 'True' in var[i]:
					self.elTablero[i] = True
				elif 'False' in var[i]:
					self.elTablero[i] = False
				elif 'None' in var[i]:
					self.elTablero[i] = None
				else:
					self.elTablero[i] = ' '

		if self.pasadorBandera:
			casilleros = self.elTablero

			if esGanador(casilleros, casilleros[12]):
				if casilleros[12] == 'X':
					global cantiX_
					cantiX_ += 1
				elif casilleros[12] == 'O':
					global cantiO_
					cantiO_ += 1

class Fabrica(protocol.Factory):

	def buildProtocol(self, dir):
		return Conexiones(self)



def funcionDisparadoraSERVENT(ventana, letra_):
	from twisted.internet import reactor, protocol, task
	global letraServer, letraClient, tickS

	if letra_ is 'X':
		letraServer = 'X'
		letraClient = 'O'
	elif letra_ is 'O':
		letraServer = 'O'
		letraClient = 'X'	

	casilleros = [' '] * 20
	casilleros[10] = True			# Estado
	casilleros[11] = letraServer	# Letra server
	casilleros[12] = letraClient	# Letra cliente
	casilleros[13] = None 			# Volver a jugar
	casilleros[14] = None 			# Letra ganadora
	casilleros[15] = letraServer	# Turno

	framesPerSecond = 30.0
	tickS = task.LoopingCall(jugarContraJugadorSERVENT, ventana)
	tickS.start(1.0 / framesPerSecond)

	try:
		reactor.run(installSignalHandlers=False)
	except: pass

def SERVENTATETI(ventana, letra_):
	global REACTORBANDERASERVER, ts, tickS
	import threading

	try:
		if ts:
			REACTORBANDERASERVER = True
			print 'Reutilizando thread server'
	except Exception as e:
		REACTORBANDERASERVER = True
		ts = threading.Thread(target=funcionDisparadoraSERVENT, args=(ventana, letra_))
		ts.start()		

#	REACTORBANDERASERVER = True

#	t = threading.Thread(target=funcionDisparadoraSERVENT, args=(ventana, letra_))
#	t.start()

	while REACTORBANDERASERVER:
		pass

	#tickS.stop()

	return True
