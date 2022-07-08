'''
Controle de braço robótico via serial
Mais detalhes: https://github.com/guilherme3a/robotic-arm

Autor: Guilherme Augusto
Data:  06/2022
'''

# importacao das bibliotecas -----------------------------------------------------

# interface GUI
from time import sleep
import PySimpleGUI as sg
from collections import deque

# grafico 2D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# calculos
import matplotlib.pyplot as plt
import numpy as np
from math import pi, sin, cos

# com serial
import serial
import serial.tools.list_ports

# variaveis globais --------------------------------------------------------------
com = []                    # armazena as portas seriais
refAngular = [90, 135, 0]   # posicao angular referencia
posAngular = [90, 135, 0]   # posicao angular enviada
refCart = [12, 0, 4]        # posicao cartesianda referencia
posCart = []                # posicao cartesiana enviada

fila = deque([])
garra = 1

# funcao para mostrar grafico ----------------------------------------------------
def drawFigure(canvas, figure):
    if canvas.children:
        for child in canvas.winfo_children():
            child.destroy()
    figure_canvas_agg = FigureCanvasTkAgg(figure, master=canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

# calculos e plots do grafico ----------------------------------------------------
def geraGrafico(t1, t2, t3):
    global posCart

    # conversao de graus para radianos
    theta1 = t1*(pi/180)
    theta2 = t2*(pi/180)
    theta3 = t3*(pi/180)

    # coordenadas do primeiro ponto
    a = [12*cos(theta1), 12*sin(theta1)]

    # coordenadas do segundo ponto
    b = [a[0]+12*cos(pi-theta2), a[1]-12*sin(pi-theta2)]

    # coordenadas do efetuador
    c = [b[0]+4, b[1]]
    yc = (12*cos(theta1)+12*cos(pi-theta2))*sin(theta3)
    
    posCart = [round(c[0]*cos(theta3)), round(yc), round(c[1])]
    print(f'P(x,y,z) = ({posCart[0]}, {posCart[1]}, {posCart[2]})')
    print('-------------------------------------------')

    # coordenadas paralelogramo
    d = np.array([0, -4*cos(pi-theta2)])
    e = np.array([0, 4*sin(pi-theta2)])
    f = np.array([a[0], d[1]+a[0]])
    g = np.array([a[1], e[1]+a[1]])
    h = np.array([d[1], d[1]+a[0]])
    i = np.array([e[1], e[1]+a[1]])

    # coordenadas base
    bx = np.array([-4, 4])
    by = np.array([0, 0])

    x = np.array([0, a[0], b[0], c[0]])
    y = np.array([0, a[1], b[1], c[1]])
    
    # plots
    plt.plot(x, y, color='k', lw=2, marker='o')
    plt.plot(bx, by, color='k', lw=2, marker='o')
    plt.plot(d, e, color='k', lw=2, marker='o')
    plt.plot(f, g, color='k', lw=2, marker='o')
    plt.plot(h, i, color='k', lw=2, marker='o')

    plt.xlim(-15, 25)
    plt.ylim(-15, 25)
    plt.grid()

# envia string -------------------------------------------------------------------
def enviaStr(t1, t2, t3):
    global refAngular, posAngular, fila
    
    steps1 = str(2 * (abs(int(refAngular[0]) - t1)))
    steps2 = str(2 * (abs(int(refAngular[1]) - t2)))
    steps3 = str(2 * (abs(int(refAngular[2]) - t3)))

    completeZeroS1 = '0' * (3 - len(steps1))    # motor 2 do prototipo
    completeZeroS2 = '0' * (3 - len(steps2))    # motor 3 do prototipo
    completeZeroS3 = '0' * (3 - len(steps3))    # motor 1 do prototipo
    
    # move M1
    if(int(posAngular[2]) >= int(refAngular[2])):
        s3 = completeZeroS3 + str(2 * (t3 - int(refAngular[2])))
        fila.append('1' + s3 + '1\n')
    else:
        s3 = completeZeroS3 + str(2 * (int(refAngular[2]) - t3))
        fila.append('1' + s3 + '0\n')

    # move M2 antes de M3
    if(int(posAngular[0]) <= int(refAngular[0])):
        s1 = completeZeroS1 + str(2 * (int(refAngular[0]) - t1))
        fila.append('2' + s1 + '1\n')

        if(int(posAngular[1]) <= int(refAngular[1])):
            s2 = completeZeroS2 + str(2 * (int(refAngular[1]) - t2))
            fila.append('3' + s2 + '0\n')
        else:
            s2 = completeZeroS2 + str(2 * (t2 - int(refAngular[1])))
            fila.append('3' + s2 + '1\n')
    
    # move M3 antes de M2
    elif(int(posAngular[0]) > int(refAngular[0])):
        if(int(posAngular[1]) <= int(refAngular[1])):
            s2 = completeZeroS2 + str(2 * (int(refAngular[1]) - t2))
            fila.append('3' + s2 + '0\n')
        else:
            s2 = completeZeroS2 + str(2 * (t2 - int(refAngular[1])))
            fila.append('3' + s2 + '1\n')

        s1 = completeZeroS1 + str(2 * (t1 - int(refAngular[0])))
        fila.append('2' + s1 + '0\n')

    # escreve na serial ------------------------------------------------------
    leitura3 = fila.popleft()
    conexao.write(leitura3.encode())
    conexao.flush()

    while True :
        verif1 = conexao.read(2).decode()

        if(str(verif1) == 'ok'):
            break
    
    leitura2 = fila.popleft()
    conexao.write(leitura2.encode())
    conexao.flush()
    
    while True :
        verif2 = conexao.read(2).decode()
        if(verif2 == 'ok'):
            break
    
    leitura1 = fila.popleft()
    conexao.write(leitura1.encode())
    conexao.flush()
    
    while True:
        verif3 = conexao.read(2).decode()
        if(verif3 == 'ok'):
            break

    print(f'{leitura3}{leitura2}{leitura1}')

    refAngular = posAngular

# tratamento de falha na comunicacao ---------------------------------------------
def falhaSerial():
    sg.theme('DefaultNoMoreNagging')

    janelaFalha = sg.Window(
        'Com Error',
        sg.popup('Falha na Comunicação Serial.\nVerifique o cabo e tente novamente.',
        title='COM Error', icon='icon.ico')
    )

    events = janelaFalha.read()
    if events == sg.WIN_CLOSED:
        janelaFalha.close()
    
# comunicacao serial -------------------------------------------------------------
while True:
    try:
        com = [port.device for port in serial.tools.list_ports.comports()]
        conexao = serial.Serial(com[0], baudrate=4800, timeout=0.5)
        sleep(3)
        conexao.flush()
        break
    except:
        falhaSerial()

"""com = [port.device for port in serial.tools.list_ports.comports()]
conexao = serial.Serial(com[0], 4800)
conexao.flush()"""

# tema da janela -----------------------------------------------------------------
sg.theme('DefaultNoMoreNagging')

# menu superior ------------------------------------------------------------------
menu_layout = [
    ['Ferramentas',['Guia do Usuário', 'Porta Serial', [com]]],
    ['Ajuda',['Consultar Repositótio', 'Sobre']]
]

# primeira coluna do layout ------------------------------------------------------
cln1_layout = [
    [sg.Button('Auto Home', size=(10,1)), sg.Button('Acionar Garra', size=(12,1))],
    [sg.Text('Coordenadas Articulares', font=('Arial', 10), size=(28,1), justification='c')],
    [sg.Input(size=(7,1), key='c1'), sg.Input(size=(7,1), key='c2'), sg.Input(size=(7,1), key='c3')],
    [sg.Text('t1', size=(7,1), justification='c'), sg.Text('t2', size=(7,1), justification='c'), sg.Text('t3', size=(7,1), justification='c')],
    [sg.Button('Mover para Posição (Enter)', size=(24,1), bind_return_key=True)],
    [sg.Output(size=(24,7))],
    [sg.Text('', key='posicao', size=(24,1), justification='c')]
]

# segunda coluna do layout -------------------------------------------------------
cln2_layout = [
    [sg.Canvas(key='-CANVAS-')]
]

# layout completo ----------------------------------------------------------------
layout = [
    [sg.Menu(menu_layout)],
    [sg.Text('ROBOTIC ARM CONTROLLER', font=('Arial', 16), size = (100,1), justification='c')],
    [sg.Text('Cinemática direta', size=(27,1), justification='c'), sg.Text('Gráfico 2D', size=(100,1), justification='c')],
    [sg.Column(cln1_layout), sg.VSeparator(), sg.Column(cln2_layout)],
    [sg.Text('', key='log', size=(100,1), justification='c')]
]

# criação da janela --------------------------------------------------------------
janela = sg.Window('ROBOTIC ARM CONTROLLER v.1.0.0', layout, finalize=True, font=('Arial', 12), icon='icon.ico', size=(630,430))

# loop principal -----------------------------------------------------------------
while True:
    events, values = janela.read()

    # janela principal -----------------------------------------------------------
    # menu -----------------------------------------------------------------------
    if events == 'Guia do Usuário':
        line1 = 'Na opção \'Cinemática Direta\' (à esquerda) o usuário encontra duas opções: \n'
        line2 = '- Enviar o manipulador para a posição de referência (Auto Home). \n'
        line3 = '- Fornecer as coordenadas articulares desejadas (t1, t2 e t3). \n'
        line4 = '\nA interface exibe as últimas coordenadas articulares e a posição do atuador P(x,y,z). \n'
        line5 = 'À direita do layout, um gráfico bidimensional (y = 0) apresenta o comportamento assumido pelo braço. \n'
        sg.popup(line1 + '\n' + line2 + '\n' + line3 + '\n' + line4 + '\n' + line5, title='Guia do Usuário', icon='icon.ico')

    if events == com[0]:
        janela['log'].update(f'Porta {com[0]} conectada')
        conexao.close()
        conexao = serial.Serial(com[0], 4800)
    
    if events == 'Consultar Repositótio':
        sg.popup('Para mais informações, acesse:\nhttps://github.com/guilherme3a/robotic-arm', title='GitHub', icon='icon.ico')

    if events == 'Sobre':
        sg.popup('Interface desenvolvida em Python 3 com a biblioteca PySimpleGUI \nAutor: Guilherme Augusto Alves Alvin', title='Sobre', icon='icon.ico')

    # fechar/minimizar -----------------------------------------------------------
    if events == sg.WIN_CLOSED:
        break

    if events == sg.SYMBOL_TITLEBAR_MINIMIZE:
        break

    # comando Auto Home ----------------------------------------------------------
    if events == 'Auto Home':
        janela['posicao'].update('Auto Home')
        posAngular = [90, 135, 0]
        enviaStr(90, 135, 0)

        plt.figure(1)
        fig = plt.gcf()
        plt.cla()
        plt.clf()

        geraGrafico(90, 135, 0)
        drawFigure(janela['-CANVAS-'].TKCanvas, fig)

        home = '00000\n'
        conexao.write(home.encode())
        conexao.flush()
    
    # comando Acionar Garra ------------------------------------------------------
    if events == 'Acionar Garra':
        janela['posicao'].update('Garra Acionada')

        while True:
            if(len(fila) == 0):
                break

        leitura4 = '4000' + str(garra) + '\n'
        conexao.write(leitura4.encode())
        conexao.flush()

        if(garra == 0):
            garra = 1
        else:
            garra = 0
    
    # comando Mover para Posicao -------------------------------------------------
    if events == 'Mover para Posição (Enter)':
        t1, t2, t3 = [values['c1'], values['c2'], values['c3']]
        posAngular = [t1, t2, t3]

        sum = t1 + t2 + t3
        if t1!='' and t2!='' and t3!='' and sum.isdigit():
            enviaStr(int(t1), int(t2), int(t3))
            janela['posicao'].update(f'Ângulos => ({t1}, {t2}, {t3})')

            plt.figure(1)
            fig = plt.gcf()
            
            DPI = fig.get_dpi()
            fig.set_size_inches(320 / float(DPI), 320 / float(DPI))

            plt.cla()
            plt.clf()

            geraGrafico(int(t1), int(t2), int(t3))
            drawFigure(janela['-CANVAS-'].TKCanvas, fig)
        else:
            janela['posicao'].update('Entrada inválida')
        
        janela['c1'].update(''); janela['c2'].update(''); janela['c3'].update('')
    
conexao.close()
janela.close()