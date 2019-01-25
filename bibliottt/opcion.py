#!/usr/bin/python
# -*- coding: utf-8 -*-

class Opcion:
	hover = False

	def __init__(self, texto_, posicion, indice_, funcion_, fuente_, ventana_):
		self.indice = indice_
		self.funcion = funcion_
		self.fuente = fuente_
		self.ventana = ventana_
		self.texto = texto_
		self.pos = posicion
		self.establecerRect()
		self.imprimir()

	def imprimir(self):
		self.establecerRepr()
		self.ventana.blit(self.repr, self.rect)

	def establecerRepr(self):
		self.repr = self.fuente.render(self.texto, True, self.traeColor())

	def traeColor(self):
		if self.hover:
			return (200, 150, 50)
		else:
			return (0, 0, 0)

	def establecerRect(self):
		self.establecerRepr()
		self.rect = self.repr.get_rect()
		self.rect.topleft = self.pos



# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------
# -------------------------------- 		BUSCAR IP DE RED 	 	---------------------------------
# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------

import os, socket

if os.name != "nt":
    import fcntl
    import struct

    def get_interface_ip(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s',
                                ifname[:15]))[20:24])

def get_lan_ip():
    ip = socket.gethostbyname(socket.gethostname())
    if ip.startswith("127.") and os.name != "nt":
        interfaces = [
            "eth0",
            "eth1",
            "eth2",
            "wlan0",
            "wlan1",
            "wifi0",
            "ath0",
            "ath1",
            "ppp0",
            "wlp3s0",
            "enp0s25"
            ]
        for ifname in interfaces:
            try:
                ip = get_interface_ip(ifname)
                break
            except IOError:
                pass
    return ip


# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------
# --------------------------------		FIN DEL COMUNICADO 		  --------------------------------
# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------


import pygame
from bibliottt.jugarContraCPU import *
from bibliottt.jugarContraJugadorPC import *
from bibliottt.jugarEnREDServer import *
from bibliottt.jugarEnREDCliente import *
from twisted.internet import reactor

# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------
# -------------------------------- SELECCIONAR PUERTO PARA CREAR ---------------------------------
# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------


# Declaro antes de pantalla = _iniciarPantallaElegir(ventana)
colorPlaceholder = (128,128,128)


def funcionParaSalirAlMenuCrearRED(ventana_):
	global volverAlMenuUnirseRED
	volverAlMenuUnirseRED = True

def seleccionarPuertoParaCrear(ventana, letra):
	global volverAlMenuUnirseRED
	pygame.init()
	pygame.display.set_caption('Ta-Te-Ti de Carlitos')
	ventana = pygame.display.set_mode((800,600))
	pygame.key.set_repeat(150, 50)

	fuenteParaMenu = pygame.font.Font('bibliottt/AtoZ.ttf', 40)
	opcionMenu = [
		Opcion('Menu', (650, 540), 'menu', funcionParaSalirAlMenuCrearRED, fuenteParaMenu, ventana)
					   ]

	fuenteInput = pygame.font.Font(None, 40)
	inputTexto = pygame.Rect(209, 300, 250, 40)

	color = pygame.Color(250,0,0)

	cantidadMaximaDigitos = int(5)
	texto = 'Ej: 25000 o 8484'

	IPSERVENT = get_lan_ip()
	puertoEscuchado = None

	volverAlMenuUnirseRED = False
	
	while not volverAlMenuUnirseRED:
		if len(texto) is 0:
			texto = 'Ej: 25000 o 8484'

		evento = pygame.event.get()
		#print len(texto)
		for e in evento:

			if e.type == pygame.QUIT:
				try:
					reactor.stop()
				except: pass		
				os._exit(0)

			if e.type == pygame.KEYDOWN:
				if texto is 'Ej: 25000 o 8484':
					texto = ''
				
				if e.key == pygame.K_RETURN:
					try:
						puertoEscuchado = reactor.listenTCP(int(texto), Fabrica())
						banderaDePuerto = True
					except Exception as e:
						banderaDePuerto = False
						print e

					if banderaDePuerto:
						volverAlMenuUnirseRED = SERVENTATETI(ventana, letra)
						texto = ''
				elif e.key == pygame.K_BACKSPACE:
					texto = texto[:-1]
				else:
					if len(texto) < cantidadMaximaDigitos and\
						e.unicode in '0 1 2 3 4 5 6 7 8 9 . :'.split():
						texto += e.unicode

		try:
			puertoEscuchado.stopListening()
		except: pass

		ventana.fill(colorGris)

		fuenteParaUnirse = pygame.font.Font('bibliottt/AtoZ.ttf', 24)
		textoUnirseAUnaPartidaUNO = 'escriba el puerto en el que'
		textoUnirseAUnaPartidaFFUNO = fuenteParaUnirse.render(textoUnirseAUnaPartidaUNO, True, colorRojo)
		ventana.blit(textoUnirseAUnaPartidaFFUNO, (209, 200))
		textoUnirseAUnaPartidaDOS = 'quiere crear su servidor de tateti'
		textoUnirseAUnaPartidaFFDOS = fuenteParaUnirse.render(textoUnirseAUnaPartidaDOS, True, colorRojo)
		ventana.blit(textoUnirseAUnaPartidaFFDOS, (209, 230))
		fuenteParaUnirseDOS = pygame.font.Font(None, 24)
		textoUnirseAUnaPartidaTRES = '(1024>puerto<65535, si el puerto esta siendo utilizado intente con otro)'
		textoUnirseAUnaPartidaTRES = fuenteParaUnirseDOS.render(textoUnirseAUnaPartidaTRES, True, colorRojo)
		ventana.blit(textoUnirseAUnaPartidaTRES, (209, 260))

		fuenteParaTextoIp = pygame.font.Font(None, 24)
		textoSobreIP = 'Tu ip local es: ' + str(IPSERVENT)
		textoSobreIP = fuenteParaTextoIp.render(textoSobreIP, True, colorRojo)
		ventana.blit(textoSobreIP, (209, 400))

		# me quedé acá
		if texto is 'Ej: 25000 o 8484':
			superficieTexto = fuenteInput.render(texto, True, colorPlaceholder)
		else:
			superficieTexto = fuenteInput.render(texto, True, color)

		widthMaxTexto = int(250)
		inputTexto.w = widthMaxTexto

		ventana.blit(superficieTexto, (inputTexto.x+4, inputTexto.y+8))
		pygame.draw.rect(ventana, color, inputTexto, 3)


		for o in opcionMenu:
			if o.rect.collidepoint( pygame.mouse.get_pos() ):
				o.hover = True
				if pygame.mouse.get_pressed()[0]:
					o.funcion(ventana)
					volverAlMenuUnirseRED = True
			else:
				o.hover = False

			o.imprimir()

	
		pygame.display.flip()

	return True	

# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------
# --------------------------------		FIN DEL COMUNICADO 		  --------------------------------
# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------





# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------
# --------------------------------			ELEGIR LETRA		  --------------------------------
# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------

# Declaro antes de pantalla = _iniciarPantallaElegir(ventana)
colorNegro = (0,0,0)
colorGris = (192,192,192)
colorRojo = (250,0,0)
# ----------------------------------------------------------------

def _escribirTituloElegir(pantalla_, letra_):

	fuenteTitulo = pygame.font.Font(None, 40)
	textoTitulo = 'Seleccione su letra'
	tituloFormateado = fuenteTitulo.render(textoTitulo, 1, colorRojo)
	pantalla_.blit(tituloFormateado, (263, 75))

	if letra_ is None:
		pygame.draw.circle(pantalla_, colorNegro, (250, 300), 34, 10)

		pygame.draw.line(pantalla_, colorNegro, (528, 278), (572, 322), 10)
		pygame.draw.line(pantalla_, colorNegro, (572, 278), (528, 322), 10)

	elif letra_ is 'O':
		pygame.draw.circle(pantalla_, colorRojo, (250, 300), 34, 10)

		pygame.draw.line(pantalla_, colorNegro, (528, 278), (572, 322), 10)
		pygame.draw.line(pantalla_, colorNegro, (572, 278), (528, 322), 10)

	elif letra_ is 'X':
		pygame.draw.circle(pantalla_, colorNegro, (250, 300), 34, 10)

		pygame.draw.line(pantalla_, colorRojo, (528, 278), (572, 322), 10)
		pygame.draw.line(pantalla_, colorRojo, (572, 278), (528, 322), 10)


def _mouseSelectorElegir(varX, varY):
	if varX > 210 and varX < 290:
		if varY > 255 and varY < 340:
			return 'O'

	if varX > 515 and varX < 585:
		if varY > 255 and varY < 340:
			return 'X'

def _mostrarPantallaElegir(ventana_, pantalla_):
	varX,varY = pygame.mouse.get_pos()
	letra = _mouseSelectorElegir(varX, varY)

	_escribirTituloElegir(pantalla_, letra)
	ventana_.blit(pantalla_, (0,0))


def _iniciarPantallaElegir(ventana_):
	fondoPantalla = pygame.Surface(ventana_.get_size())
	fondoPantalla = fondoPantalla.convert()
	fondoPantalla.fill(colorGris)
	return fondoPantalla


def funcionParaElegirLetra(ventana, tipoDeJuego):
	pygame.init()
	pygame.display.set_caption('Ta-Te-Ti de Carlitos')
	pygame.mouse.set_visible(True)
	pantalla = _iniciarPantallaElegir(ventana)

	volverAlMenu = False
	funcionDejuego = None
	if tipoDeJuego == 'i1':
		funcionDejuego = jugarContraCPU
	if tipoDeJuego == 'i2':
		funcionDejuego = jugarContraJugadorPC
	if tipoDeJuego == 'Crear':
		funcionDejuego = seleccionarPuertoParaCrear

	while True:

		evento = pygame.event.get()

		for e in evento:
			if e.type == pygame.QUIT:
				try:
					reactor.stop()
				except: pass		
				os._exit(0)

			if e.type == pygame.MOUSEBUTTONDOWN:
				varX,varY = pygame.mouse.get_pos()
				if varX > 210 and varX < 290:
					if varY > 255 and varY < 340:
						if funcionDejuego is not None:
							volverAlMenu = funcionDejuego(ventana, 'O')

				if varX > 515 and varX < 585:
					if varY > 255 and varY < 340:
						if funcionDejuego is not None:
							volverAlMenu = funcionDejuego(ventana, 'X')

		if volverAlMenu:
			break

		pygame.event.pump()
		ventana.blit(pantalla, (0, 0))

		if not volverAlMenu:
			pygame.display.flip()

		_mostrarPantallaElegir(ventana, pantalla)

	return True
# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------
# --------------------------------		FIN DEL COMUNICADO 		  --------------------------------
# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------
# --------------------------------FUNCION MOSTRAR PANTALLA UNIRSE---------------------------------
# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------

# Declaro antes de pantalla = _iniciarPantallaElegir(ventana)
colorPlaceholder = (128,128,128)


def funcionParaSalirAlMenuUnirseRED(ventana_):
	global volverAlMenuUnirseRED
	volverAlMenuUnirseRED = True

def funcionMostrarPantallaParaUnirse(ventana):
	global volverAlMenuUnirseRED
	pygame.init()
	pygame.display.set_caption('Ta-Te-Ti de Carlitos')
	ventana = pygame.display.set_mode((800,600))
	pygame.key.set_repeat(150, 50)

	fuenteParaMenu = pygame.font.Font('bibliottt/AtoZ.ttf', 40)
	opcionMenu = [
		Opcion('Menu', (650, 540), 'menu', funcionParaSalirAlMenuUnirseRED, fuenteParaMenu, ventana)
					   ]

	fuenteInput = pygame.font.Font(None, 40)
	inputTexto = pygame.Rect(209, 300, 362, 40)

	color = pygame.Color(250,0,0)

	cantidadMaximaDigitos = int(21)
	texto = 'Ej: 255.255.255.255:65535'

	volverAlMenuParaUnirseRED = False

	IPCLIENTE = get_lan_ip()
	conector = None

	while not volverAlMenuParaUnirseRED:
		if len(texto) is 0:
			texto = 'Ej: 255.255.255.255:65535'

		evento = pygame.event.get()
		#print len(texto)
		for e in evento:

			if e.type == pygame.QUIT:
				try:
					reactor.stop()
				except: pass				
				os._exit(0)

			if e.type == pygame.KEYDOWN:
				if texto is 'Ej: 255.255.255.255:65535':
					texto = ''
				
				if e.key == pygame.K_RETURN:

					try:
						datosIP = texto.split(':')
						dirIP = str(datosIP[0])
						puertoIP = int(datosIP[1])
					except Exception as e:
						banderaDePuerto = False
						print e

					try:
						conector = reactor.connectTCP(str(dirIP), int(puertoIP), FabricaCliente())
						banderaDePuerto = True
					except Exception as e:
						banderaDePuerto = False
						print e

					if banderaDePuerto:
						volverAlMenuParaUnirseRED = CLIENTATETI(ventana, texto)
						texto = ''

				elif e.key == pygame.K_BACKSPACE:
					texto = texto[:-1]
				else:
					if len(texto) < cantidadMaximaDigitos and\
						e.unicode in '0 1 2 3 4 5 6 7 8 9 . :'.split():
						texto += e.unicode

		try:
			conector.disconnect()
		except: pass

		ventana.fill(colorGris)

		fuenteParaUnirse = pygame.font.Font('bibliottt/AtoZ.ttf', 32)
		textoUnirseAUnaPartida = 'escriba la direccion del servidor'
		textoUnirseAUnaPartidaFF = fuenteParaUnirse.render(textoUnirseAUnaPartida, True, colorRojo)
		ventana.blit(textoUnirseAUnaPartidaFF, (100, 200))

		# me quedé acá
		if texto is 'Ej: 255.255.255.255:65535':
			superficieTexto = fuenteInput.render(texto, True, colorPlaceholder)
		else:
			superficieTexto = fuenteInput.render(texto, True, color)

		widthMaxTexto = int(362)
		inputTexto.w = widthMaxTexto

		ventana.blit(superficieTexto, (inputTexto.x+4, inputTexto.y+8))
		pygame.draw.rect(ventana, color, inputTexto, 3)

		fuenteParaTextoIp = pygame.font.Font(None, 24)
		textoSobreIP = 'Tu ip local es: ' + str(IPCLIENTE)
		textoSobreIP = fuenteParaTextoIp.render(textoSobreIP, True, colorRojo)
		ventana.blit(textoSobreIP, (209, 400))

		for o in opcionMenu:
			if o.rect.collidepoint( pygame.mouse.get_pos() ):
				o.hover = True
				if pygame.mouse.get_pressed()[0]:
					o.funcion(ventana)
					volverAlMenuParaUnirseRED = True
			else:
				o.hover = False

			o.imprimir()
		
		pygame.display.flip()

	
	return True



# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------
# --------------------------------		FIN DEL COMUNICADO 		  --------------------------------
# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------




# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------
# -------------------------------- ELEGIR SER SERVIDOR O CLIENTE ---------------------------------
# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------

# Declaro antes de pantalla = _iniciarPantallaElegirRED(ventana)
colorNegro = (0,0,0)
colorGris = (192,192,192)
colorRojo = (250,0,0)
# ----------------------------------------------------------------

def _escribirTituloElegirRED(pantalla_, modoDeJuego_):

	fuenteTitulo = pygame.font.Font(None, 40)
	textoTitulo = 'Seleccione una opcion'
	tituloFormateado = fuenteTitulo.render(textoTitulo, 1, colorRojo)
	pantalla_.blit(tituloFormateado, (263, 75))
	textoCrearPartida = 'Crear partida'
	textoUnirsePartida = 'Unirse'

	if modoDeJuego_ is None:
		textoCrearPartidaFF = fuenteTitulo.render(textoCrearPartida, True, colorNegro)
		textoUnirsePartidaFF = fuenteTitulo.render(textoUnirsePartida, True, colorNegro)
		pantalla_.blit(textoCrearPartidaFF, (330, 250))
		pantalla_.blit(textoUnirsePartidaFF, (380, 350))

	elif modoDeJuego_ is 'Crear':
		textoCrearPartidaFF = fuenteTitulo.render(textoCrearPartida, True, colorRojo)
		textoUnirsePartidaFF = fuenteTitulo.render(textoUnirsePartida, True, colorNegro)
		pantalla_.blit(textoCrearPartidaFF, (330, 250))
		pantalla_.blit(textoUnirsePartidaFF, (380, 350))

	elif modoDeJuego_ is 'Unirse':
		textoCrearPartidaFF = fuenteTitulo.render(textoCrearPartida, True, colorNegro)
		textoUnirsePartidaFF = fuenteTitulo.render(textoUnirsePartida, True, colorRojo)
		pantalla_.blit(textoCrearPartidaFF, (330, 250))
		pantalla_.blit(textoUnirsePartidaFF, (380, 350))


def _mouseSelectorElegirRED(varX, varY):
	if varX > 325 and varX < 520:
		if varY > 245 and varY < 280:
			return 'Crear'

	if varX > 370 and varX < 480:
		if varY > 350 and varY < 375:
			return 'Unirse'


def funcionParaSalirAlMenuRED(ventana_):
	global volverAlMenuRED
	volverAlMenuRED = True


def _mostrarPantallaElegirRED(ventana_, pantalla_):
	varX,varY = pygame.mouse.get_pos()
	modoDeJuego_ = _mouseSelectorElegirRED(varX, varY)

	fuenteParaMenu = pygame.font.Font('bibliottt/AtoZ.ttf', 40)
	opcionMenu = [
		Opcion('Menu', (650, 540), 'menu', funcionParaSalirAlMenuRED, fuenteParaMenu, ventana_)
					   ]
	_escribirTituloElegirRED(pantalla_, modoDeJuego_)
	ventana_.blit(pantalla_, (0,0))

	for o in opcionMenu:
		if o.rect.collidepoint( pygame.mouse.get_pos() ):
			o.hover = True
			if pygame.mouse.get_pressed()[0]:
				o.funcion(ventana_)
		else:
			o.hover = False

		o.imprimir()

	pygame.display.flip()


def _iniciarPantallaElegirRED(ventana_):
	fondoPantalla = pygame.Surface(ventana_.get_size())
	fondoPantalla = fondoPantalla.convert()
	fondoPantalla.fill(colorGris)
	return fondoPantalla


def funcionParaElegirModoDeJuegoRED(ventana, tipoDeJuego):
	global volverAlMenuRED
	pygame.init()
	pygame.display.set_caption('Ta-Te-Ti de Carlitos')
	pygame.mouse.set_visible(True)
	pantalla = _iniciarPantallaElegirRED(ventana)

	volverAlMenuRED = False

	while True:

		evento = pygame.event.get()

		for e in evento:
			if e.type == pygame.QUIT:
				try:
					reactor.stop()
				except: pass
				os._exit(0)

			if e.type == pygame.MOUSEBUTTONDOWN:
				varX,varY = pygame.mouse.get_pos()
				if varX > 325 and varX < 520:
					if varY > 245 and varY < 280:
						volverAlMenuRED = funcionParaElegirLetra(ventana, 'Crear')

				if varX > 370 and varX < 480:
					if varY > 350 and varY < 375:
						volverAlMenuRED = funcionMostrarPantallaParaUnirse(ventana)

		if volverAlMenuRED:
			break

		pygame.event.pump()
		ventana.blit(pantalla, (0, 0))

		#pygame.display.flip()
		_mostrarPantallaElegirRED(ventana, pantalla)
	return True

# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------
# --------------------------------      FIN DEL COMUNICADO        --------------------------------
# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------