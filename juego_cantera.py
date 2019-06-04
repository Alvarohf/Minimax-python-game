import pygame
import random
import time
from math import ceil, inf

"""-----------------------------------------------
*                Alvaro de las Heras             *
*              Inteligencia Artificial           *
-----------------------------------------------"""

# CONSTANTES
# colores
COLOR_1 = (255, 255, 255)
COLOR_2 = (204, 204, 204)
COLOR_FONDO = (88, 88, 88)
COLOR_RELLENO = (30, 30, 30)
COLOR_LETRAS = (166, 166, 166)
COLOR_INACTIVO = (70, 70, 70)
COLOR_ACTIVO = pygame.Color('dodgerblue2')
# ventana
T_CASILLA_X = 52
T_CASILLA_Y = 58
T_DIF_HOR = 27
T_DIF_VER = 32
T_DIF_PROF = 12
FPS = 30
# jugadores
MAX = 1
MIN = -1

# INICIALIZACION DEL JUEGO
# precarga del juego
pygame.init()
# fuente de texto
pygame.font.init()
font = pygame.font.Font(None, 50)
font2 = pygame.font.Font(None, 35)
# variables para los colores
color_x = COLOR_INACTIVO
color_y = COLOR_INACTIVO
color_z = COLOR_INACTIVO
# imagen del cubo
bloque = pygame.image.load("images/cubo3.png")
# titulo del juego
pygame.display.set_caption("Juego de los canteros")
# icono del juego
ICONO = pygame.image.load("images/pico.png")
pygame.display.set_icon(ICONO)
# textos a mostrar
texto_x = font.render(" Corte en el eje X ", True, COLOR_LETRAS)
texto_y = font.render(" Corte en el eje Y ", True, COLOR_LETRAS)
texto_z = font.render(" Corte en el eje Z ", True, COLOR_LETRAS)
texto_cortar = font.render("Cortar", True, COLOR_LETRAS)
texto_mayores = font2.render("Aceptar", True, COLOR_LETRAS)
# dimensiones
# se controla que solo introduzca datos enteros
try:
    print("Dimension del eje x: ")
    x = int(input())
    print("Dimension del eje y: ")
    y = int(input())
    print("Dimension del eje z: ")
    z = int(input())
except ValueError:
    print("Introduzca numeros enteros")
    exit(0)
# resolucion de la pantalla en funcion de las dimensiones
resolucion = (T_CASILLA_X * x + 480 + T_DIF_HOR * z, int(T_CASILLA_Y * y * 0.5 + T_DIF_PROF * z + 260))
screen = pygame.display.set_mode(resolucion)
# reloj del juego
clock = pygame.time.Clock()
# cajas de texto
area_x = pygame.Rect(T_CASILLA_X * x + T_DIF_HOR * z + 370, 50, 90, 40)
area_y = pygame.Rect(T_CASILLA_X * x + T_DIF_HOR * z + 370, 100, 90, 40)
area_z = pygame.Rect(T_CASILLA_X * x + T_DIF_HOR * z + 370, 150, 90, 40)
boton_corte = pygame.Rect(T_CASILLA_X * x + T_DIF_HOR * z + 180, 200, 140, 40)
# contenidos de las cajas
numeros_x = ""
numeros_y = ""
numeros_z = ""
# activa el area de las cajas
activo_x = False
activo_y = False
activo_z = False
# activa el renderizado del juego completo
renderizado = True


# FUNCIONES

# ALGORITMO MINIMAX Y EXPANSION DE ESTADOS

def expandir_estados(estado):
    """
    Expande los estados de un nodo dado
    :param estado: nodo que se expandira
    :return: todos los nodos expandidos
    """
    expansion = []
    # se van expandiendo en cada dimension pero solo se tienen en cuenta la mitad
    # ahorrando así recursos
    if estado[0] > 1:
        for i in reversed(range(ceil(estado[0] / 2), estado[0])):
            expansion.append([i, estado[1], estado[2]])
    if estado[1] > 1:
        if estado[1] != estado[0]:
            for j in reversed(range(ceil(estado[1] / 2), estado[1])):
                expansion.append([estado[0], j, estado[2]])
    if estado[2] > 1:
        if estado[2] != estado[1] and estado[2] != estado[0]:
            for k in reversed(range(ceil(estado[2] / 2), estado[2])):
                expansion.append([estado[0], estado[1], k])
    return expansion


def minimax(estado, jugador):
    """
    Algoritmo minimax que elige la mejor jugada segun el jugador o estado
    :param estado: estado actual del bloque
    :param jugador: jugador actual (MIN o Max)
    :return: la mejor jugada con su puntuacion
    """
    # dependiendo del jugador se inicia de una forma u otra la puntuacion
    if jugador == MAX:
        # [estado, puntuacion]
        mejor = [-1, -inf]
    else:
        mejor = [-1, +inf]
    # condicion meta para acabar (bloque 1x1x1)
    if estado[0] == 1 and estado[1] == 1 and estado[2] == 1:
        # si es la maquina quien llega a la puntuacion se toma como -1
        if jugador == MAX:
            puntuacion = -1
        else:
            # si es la persona como +1
            puntuacion = +1
        # se devuelve la puntuacion obtenida
        return [-1, puntuacion]
    # se recorren todos los nodos y sus expansiones
    for i in expandir_estados(estado):
        # se guarda el actual
        estado_aux = estado
        # se llama recursivamente
        puntuacion = minimax(i, -jugador)
        # se restaura el estado
        estado = estado_aux
        # se guarda la jugada hecha
        puntuacion[0] = i
        # se comprueba si para MAX hay una puntuacion que maximice la mejor
        if jugador == MAX:
            if puntuacion[1] > mejor[1]:
                mejor = puntuacion
        # se comprueba si para MIN hay una puntuacion que minimice la mejor
        else:
            if puntuacion[1] < mejor[1]:
                mejor = puntuacion
    # devuelve la mejor puntuacion de todas
    return mejor


# FUNCIONES DEL JUEGO


def render_juego(p_screen, p_numeros_x, p_numeros_y, p_numeros_z, p_renderizado_total):
    """
    Renderiza el juego con todos los elementos que contiene
    :param p_screen: pantalla sobre la que se renderizara
    :param p_numeros_x: string con el conetenido de la casilla de x
    :param p_numeros_y: string con el conetenido de la casilla de y
    :param p_numeros_z: string con el conetenido de la casilla de z
    :param p_renderizado_total: booleano que indica si hay que renderizar todo
    """
    # renderiza ademas de lo basico el modelo 3D y las cajas fijas
    if p_renderizado_total:
        # vuelve a rellenar la pantalla
        screen.fill(COLOR_FONDO)
        # modelo 3d del cubo hecho con bloques mas pequeños
        for t in range(0, x):
            acum_y = 0
            for i in reversed(range(0, z)):
                acum_y += T_DIF_PROF
                for j in reversed(range(0, y)):
                    p_screen.blit(bloque, (i * T_DIF_HOR + t * T_DIF_HOR + 70, j * T_DIF_VER + acum_y + t * T_DIF_PROF))
        # cajas de los botones de corte
        pygame.draw.rect(p_screen, COLOR_RELLENO, boton_corte)
        pygame.draw.rect(p_screen, COLOR_INACTIVO, boton_corte, 3)
        # muestra los textos
        p_screen.blit(texto_mayores, (boton_corte.x + 20, boton_corte.y + 8))
        p_screen.blit(texto_x, (T_CASILLA_X * x + T_DIF_HOR * z + 70, 50))
        p_screen.blit(texto_y, (T_CASILLA_X * x + T_DIF_HOR * z + 70, 100))
        p_screen.blit(texto_z, (T_CASILLA_X * x + T_DIF_HOR * z + 70, 150))
        p_screen.blit(texto_cortar, (T_CASILLA_X * x + T_DIF_HOR * z + 70, 200))
        texto_dimensiones = font.render("Dim | x: " + str(x) + " y: " + str(y) + " z: " + str(z), True, COLOR_LETRAS)
        p_screen.blit(texto_dimensiones, (T_CASILLA_X * x + T_DIF_HOR * z + 70, 250))

    # dibuja cajas de los textos y sus bordes
    pygame.draw.rect(p_screen, COLOR_RELLENO, area_x)
    pygame.draw.rect(p_screen, color_x, area_x, 3)
    pygame.draw.rect(p_screen, COLOR_RELLENO, area_y)
    pygame.draw.rect(p_screen, color_y, area_y, 3)
    pygame.draw.rect(p_screen, COLOR_RELLENO, area_z)
    pygame.draw.rect(p_screen, color_z, area_z, 3)
    # muestra los textos de las cajas
    textsurface_p = font.render(p_numeros_x, True, COLOR_LETRAS)
    screen.blit(textsurface_p, (area_x.x + 5, area_x.y + 4))
    textsurface_p = font.render(p_numeros_y, True, COLOR_LETRAS)
    screen.blit(textsurface_p, (area_y.x + 5, area_y.y + 4))
    textsurface_p = font.render(p_numeros_z, True, COLOR_LETRAS)
    screen.blit(textsurface_p, (area_z.x + 5, area_z.y + 4))


def comprobar_valido(p_eje_x, p_eje_y, p_eje_z):
    """
    Comprueba si los valores de los cortes son validos
    :param p_eje_x: valor del corte en el eje x
    :param p_eje_y: valor del corte en el eje y
    :param p_eje_z: valor del corte en el eje z
    :return: devuelve los tres valores una vez validados
    """
    # valor por defecto correspondiente al actual
    comprobacion = (x, y, z)
    # comprueba si son positivos y menores que los actuales y los otros valores distintos a 0
    if (p_eje_x > 0) and (p_eje_y == p_eje_z == 0) and (p_eje_x < x):
        # el nuevo valor sera el del corte o el de la diferencia con el actual
        comprobacion = (max(x - p_eje_x, p_eje_x), y, z)
    elif (p_eje_y > 0) and (p_eje_x == p_eje_z == 0) and (p_eje_y < y):
        comprobacion = (x, max(y - p_eje_y, p_eje_y), z)
    elif (p_eje_z > 0) and (p_eje_y == p_eje_x == 0) and (p_eje_z < z):
        comprobacion = (x, y, max(z - p_eje_z, p_eje_z))
    return comprobacion


def sortear_turno():
    """
    Sortea el turno entre dos jugadores
    :return: un booleano que representa el turno
    """
    return True if random.random() < 0.5 else False


def comprobar_colision(p_activo, area, evento):
    """
    Comprueba si hay colision y devuelve un booleano
    :param p_activo: booleano que modificara
    :param area: area en la que comprobara la colision
    :param evento: evento que colisiono
    :return: booleano con los datos de la colision
    """
    if area.collidepoint(evento.pos):
        # activa la variable
        p_activo = not p_activo
    else:
        p_activo = False
    return p_activo


def modificar_numeros(numeros, evento):
    """
    Modifica los numeros del juego
    :param numeros: numeros que modificara
    :param evento: tecla que lo ha originado
    :return: los numeros actualizados
    """
    # se aseguran que sean decimales y se añaden
    if evento.unicode.isdecimal():
        numeros += event.unicode
    # si es tecla de borrado elimina el ultimo
    elif evento.key == pygame.K_BACKSPACE:
        numeros = numeros[:-1]
    # si es enter borra todo
    elif evento.key == pygame.K_RETURN:
        numeros = ""
    # si se pulsa escape se sale del juego
    elif evento.key == pygame.K_ESCAPE:
        exit(0)
    return numeros


def ganador():
    """
    Comprueba si se ha ganado y finaliza el juego
    """
    # si no se puede cortar mas en funcion del turno gana un jugador u otro
    if x == 1 and y == 1 and z == 1:
        if turno:
            print("PIERDE EL HUMANO")
        else:
            print("PIERDE EL ORDENADOR")
        print("FIN DEL JUEGO")
        exit(0)


def cortar(p_numeros_x, p_numeros_y, p_numeros_z):
    """
    Corta el bloque en las dimensiones dadas
    :param p_numeros_x: dimensiones del eje x para cortar
    :param p_numeros_y: dimensiones del eje y para cortar
    :param p_numeros_z: dimensiones del eje z para cortar
    """
    # comprueba si las dimensiones son validas
    p = comprobar_valido(get_num(p_numeros_x), get_num(p_numeros_y), get_num(p_numeros_z))
    # si son iguales que las actuales no se hace nada
    if p != (x, y, z):
        # si difieren se actualizan las dimensiones
        set_x(p[0])
        set_y(p[1])
        set_z(p[2])
        # se actualizan las areas con las nuevas dimensiones
        n_area_x = pygame.Rect(T_CASILLA_X * x + T_DIF_HOR * z + 370, 50, 90, 40)
        n_area_y = pygame.Rect(T_CASILLA_X * x + T_DIF_HOR * z + 370, 100, 90, 40)
        n_area_z = pygame.Rect(T_CASILLA_X * x + T_DIF_HOR * z + 370, 150, 90, 40)
        n_boton_corte = pygame.Rect(T_CASILLA_X * x + T_DIF_HOR * z + 180, 200, 140, 40)
        set_areas(n_area_x, n_area_y, n_area_z, n_boton_corte)
        # se actualizan los tipos de bloque
        if turno:
            global bloque
            bloque = pygame.image.load("images/cubo3.png")
        else:
            bloque = pygame.image.load("images/cubo.png")
        # se cambia el turno
        set_turno(not turno)

    # Se formatean las casillas de las dimensiones
    set_textos("", "", "")


def reducir(p_x, p_y, p_z):
    """
    Reduce el tamano del bloque para facilitar calculo
    :param p_x: tamano de la x
    :param p_y: tamano de la y
    :param p_z: tamano de la z
    :return: el bloque reducido
    """
    reduccion = (p_x, p_y, p_z)
    # cortara el mayor de todos por la mitad aproximada
    if p_x >= p_y and p_x >= p_z:
        reduccion = (ceil(p_x / 2), p_y, p_z)
    elif p_y >= p_z and p_y >= p_x:
        reduccion = (p_x, ceil(p_y / 2), p_z)
    elif p_z >= p_y and p_z >= p_x:
        reduccion = (p_x, p_y, ceil(p_z / 2))
    # lo devuelve dentro de otra lista para compatibilidad
    return [reduccion]


# SETTERS Y GETTERS(CON RESTRICCIONES)


def set_x(p_x):
    """
    Asigna un valor a la variable global x
    :param p_x: nuevo valor de x
    """
    global x
    x = p_x


def set_y(p_y):
    """
    Asigna un valor a la variable global y
    :param p_y: nuevo valor de y
    """
    global y
    y = p_y


def set_z(p_z):
    """
    Asigna un valor a la variable global z
    :param p_z: nuevo valor de z
    """
    global z
    z = p_z


def set_turno(p_turno):
    """
    Asigna un valor a la variable global del turno
    :param p_turno: nuevo valor del turno
    :return:
    """
    global turno
    turno = p_turno


def set_areas(p_area_x, p_area_y, p_area_z, p_boton_cortar):
    """
    Asigna nuevos valores a todas las areas del juego
    :param p_area_x: nuevo valor del area de x
    :param p_area_y: nuevo valor del area de y
    :param p_area_z: nuevo valor del area de z
    :param p_boton_cortar: nuevo valor del area del boton
    """
    global area_x, area_y, area_z, boton_corte
    area_x = p_area_x
    area_y = p_area_y
    area_z = p_area_z
    boton_corte = p_boton_cortar


def set_textos(p_numeros_x, p_numeros_y, p_numeros_z):
    """
    Asigna nuevos valores a todos los textos modificables del juego
    :param p_numeros_x: nuevo valor del texto de x
    :param p_numeros_y: nuevo valor del texto de x
    :param p_numeros_z: nuevo valor del texto de x
    """
    global numeros_x, numeros_y, numeros_z
    numeros_x = p_numeros_x
    numeros_y = p_numeros_y
    numeros_z = p_numeros_z


def get_num(p_numero):
    """
    Recibe un string y lo pasa a entero filtrando cadenas vacias
    :param p_numero: string que sera el numero a devolver
    :return: numero que se devuelve
    """
    try:
        # si es una cadena vacia se trata como un 0
        if p_numero == "":
            p_numero = "0"
        return int(p_numero)
    except ValueError:
        print("Error de tipo: solo numeros enteros")


def get_jugada(p_jugada, p_total):
    """
    Recibe la jugada y el total para coger solo las que difieren
    :param p_jugada: jugada a comprobar
    :param p_total: valor actual total
    :return: la jugada si es distinta al total
    """
    if p_jugada == p_total:
        p_jugada = 0
    return p_jugada


# COMIENZO DEL JUEGO
# sorteo del turno
turno = sortear_turno()
if turno:
    print("COMIENZA EL HUMANO")
else:
    print("COMIENZA EL ORDENADOR")
# renderizado del tablero inicial
render_juego(screen, numeros_x, numeros_y, numeros_z, renderizado)
pygame.display.flip()
# BUCLE DEL JUEGO
while True:
    # comprueba si ha ganado la maquina
    ganador()
    # turno del jugador humano
    while turno:
        # se limitan los FPS para consumir menos
        clock.tick(FPS)
        # se atienden los eventos que genera el usuario
        for event in pygame.event.get():
            # si cierra el juego se cierra el sistema
            if event.type == pygame.QUIT:
                raise SystemExit
            # si aprieta una tecla leera solo los numeros del teclado
            elif event.type == pygame.KEYDOWN:
                # segun el que este activo se modifica uno u otro
                if activo_x:
                    numeros_x = modificar_numeros(numeros_x, event)
                elif activo_y:
                    numeros_y = modificar_numeros(numeros_y, event)
                elif activo_z:
                    numeros_z = modificar_numeros(numeros_z, event)
            # si el evento de es de click de raton
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # comprueba donde se produjo la colision
                activo_x = comprobar_colision(activo_x, area_x, event)
                activo_y = comprobar_colision(activo_y, area_y, event)
                activo_z = comprobar_colision(activo_z, area_z, event)
                # segun la posicion de la colision cambia los colores
                if activo_x:
                    color_x = COLOR_ACTIVO
                    color_y = COLOR_INACTIVO
                    color_z = COLOR_INACTIVO
                elif activo_y:
                    color_x = COLOR_INACTIVO
                    color_y = COLOR_ACTIVO
                    color_z = COLOR_INACTIVO
                elif activo_z:
                    color_x = COLOR_INACTIVO
                    color_y = COLOR_INACTIVO
                    color_z = COLOR_ACTIVO
                # si se detecto la colision en el boton de corte lo intenta realizar
                if boton_corte.collidepoint(event.pos):
                    print("-----HUMANO------")
                    # llama a la funcion para cortar
                    cortar(numeros_x, numeros_y, numeros_z)
                    print("x: ", x, "y: ", y, "z: ", z)
                    # modifica la pantalla con los nuevos valores
                    resolucion = (
                        T_CASILLA_X * x + 480 + T_DIF_HOR * z, int(T_CASILLA_Y * y * 0.5 + T_DIF_PROF * z + 260))
                    screen = pygame.display.set_mode(resolucion)
                    # renderiza la nueva pantalla
                    render_juego(screen, chr(x), chr(y), chr(z), True)
            # dibuja tablero
            render_juego(screen, numeros_x, numeros_y, numeros_z, renderizado)
            # no se renderiza completo
            renderizado = False
        pygame.display.flip()
    # comprueba si ha ganado el humano
    ganador()
    # entra si es el turno de la maquina
    if not turno:
        print("-----MAQUINA------")
        # cuenta el tiempo de computo de las soluciones
        tiempo_inicial = time.time()
        # si es muy grande no es posible calcularlo en un tiempo razonable 6x6x6
        if x * y * z > 226:
            # reduce el tamano hasta uno mas asequible
            jugada = reducir(x, y, z)
        else:
            # obtiene la jugada del minimax
            jugada = minimax((x, y, z), -1)
        print("Tiempo computo {:.5f} ms".format((time.time() - tiempo_inicial) * 1000))
        print("Mi jugada sera: {}".format(jugada[0]))
        try:
            # espera para poder ver la jugada de la maquina
            time.sleep(3)
            # realiza el corte
            cortar(get_jugada(jugada[0][0], x), get_jugada(jugada[0][1], y), get_jugada(jugada[0][2], z))
        except TypeError:
            exit(-1)
        # modifica la resolucion con los nuevos valores
        resolucion = (
            T_CASILLA_X * x + 480 + T_DIF_HOR * z, int(T_CASILLA_Y * y * 0.5 + T_DIF_PROF * z + 260))
        screen = pygame.display.set_mode(resolucion)
        # muestra el tablero de nuevo
        render_juego(screen, chr(x), chr(y), chr(z), True)
        pygame.display.flip()
