# Minimax-python-game
A game of cutting blocks implemented with a minimax algorithm.
## UI (User interface)
There is an user interface created with pygame, it lets you choose your cut and see the visual representation of the block. It will switch colours in each turn.
![Image of human turn](https://github.com/Alvarohf/Minimax-python-game/blob/master/ai_turn.png)
Human turn
![Image of ai turn](https://github.com/Alvarohf/Minimax-python-game/blob/master/human_turn.png)
AI turn
## Algorithm Minimax
AI is created by this algorithm, it is a full information algorithm that explores all posible plays. That is why it has been optimized while exploring new nodes (plays). Also it has a system to reduce the block to a size that is easily computable by the algorithm.
```python
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
```
This algorithm searchs for the best puntuation posible in the game. It needs a function to expand the nodes called expandir_estados.
```python
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
```
