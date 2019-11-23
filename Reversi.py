import pygame
from pygame.locals import *
from sys import exit
from time import sleep

def cambiarJugador(turno:int) -> int:
	if turno == 0:
		turno = 1
	elif turno ==1:
		turno = 0
	return turno

def consumo(tablero:[[int]], fila:int, columna:int, turno:int) -> [[int]]:
	consumidas = []
	for i in [[-1,0], [1,0], [0,1], [0,-1], [-1,-1], [-1,1], [1,1], [1,-1]]:
		j, posibles_consumidas, vecino, fin_de_linea = 1, [], True, False
		while j < 8 and vecino and not fin_de_linea:		 
			if j == 1 and 0 <= fila + j*i[0] < 8 and 0 <= columna + j*i[1] < 8 and tablero[fila + j*i[0]][columna + j*i[1]] != 2 - turno:
				vecino = False
			elif j >= 1 and 0 <= fila + j*i[0] < 8 and 0 <= columna + j*i[1] < 8 and tablero[fila + j*i[0]][columna + j*i[1]] == 2 - turno:
				posibles_consumidas.append([fila + j*i[0],columna + j*i[1]])			
			elif j > 1 and 0 <= fila + j*i[0] < 8 and 0 <= columna + j*i[1] < 8 and tablero[fila + j*i[0]][columna + j*i[1]] == turno + 1:
				consumidas = consumidas + posibles_consumidas				
				fin_de_linea = True
			elif j > 1 and 0 <= fila + j*i[0] < 8 and 0 <= columna + j*i[1] < 8 and tablero[fila + j*i[0]][columna + j*i[1]] == 0:
				fin_de_linea = True
			j = j+1	
	for i in consumidas:
		tablero[i[0]][i[1]] = turno + 1
	return tablero
	""" Teniendo en cuenta que hay que demostrar esta funcion, tal vez habrá que cambiarla. Ademas, se tiene que este subprograma
	debe separarse en otros tres subprogramas (consumoVertical,consumoHorizontal y consumoDiagonal) sin embargo, la idea de esto es tener adelantado
	parte de la lógica """


def dibujarJugada(tablero:[[int]], fila:int, columna:int, turno:int) -> "void":
	# Precondicion
	assert(0 <= fila < 8 and 0 <= columna < 8 and 0 <= turno < 2)
	tablero[fila][columna] = turno+1
	i = 0
	while i < 8:
		j = 0
		while j < 8:
			if tablero[i][j] == 0:
				pass
			elif tablero[i][j] == 1:
				ventana.blit(fichaBlanca,(205 + 50*j, 56 + 50*i))
			elif tablero[i][j] == 2:
				ventana.blit(fichaNegra,(205 + 50*j, 56 + 50*i))
			j = j+1
		i = i+1
	pygame.display.flip()
	# Post condicion
	assert(tablero[fila][columna] == turno+1)
	
def inicializarTablero() -> [[int]]: 
	tablero = [[0 for i in range(0,8)] for i in range(0,8)]
	# Precondicion
	assert(all(all(tablero[i][j] == 0 for i in range(0,8)) for j in range(0,8)))
	tablero[3][3],tablero[4][4] = 1, 1
	tablero[3][4],tablero[4][3] = 2, 2
	ventana.blit(fondo, (0,0))
	i = 0
	while i < 8:
		j = 0
		while j < 8:
			if tablero[i][j] == 0:
				pass
			elif tablero[i][j] == 1:
				ventana.blit(fichaBlanca,(205 + 50*j, 56 + 50*i))
			elif tablero[i][j] == 2:
				ventana.blit(fichaNegra,(205 + 50*j, 56 + 50*i))
			j = j+1
		i = i+1
	ventana.blit(fichaBlancaContador, (50, 460))
	ventana.blit(fichaNegraContador, (650, 460))
	mensajeFichasB = fuente.render("2", 0, (100,100,100))
	mensajeFichasN = fuente.render("2", 0, (125,125,125))
	ventana.blit(mensajeFichasB, (85, 495))
	ventana.blit(mensajeFichasN, (685,495))
	pygame.display.flip()
	# Post condicion
	assert(all(all(tablero[i][j] == 0 for i in range(0,8) if i != 3 and i != 4) for j in range(0,8)))	
	return tablero

def esValida(tablero:[[int]], fila:int, columna:int, turno:int) -> bool: 
	# Casilla no esta ocupada por una ficha
	if tablero[fila][columna] == 0:
		casillaValida = True
	elif tablero[fila][columna] != 0:
		casillaValida = False
	# Comprueba la jugada en todas las direcciones
	cambiadas = 0
	for i in [[-1,0], [1,0], [0,1], [0,-1], [-1,-1], [-1,1], [1,1], [1,-1]]:
		j, vecino, contador, flanqueada = 1, True, 0, False 
		while j < 8 and vecino and not flanqueada: 
			if j == 1 and 0 <= fila + j*i[0] < 8 and 0 <= columna + j*i[1] < 8 and tablero[fila + j*i[0]][columna + j*i[1]] != 2 - turno:
				vecino = False
			elif j == 1 and 0 <= fila + j*i[0] < 8 and 0 <= columna + j*i[1] < 8 and tablero[fila + j*i[0]][columna + j*i[1]] == 2 - turno:
				contador = contador + 1
			elif j > 1 and 0 <= fila + j*i[0] < 8 and 0 <= columna + j*i[1] < 8 and tablero[fila + j*i[0]][columna + j*i[1]] == turno + 1:
				flanqueada = True
			elif j > 1 and 0 <= fila + j*i[0] < 8 and 0 <= columna + j*i[1] < 8 and tablero[fila + j*i[0]][columna + j*i[1]] == 2-turno:
				contador = contador + 1
			j = j + 1
		if flanqueada:
			cambiadas = cambiadas + contador
		elif not flanqueada:
			pass
		
	# Comprueba si hubieron fichas que cambiaron de color
	if cambiadas == 0:
		cambio = False
	elif cambiadas > 0:
		cambio = True

	# Comprueba que la jugada sea valida
	if cambio and casillaValida:
		esvalida = True
	elif not cambio or not casillaValida:
		esvalida = False

	return esvalida


def obtenerJugada(turno:int) -> [int]: 
	if turno == 0: # Mensaje de quien le toca jugar
		texto = "Ingrese jugada " + str(nombreJugador1) 
	elif turno == 1:
		texto = "Ingrese jugada " + str(nombreJugador2)
	mensaje = fuente.render(texto, 0, (50,50,50))
	ventana.blit(tablon, (180,460))
	ventana.blit(mensaje, (180,460))
	pygame.display.flip()

	coordenadas = ["a", "b", "c", "d", "e", "f", "g", "h"]
	while True:		
		fila = int(input("¿En qué fila desea jugar?")) 
		columna = input("¿En qué columna desea jugar?").lower()			
		try: 
			# Precondicion
			assert(0 <= fila < 8 and columna in coordenadas)
			break
		except:
			print("Ingrese una coordenada válida")
	i = 0
	while i < 8:
		if columna == coordenadas[i]:
			columna = i
		else:
			pass
		i = i + 1

	jugada = [fila-1, columna]
	# Post condicion
	assert(0 <= jugada[0] < 8 and 0 <= jugada[1] < 8)
	return jugada

def otraPartida() -> bool:
	print("¿Quieren jugar otra partida?:")
	respuesta = ""
	while respuesta != "si" and respuesta != "no":
		respuesta = input()
	return respuesta

def error(turno:int) -> "void":
	texto = "Jugada inválida"
	mensaje = fuente.render(texto, 0, (50,50,50))
	ventana.blit(tablon, (180,460))
	ventana.blit(mensaje, (180,460))
	pygame.display.flip()
	sleep(1.1)

def quedanFichas(tablero:[[int]]) -> bool:
	i, quedan = 0, False
	while i < 8 and not quedan:
		j = 0
		while j < 8 and not quedan:
			if tablero[i][j] == 0:
				quedan = False
			j = j + 1
		i = i + 1
	return quedan

def resultadoParcial(tablero:[[int]]) -> "void":
	i , fichasB, fichasN = 0, 0, 0
	while i < 8:
		j = 0
		while j < 8:
			if tablero[i][j] == 0:
				pass
			elif tablero[i][j] == 1:
				fichasB = fichasB + 1
			elif tablero[i][j] == 2:
				fichasN = fichasN + 1
			j = j+1
		i = i+1
	ventana.blit(fichaBlancaContador, (50, 460)) # Imprime la cantidad de fichas de cada color en el tablero
	ventana.blit(fichaNegraContador, (650, 460))
	textoFichasB = str(fichasB)
	textoFichasN = str(fichasN)
	mensajeFichasB = fuente.render(textoFichasB, 0, (100,100,100))
	mensajeFichasN = fuente.render(textoFichasN, 0, (125,125,125))
	ventana.blit(mensajeFichasB, (85, 495))
	ventana.blit(mensajeFichasN, (685,495))

# "Aproximacion de como deber ser el programa"
"""
turno = 0
otro = True
while otro:
	while quedanFichas:
		obtenerJugada(fila,columna) ¿Para qué el fil y el col como entrada?
		if esValida(tablero, fila, columna):
			consumo(tablero, fila, columna, turno)
			dibujarJugada(tablero, fila, columna, turno)
			cambiarJugador(turno)
		elif not esValida(tablero, fila, columna):
			error()
		resultado()
	otro = otraPartida()
"""
# Nombres de jugadores
nombreJugador1 = input("Inserte el nombre del jugador 1: ")
nombreJugador2 = input("Inserte el nombre del jugador 2: ")
# Inicializacion
pygame.init()
ventana = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Reversi")
fuente = pygame.font.Font(None, 40)
# Cargar y modificar imagenes
fondo = pygame.image.load("Tablero.png").convert()
fichaBlanca = pygame.image.load("Ficha_Blanca.png").convert_alpha()
fichaNegra = pygame.image.load("Ficha_Negra.png").convert_alpha()
tablon = pygame.image.load("Tablon.png")
fichaBlancaContador = pygame.transform.scale(fichaBlanca, (90,90))
fichaNegraContador = pygame.transform.scale(fichaNegra, (90,90))

turno = 1
tablero = inicializarTablero()
while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			exit()
	jugada = obtenerJugada(turno)	
	if esValida(tablero, jugada[0], jugada[1], turno):
		tablero = consumo(tablero, jugada[0], jugada[1], turno)
		dibujarJugada(tablero, jugada[0], jugada[1], turno)
		turno = cambiarJugador(turno)
	elif not esValida(tablero,jugada[0], jugada[1], turno):
		error(turno)
	resultadoParcial(tablero)