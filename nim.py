import sys, pygame, random
from pygame.locals import *
from copy import deepcopy

WIDTH = 600
HEIGHT = 600
pygame.init()

COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)

class nodo:
    def __init__(self, value="Manzana"):
        self.padre = None
        self.hijos = []
        self.value = value
        self.color = ""

    def esHoja(self):
        return not self.hijos

class arbol:
    def __init__(self):
        self.raiz = None

    def add_raiz(self, valor):
        nodo_temp = nodo(valor)
        self.raiz = nodo_temp
        return nodo_temp

    def add_nodo(self, padre, valor):
        nodo_temp = nodo(valor)
        padre.hijos.append(nodo_temp)
        nodo_temp.padre = padre
        return nodo_temp

    def ancestros(self, nodo):
        if not nodo:
            return []
        else:
            return self.ancestros(nodo.padre) + [nodo.valor]

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(150, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

def text_objects(text, font, color):
    black = (0, 0, 0)
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def startGame():
    numMonticulos = random.randint(2, 3)
    listaPiedras = []
    for i in range(numMonticulos):
        numPiedras = random.randint(3, 5)
        listaPiedras.append(numPiedras)
    listaPiedras.append("1")
    return numMonticulos, listaPiedras

def createTree(nodito, arbolito):
    newList = nodito.value.copy()
    jugadorAnt = newList[len(newList) - 1]
    if jugadorAnt == "1":
        jugadorActual = "2"
    else:
        jugadorActual = "1"

    newList[len(newList) - 1] = jugadorActual

    for index, element in enumerate(newList):
        if not isinstance(element, str):
            newList2 = nodito.value.copy()
            newList2[len(newList) - 1] = jugadorActual
            if element == 1:

                element -= 1
                newList2[index] = element

                newNodo = arbolito.add_nodo(nodito, newList2.copy())
                createTree(newNodo, arbolito)
            else:
                while element > 1:
                    element -= 1
                    newList2[index] -= 1
                    nodito3 = arbolito.add_nodo(nodito, newList2.copy())
                    createTree(nodito3, arbolito)

def paintHojas(nodito):
    for hijo in nodito.hijos:
        if hijo.esHoja():
            if hijo.value[-1] == "1":
                hijo.color = "Green"
            else:
                hijo.color = "Blue"
        else:
            paintHojas(hijo)

def paintTree(nodito):
    if not nodito.esHoja():
        for hijo in nodito.hijos:
            paintTree(hijo)
        for hijo in nodito.hijos:
            if hijo.color == "Green":
                nodito.color = "Green"
                break
            else:
                nodito.color = "Blue"

def actionButton1(counterButton1, color):
    counterButton1 += 1
    if counterButton1 == 3:
        counterButton1 = 1

    if counterButton1 == 1: # Desactivado
        color["button1"] = pygame.Color('lightskyblue3')
        var = False
    else: # Activado
        color["button1"] = pygame.Color('dodgerblue2')
        var = True
    #print('button was pressed at {0}'.format(mouse_pos))
    return counterButton1, var

def actionButton2(counterButton2, color):
    counterButton2 += 1
    if counterButton2 == 3:
        counterButton2 = 1

    if counterButton2 == 1:
        color["button2"] = pygame.Color('lightskyblue3')
        var = False
    else:
        color["button2"] = pygame.Color('dodgerblue2')
        var = True
    #print('button was pressed at {0}'.format(mouse_pos))
    return counterButton2, var

def actionMonton1(numPiedras, counterMonton1, bandsMonton1):
    counterMonton1 = counterPlus(counterMonton1)

    if counterMonton1 == 1:  # Desactivado
        var = False
    else:  # Activado
        var = True

    if numPiedras == 1:
        bandsMonton1[0] = True
    else:
        for i in range(numPiedras - 1):
            bandsMonton1[i] = True

    return counterMonton1, var

def actionMonton2(numPiedras, counterMonton2, bandsMonton2):
    counterMonton2 = counterPlus(counterMonton2)

    if counterMonton2 == 1:  # Desactivado
        #color["button1"] = pygame.Color('lightskyblue3')
        var = False
    else:  # Activado
        #color["button1"] = pygame.Color('dodgerblue2')
        var = True

    if numPiedras == 1:
        bandsMonton2[0] = True
    else:
        for i in range(numPiedras - 1):
            bandsMonton2[i] = True

    return counterMonton2, var

def actionMonton3(numPiedras, counterMonton3, bandsMonton3):
    counterMonton3 = counterPlus(counterMonton3)

    if counterMonton3 == 1:  # Desactivado
        var = False
    else:  # Activado
        var = True

    if numPiedras == 1:
        bandsMonton3[0] = True
    else:
        for i in range(numPiedras - 1):
            bandsMonton3[i] = True

    return counterMonton3, var

def updateGame(numMonton, numPiedrasMenos, listaPiedras, arbolito, nodoActual):
    newList = listaPiedras.copy()
    newList[numMonton-1] = newList[numMonton-1] + numPiedrasMenos
    if newList[-1] == "1":
        newList[-1] = "2"
    else:
        newList[-1] = "1"

    for index, hijo in enumerate(nodoActual.hijos):
        if hijo.value == newList:
            nodoActual = hijo
            listaPiedras = newList
            break
    return nodoActual, listaPiedras

def updatePC(choice, listaPiedras, nodoActual):
    #newList = listaPiedras.copy()

    listaElegidos = []

    for index, hijo in enumerate(nodoActual.hijos):
        if hijo.color == choice:
            listaElegidos.append(hijo)

    if not listaElegidos:
        if nodoActual.hijos:
            newNodo = random.choice(nodoActual.hijos)
    else:
        newNodo = random.choice(listaElegidos)

    nodoActual = newNodo
    listaPiedras = newNodo.value

    return nodoActual, listaPiedras

def updateMontones(listaPiedras, color):
    pos = (175, 175)
    largeText = pygame.font.SysFont("comicsansms", 20)
    TextSurfMon1, TextRectMon1 = text_objects(str(listaPiedras[0]), largeText, color["negro"])
    TextRectMon1.center = (pos)

    pos = (275, 175)
    TextSurfMon2, TextRectMon2 = text_objects(str(listaPiedras[1]), largeText, color["negro"])
    TextRectMon2.center = (pos)

    pos = (375, 175)
    TextSurfMon3, TextRectMon3 = text_objects(str(listaPiedras[2]), largeText, color["negro"])
    TextRectMon3.center = (pos)

    return TextSurfMon1, TextRectMon1, TextSurfMon2, TextRectMon2, TextSurfMon3, TextRectMon3

def counterPlus(counter):
    counter += 1
    if counter == 3:
        counter = 1
    return counter

def turn(nombres, game):
    game += 1
    if game == 3:
        game = 1
    largeText = pygame.font.SysFont("comicsansms", 20)

    pos = (180, 100)
    TextSurfName, TextRectName = text_objects(nombres[game-1], largeText, (102, 208, 250))
    TextRectName.center = (pos)

    return TextSurfName, TextRectName, game

def calculateChoice(dificultades, game):
    dif = dificultades[game - 1]
    numRand = random.randint(1, 10)
    if numRand <= dif:
        if game == 1:
            choice = "Green"
        else:
            choice = "Blue"
    else:
        if game == 1:
            choice = "Blue"
        else:
            choice = "Green"
    return choice

def checkIfWins(listaPiedras, pantalla, color, nombres, game):
    sum = 0
    for element in listaPiedras:
        if not isinstance(element, str):
            sum += element
    if sum == 1:
        game = 3
    return game

def main():
    game = 0
    counterButton1 = 1
    counterButton2 = 1
    counterMonton1 = 1
    counterMonton2 = 1
    counterMonton3 = 1

    banderasInputs = [False, False]
    banderasMontones = [False, False, False]
    bandsMonton1 = [False, False, False, False, False]
    bandsMonton2 = [False, False, False, False, False]
    bandsMonton3 = [False, False, False, False, False]
    bandsMontones = [bandsMonton1, bandsMonton2, bandsMonton3]

    nombres = ["", ""]
    dificultades = [0, 0]

    color = dict()
    color["fondo"] = (5, 134, 181)
    color["blanco"] = (255, 255, 255)
    color["azul"] = (0, 0, 255)
    color["rojo"] = (0, 255, 0)
    color["verde"] = (0, 255, 0)
    color["negro"] = (0, 0, 0)
    color["camino"] = (176, 252, 255)
    color["pared"] = (7, 114, 117)
    color["button1"] = pygame.Color('lightskyblue3')
    color["button2"] = pygame.Color('lightskyblue3')

    reloj = pygame.time.Clock()
    pantalla = pygame.display.set_mode((WIDTH, HEIGHT))

    #Boton 1
    button1 = pygame.Rect(150, 200, 50, 50)
    pos = (175, 225)
    largeText = pygame.font.SysFont("comicsansms", 18)
    TextSurf, TextRect = text_objects("PC1", largeText, color["negro"])
    TextRect.center = (pos)

    #Boton 2
    button2 = pygame.Rect(400, 200, 50, 50)
    pos = (425, 225)
    TextSurf2, TextRect2 = text_objects("PC2", largeText, color["negro"])
    TextRect2.center = (pos)

    #Boton Start
    buttonStart = pygame.Rect(275, 500, 100, 50)
    pos = (325, 525)
    largeText = pygame.font.SysFont("comicsansms", 25)
    TextSurfStart, TextRectStart = text_objects("Start", largeText, color["negro"])
    TextRectStart.center = (pos)

    #Inputs
    input_box1 = InputBox(100, 300, 150, 32, "Name")
    input_box2 = InputBox(350, 300, 150, 32, "Name")
    input_boxes = [input_box1, input_box2]

    TextSurfD1, TextRectD1 = text_objects("Difficulty: ", largeText, color["blanco"])
    TextRectD1.center = (150, 375)

    TextSurfD2, TextRectD2 = text_objects("Difficulty: ", largeText, color["blanco"])
    TextRectD2.center = (400, 375)

    RectsDif = [[TextSurfD1, TextRectD1], [TextSurfD2, TextRectD2]]

    input_boxD1 = InputBox(100, 400, 150, 30, "1-10")
    input_boxD2 = InputBox(350, 400, 150, 30, "1-10")
    inputs_difficulty = [input_boxD1, input_boxD2]

    #Jugadores
    largeText = pygame.font.SysFont("comicsansms", 20)

    pos = (175, 175)
    TextSurfJ1, TextRectJ1 = text_objects("Player 1", largeText, color["blanco"])
    TextRectJ1.center = (pos)

    pos = (425, 175)
    TextSurfJ2, TextRectJ2 = text_objects("Player 2", largeText, color["blanco"])
    TextRectJ2.center = (pos)

    pos = (300, 100)
    largeText = pygame.font.SysFont("comicsansms", 40)
    TextSurfNim, TextRectNim = text_objects("NIM", largeText, color["blanco"])
    TextRectNim.center = (pos)

    #Crea el Arbol
    numMonticulos, listaPiedras = startGame()
    arbolito = arbol()
    raiz = arbolito.add_raiz(listaPiedras)
    createTree(raiz, arbolito)
    paintHojas(raiz)
    paintTree(raiz)

    nodoActual = raiz

    '''______________________Game_______________________'''

    largeText = pygame.font.SysFont("comicsansms", 20)
    pos = (100, 100)
    TextSurfTurn, TextRectTurn = text_objects("Turno de: ", largeText, color["blanco"])
    TextRectTurn.center = (pos)

    pos = (180, 100)
    TextSurfName, TextRectName = text_objects(nombres[1], largeText, color["azul"])
    TextRectName.center = (pos)

    #Montones
    monton1 = pygame.Rect(150, 150, 50, 50)
    pos = (175, 175)
    largeText = pygame.font.SysFont("comicsansms", 20)
    TextSurfMon1, TextRectMon1 = text_objects(str(listaPiedras[0]), largeText, color["negro"])
    TextRectMon1.center = (pos)

    monton2 = pygame.Rect(250, 150, 50, 50)
    pos = (275, 175)
    TextSurfMon2, TextRectMon2 = text_objects(str(listaPiedras[1]), largeText, color["negro"])
    TextRectMon2.center = (pos)

    monton3 = pygame.Rect(350, 150, 50, 50)
    pos = (375, 175)
    TextSurfMon3, TextRectMon3 = text_objects(str(listaPiedras[2]), largeText, color["negro"])
    TextRectMon3.center = (pos)


    #____BOTONES____#
    botones = []
    textos = []

    mon1_button1 = pygame.Rect(150, 225, 50, 50)
    pos = (175, 250)
    TextSurf_m1b1, TextRect_m1b1 = text_objects("-1", largeText, color["negro"])
    TextRect_m1b1.center = (pos)
    mon1_button2 = pygame.Rect(150, 300, 50, 50)
    pos = (175, 325)
    TextSurf_m1b2, TextRect_m1b2 = text_objects("-2", largeText, color["negro"])
    TextRect_m1b2.center = (pos)
    mon1_button3 = pygame.Rect(150, 375, 50, 50)
    pos = (175, 400)
    TextSurf_m1b3, TextRect_m1b3 = text_objects("-3", largeText, color["negro"])
    TextRect_m1b3.center = (pos)
    mon1_button4 = pygame.Rect(150, 450, 50, 50)
    pos = (175, 475)
    TextSurf_m1b4, TextRect_m1b4 = text_objects("-4", largeText, color["negro"])
    TextRect_m1b4.center = (pos)
    mon1_button5 = pygame.Rect(150, 525, 50, 50)
    pos = (175, 550)
    TextSurf_m1b5, TextRect_m1b5 = text_objects("-5", largeText, color["negro"])
    TextRect_m1b5.center = (pos)

    mon2_button1 = pygame.Rect(250, 225, 50, 50)
    pos = (275, 250)
    TextSurf_m2b1, TextRect_m2b1 = text_objects("-1", largeText, color["negro"])
    TextRect_m2b1.center = (pos)
    mon2_button2 = pygame.Rect(250, 300, 50, 50)
    pos = (275, 325)
    TextSurf_m2b2, TextRect_m2b2 = text_objects("-2", largeText, color["negro"])
    TextRect_m2b2.center = (pos)
    mon2_button3 = pygame.Rect(250, 375, 50, 50)
    pos = (275, 400)
    TextSurf_m2b3, TextRect_m2b3 = text_objects("-3", largeText, color["negro"])
    TextRect_m2b3.center = (pos)
    mon2_button4 = pygame.Rect(250, 450, 50, 50)
    pos = (275, 475)
    TextSurf_m2b4, TextRect_m2b4 = text_objects("-4", largeText, color["negro"])
    TextRect_m2b4.center = (pos)
    mon2_button5 = pygame.Rect(250, 525, 50, 50)
    pos = (275, 550)
    TextSurf_m2b5, TextRect_m2b5 = text_objects("-5", largeText, color["negro"])
    TextRect_m2b5.center = (pos)

    mon3_button1 = pygame.Rect(350, 225, 50, 50)
    pos = (375, 250)
    TextSurf_m3b1, TextRect_m3b1 = text_objects("-1", largeText, color["negro"])
    TextRect_m3b1.center = (pos)
    mon3_button2 = pygame.Rect(350, 300, 50, 50)
    pos = (375, 325)
    TextSurf_m3b2, TextRect_m3b2 = text_objects("-2", largeText, color["negro"])
    TextRect_m3b2.center = (pos)
    mon3_button3 = pygame.Rect(350, 375, 50, 50)
    pos = (375, 400)
    TextSurf_m3b3, TextRect_m3b3 = text_objects("-3", largeText, color["negro"])
    TextRect_m3b3.center = (pos)
    mon3_button4 = pygame.Rect(350, 450, 50, 50)
    pos = (375, 475)
    TextSurf_m3b4, TextRect_m3b4 = text_objects("-4", largeText, color["negro"])
    TextRect_m3b4.center = (pos)
    mon3_button5 = pygame.Rect(350, 525, 50, 50)
    pos = (375, 550)
    TextSurf_m3b5, TextRect_m3b5 = text_objects("-5", largeText, color["negro"])
    TextRect_m3b5.center = (pos)

    lista = [mon1_button1, mon1_button2, mon1_button3, mon1_button4, mon1_button5]
    botones.append(lista)
    lista = [mon2_button1, mon2_button2, mon2_button3, mon2_button4, mon2_button5]
    botones.append(lista)
    lista = [mon3_button1, mon3_button2, mon3_button3, mon3_button4, mon3_button5]
    botones.append(lista)

    texto = [(TextSurf_m1b1, TextRect_m1b1), (TextSurf_m1b2, TextRect_m1b2), (TextSurf_m1b3, TextRect_m1b3), (TextSurf_m1b4, TextRect_m1b4), (TextSurf_m1b5, TextRect_m1b5)]
    textos.append(texto)
    texto = [(TextSurf_m2b1, TextRect_m2b1), (TextSurf_m2b2, TextRect_m2b2), (TextSurf_m2b3, TextRect_m2b3), (TextSurf_m2b4, TextRect_m2b4), (TextSurf_m2b5, TextRect_m2b5)]
    textos.append(texto)
    texto = [(TextSurf_m3b1, TextRect_m3b1), (TextSurf_m3b2, TextRect_m3b2), (TextSurf_m3b3, TextRect_m3b3),
             (TextSurf_m3b4, TextRect_m3b4), (TextSurf_m3b5, TextRect_m3b5)]
    textos.append(texto)

    choice = ""
    #update = 0
    firstOne = 1
    while True:
        if game == 0:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit(0)

                for box in input_boxes:
                    box.handle_event(event)
                for box in inputs_difficulty:
                    box.handle_event(event)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos  # gets mouse position

                    # checks if mouse position is over the button
                    if button1.collidepoint(mouse_pos):
                        counterButton1, banderasInputs[0] = actionButton1(counterButton1, color)

                    if button2.collidepoint(mouse_pos):
                        counterButton2, banderasInputs[1] = actionButton2(counterButton2, color)

                    if buttonStart.collidepoint(mouse_pos):
                        for index, box in enumerate(input_boxes):
                            if banderasInputs[index] == False:
                                nombres[index] = input_boxes[index].text
                            else:
                                dif = int(inputs_difficulty[index].text)
                                dificultades[index] = dif
                                nombres[index] = f'PC {dif}'

                        game = 0
                        TextSurfName, TextRectName, game = turn(nombres, game)

            for box in input_boxes:
                box.update()

            for box in inputs_difficulty:
                box.update()

            pantalla.fill((30, 30, 30))

            pygame.draw.rect(pantalla, color["button1"], button1)
            pygame.draw.rect(pantalla, color["button2"], button2)
            pygame.draw.rect(pantalla, COLOR_ACTIVE, buttonStart)

            pantalla.blit(TextSurf, TextRect)
            pantalla.blit(TextSurf2, TextRect2)
            pantalla.blit(TextSurfJ1, TextRectJ1)
            pantalla.blit(TextSurfJ2, TextRectJ2)
            pantalla.blit(TextSurfNim, TextRectNim)
            pantalla.blit(TextSurfStart, TextRectStart)

            for index, box in enumerate(input_boxes):
                if banderasInputs[index] == False:
                    box.draw(pantalla)

            for index, box in enumerate(inputs_difficulty):
                if banderasInputs[index] == True:
                    box.draw(pantalla)
                    pantalla.blit(RectsDif[index][0], RectsDif[index][1])

            pygame.display.flip()
            #reloj.tick(30)
        elif firstOne == 1:
            TextSurfMon1, TextRectMon1, TextSurfMon2, TextRectMon2, TextSurfMon3, TextRectMon3 = updateMontones(
                listaPiedras, color)
            pantalla.fill((30, 30, 30))

            pygame.draw.rect(pantalla, color["blanco"], monton1)
            pygame.draw.rect(pantalla, color["blanco"], monton2)

            pantalla.blit(TextSurfMon1, TextRectMon1)
            pantalla.blit(TextSurfMon2, TextRectMon2)
            pantalla.blit(TextSurfTurn, TextRectTurn)
            pantalla.blit(TextSurfName, TextRectName)

            for index, buttons in enumerate(botones):  ##########
                if banderasMontones[index] == True:
                    for index2, button in enumerate(buttons):
                        if bandsMontones[index][index2] == True:
                            pygame.draw.rect(pantalla, (255, 248, 224), button)

            for index, textos2 in enumerate(textos):  ##########
                if banderasMontones[index] == True:
                    for index2, texto in enumerate(textos2):
                        if bandsMontones[index][index2] == True:
                            pantalla.blit(texto[0], texto[1])

            if not isinstance(listaPiedras[2], str):
                pygame.draw.rect(pantalla, color["blanco"], monton3)
                pantalla.blit(TextSurfMon3, TextRectMon3)

            pygame.display.flip()
            pygame.time.delay(800)
            reloj.tick(30)
            firstOne = 2
        elif game == 3:
            pygame.time.delay(800)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit(0)
            if listaPiedras[-1] == "1":
                winner = 1
            else:
                winner = 0
            pantalla.fill((30, 30, 30))
            pos = (300, 300)
            largeText = pygame.font.SysFont("comicsansms", 48)
            TextSurf, TextRect = text_objects(nombres[winner], largeText, color["blanco"])
            TextRect.center = (pos)
            pantalla.blit(TextSurf, TextRect)

            pos = (300, 400)
            largeText = pygame.font.SysFont("comicsansms", 28)
            TextSurf, TextRect = text_objects("Winner", largeText, pygame.Color('dodgerblue2'))
            TextRect.center = (pos)
            pantalla.blit(TextSurf, TextRect)
            game = 3
            pygame.display.flip()
            # pygame.time.delay(10000)
        else:
            if dificultades[game-1] != 0:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit(0)

                pygame.time.delay(3000)
                choice = calculateChoice(dificultades, game)
                nodoActual, listaPiedras = updatePC(choice, listaPiedras, nodoActual)
                TextSurfName, TextRectName, game = turn(nombres, game)
                # TextSurfMon1, TextRectMon1, TextSurfMon2, TextRectMon2, TextSurfMon3, TextRectMon3 = updateMontones(listaPiedras, color)
                for index, textos2 in enumerate(textos):
                    for index2, texto in enumerate(textos2):
                        bandsMontones[index][index2] = False

                #pygame.time.delay(3000)

                pygame.display.flip()

            else:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit(0)

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = event.pos  # gets mouse position
                        # checks if mouse position is over the button
                        if monton1.collidepoint(mouse_pos):
                            counterMonton1, banderasMontones[0] = actionMonton1(listaPiedras[0], counterMonton1, bandsMonton1)

                        if monton2.collidepoint(mouse_pos):
                            counterMonton2, banderasMontones[1] = actionMonton2(listaPiedras[1], counterMonton2, bandsMonton2)

                        if not isinstance(listaPiedras[2], str):
                            if monton3.collidepoint(mouse_pos):
                                counterMonton3, banderasMontones[2] = actionMonton3(listaPiedras[2], counterMonton3, bandsMonton3)

                            if mon3_button1.collidepoint(mouse_pos):
                                nodoActual, listaPiedras = updateGame(3, -1, listaPiedras, arbolito, nodoActual)
                                TextSurfName, TextRectName, game = turn(nombres, game)
                                counterMonton3 = counterPlus(counterMonton3)
                                for index, textos2 in enumerate(textos):
                                    for index2, texto in enumerate(textos2):
                                        bandsMontones[index][index2] = False
                            if mon3_button2.collidepoint(mouse_pos):
                                nodoActual, listaPiedras = updateGame(3, -2, listaPiedras, arbolito, nodoActual)
                                TextSurfName, TextRectName, game = turn(nombres, game)
                                counterMonton3 = counterPlus(counterMonton3)
                                for index, textos2 in enumerate(textos):
                                    for index2, texto in enumerate(textos2):
                                        bandsMontones[index][index2] = False
                            if mon3_button3.collidepoint(mouse_pos):
                                nodoActual, listaPiedras = updateGame(3, -3, listaPiedras, arbolito, nodoActual)
                                TextSurfName, TextRectName, game = turn(nombres, game)
                                counterMonton3 = counterPlus(counterMonton3)
                                for index, textos2 in enumerate(textos):
                                    for index2, texto in enumerate(textos2):
                                        bandsMontones[index][index2] = False
                            if mon3_button4.collidepoint(mouse_pos):
                                nodoActual, listaPiedras = updateGame(3, -4, listaPiedras, arbolito, nodoActual)
                                TextSurfName, TextRectName, game = turn(nombres, game)
                                counterMonton3 = counterPlus(counterMonton3)
                                for index, textos2 in enumerate(textos):
                                    for index2, texto in enumerate(textos2):
                                        bandsMontones[index][index2] = False
                            if mon3_button5.collidepoint(mouse_pos):
                                nodoActual, listaPiedras = updateGame(3, -5, listaPiedras, arbolito, nodoActual)
                                TextSurfName, TextRectName, game = turn(nombres, game)
                                counterMonton3 = counterPlus(counterMonton3)
                                for index, textos2 in enumerate(textos):
                                    for index2, texto in enumerate(textos2):
                                        bandsMontones[index][index2] = False

                        if mon1_button1.collidepoint(mouse_pos):
                            nodoActual, listaPiedras = updateGame(1, -1, listaPiedras, arbolito, nodoActual)
                            TextSurfName, TextRectName, game = turn(nombres, game)
                            counterMonton1 = counterPlus(counterMonton1)
                            for index, textos2 in enumerate(textos):
                                for index2, texto in enumerate(textos2):
                                    bandsMontones[index][index2] = False
                        if mon1_button2.collidepoint(mouse_pos):
                            nodoActual, listaPiedras = updateGame(1, -2, listaPiedras, arbolito, nodoActual)
                            TextSurfName, TextRectName, game = turn(nombres, game)
                            counterMonton1 = counterPlus(counterMonton1)
                            for index, textos2 in enumerate(textos):
                                for index2, texto in enumerate(textos2):
                                    bandsMontones[index][index2] = False
                        if mon1_button3.collidepoint(mouse_pos):
                            nodoActual, listaPiedras = updateGame(1, -3, listaPiedras, arbolito, nodoActual)
                            TextSurfName, TextRectName, game = turn(nombres, game)
                            counterMonton1 = counterPlus(counterMonton1)
                            for index, textos2 in enumerate(textos):
                                for index2, texto in enumerate(textos2):
                                    bandsMontones[index][index2] = False
                        if mon1_button4.collidepoint(mouse_pos):
                            nodoActual, listaPiedras = updateGame(1, -4, listaPiedras, arbolito, nodoActual)
                            TextSurfName, TextRectName, game = turn(nombres, game)
                            counterMonton1 = counterPlus(counterMonton1)
                            for index, textos2 in enumerate(textos):
                                for index2, texto in enumerate(textos2):
                                    bandsMontones[index][index2] = False
                        if mon1_button5.collidepoint(mouse_pos):
                            nodoActual, listaPiedras = updateGame(1, -5, listaPiedras, arbolito, nodoActual)
                            TextSurfName, TextRectName, game = turn(nombres, game)
                            counterMonton1 = counterPlus(counterMonton1)
                            for index, textos2 in enumerate(textos):
                                for index2, texto in enumerate(textos2):
                                    bandsMontones[index][index2] = False
                        if mon2_button1.collidepoint(mouse_pos):
                            nodoActual, listaPiedras = updateGame(2, -1, listaPiedras, arbolito, nodoActual)
                            TextSurfName, TextRectName, game = turn(nombres, game)
                            counterMonton2 = counterPlus(counterMonton2)
                            for index, textos2 in enumerate(textos):
                                for index2, texto in enumerate(textos2):
                                    bandsMontones[index][index2] = False
                        if mon2_button2.collidepoint(mouse_pos):
                            nodoActual, listaPiedras = updateGame(2, -2, listaPiedras, arbolito, nodoActual)
                            TextSurfName, TextRectName, game = turn(nombres, game)
                            counterMonton2 = counterPlus(counterMonton2)
                            for index, textos2 in enumerate(textos):
                                for index2, texto in enumerate(textos2):
                                    bandsMontones[index][index2] = False
                        if mon2_button3.collidepoint(mouse_pos):
                            nodoActual, listaPiedras = updateGame(2, -3, listaPiedras, arbolito, nodoActual)
                            TextSurfName, TextRectName, game = turn(nombres, game)
                            counterMonton2 = counterPlus(counterMonton2)
                            for index, textos2 in enumerate(textos):
                                for index2, texto in enumerate(textos2):
                                    bandsMontones[index][index2] = False
                        if mon2_button4.collidepoint(mouse_pos):
                            nodoActual, listaPiedras = updateGame(2, -4, listaPiedras, arbolito, nodoActual)
                            TextSurfName, TextRectName, game = turn(nombres, game)
                            counterMonton2 = counterPlus(counterMonton2)
                            for index, textos2 in enumerate(textos):
                                for index2, texto in enumerate(textos2):
                                    bandsMontones[index][index2] = False
                        if mon2_button5.collidepoint(mouse_pos):
                            nodoActual, listaPiedras = updateGame(2, -5, listaPiedras, arbolito, nodoActual)
                            TextSurfName, TextRectName, game = turn(nombres, game)
                            counterMonton2 = counterPlus(counterMonton2)
                            for index, textos2 in enumerate(textos):
                                for index2, texto in enumerate(textos2):
                                    bandsMontones[index][index2] = False

            TextSurfMon1, TextRectMon1, TextSurfMon2, TextRectMon2, TextSurfMon3, TextRectMon3 = updateMontones(
                listaPiedras, color)
            pantalla.fill((30, 30, 30))

            pygame.draw.rect(pantalla, color["blanco"], monton1)
            pygame.draw.rect(pantalla, color["blanco"], monton2)

            pantalla.blit(TextSurfMon1, TextRectMon1)
            pantalla.blit(TextSurfMon2, TextRectMon2)
            pantalla.blit(TextSurfTurn, TextRectTurn)
            pantalla.blit(TextSurfName, TextRectName)

            for index, buttons in enumerate(botones): ##########
                if banderasMontones[index] == True:
                    for index2, button in enumerate(buttons):
                        if bandsMontones[index][index2] == True:
                            pygame.draw.rect(pantalla, (255, 248, 224), button)

            for index, textos2 in enumerate(textos): ##########
                if banderasMontones[index] == True:
                    for index2, texto in enumerate(textos2):
                        if bandsMontones[index][index2] == True:
                            pantalla.blit(texto[0], texto[1])

            if not isinstance(listaPiedras[2], str):
                pygame.draw.rect(pantalla, color["blanco"], monton3)
                pantalla.blit(TextSurfMon3, TextRectMon3)

            pygame.display.flip()
            '''if dificultades[game - 1] != 0:
                pygame.time.delay(3000)'''
            game = checkIfWins(listaPiedras, pantalla, color, nombres, game)
            reloj.tick(30)


if __name__ == '__main__':
    main()