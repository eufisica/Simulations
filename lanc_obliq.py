from tkinter import *
from vpython import *
import math
#posição da partícula na coordenada x versus o tempo
graf_pos_x = graph(xtitle="tempo (s)", ytitle="Posição (m)")
curva_pos_x = gcurve(color=color.red, label = "Coordenada X")
#posição da partícula na coordenada y versus o tempo
graf_pos_y = graph(xtitle="tempo (s)", ytitle="Posição (m)")
curva_pos_y = gcurve(color=color.red, label = "Coordenada Y")
#velocidade da partícula na coordenada y versus o tempo
graf_vel_y = graph(xtitle="tempo (s)", ytitle="velocidade (m)")
curva_vel_y = gcurve(color=color.red, label = "Coordenada Y")

def ajuda(): #janela de ajuda
    newWindow = Toplevel(janela) #janela de ajuda
    newWindow.geometry('520x480+100+150') #tamanho da janela de ajuda (largura x altura + posição x + posição y)
    newWindow.title('AJUDA') #título da janela de ajuda
    newWindow['pady']=20 #espaçamento entre os elementos da janela de ajuda e entre eles mesmos
    newWindow['padx']=30 #espaçamento entre os elementos da janela de ajuda e a borda da janela de ajuda
    lab_title2 = Label(newWindow, text='Lançamento Oblíquo', font='times 20 bold', height=3)
    lab_title2.grid(row=0, column=0)
    a = 'O lançamento oblíquo se caracteriza por ser um movimento curvilíneo, em que um corpo é '
    a = a + 'lançado a parir de um ângulo com uma velocidade inicial, realizando uma trajetória '
    a = a + 'parabôlica. Nele, a velocidade na componente x é constante, enquanto que na componente y '
    a = a + 'é acelerado devido justamente à aceleração da gravidade. '
    a = a + '\n\nNa simulação é possível visualizar a trajetória do corpo formada por pontos que '
    a = a + 'aparecem em intervalos de tempos iguais - como dito, uma trajetória parabôlica. '
    a = a + 'É possível verificar também que o espaço de um ponto a outro na componente x é igual e '
    a = a + 'na componente y varia, o que indica que a variação da posição do corpo em relação ao tempo '
    a = a + 'é constante em x e acelerado em y. (Em alguns casos, no início da simulação a trajetória '
    a = a + 'pode conter algumas incoerências devido a um atraso na inicialização da simulação). '
    a = a + 'Outros sim, ao longo da trajetória, é marcado o posição inicial, posição de máximo e posição final. '
    lab_desc = Label(newWindow, font='times 12 ',text=a, wraplength=450) #descrição da janela de ajuda
    lab_desc.grid(row=1, column=0) #organização da descrição da janela de ajuda
    
def bt_clic():
    try:
        i_vel=float(ed_i_vel.get()) #velocidade inicial
        tet=float(ed_i_tet.get()) #ângulo de lançamento
        x_pos=float(ed_i_x.get()) #posição inicial da partícula na coordenada x
        y_pos=float(ed_i_y.get()) #posição inicial da partícula na coordenada y
        g = 9.81 #valor da gravidade
        t = math.sin(math.radians(tet))*(i_vel/g) #tempo de subida
        y_max = y_pos + ((i_vel*math.sin(math.radians(tet)))**2)/(2*g) #altura máxima
        x_y_max = x_pos + i_vel*math.cos(math.radians(tet))*t #correspondente em x da altura máxima
        x_vel = i_vel*math.cos(math.radians(tet)) #Velocidade em x
        if (y_pos > 0):
            t +=(2*y_max/g)**(1/2) #tempo de subida + tempo de descida (tempo total)
        else:t = t*2 #tempo de subida + tempo de descida (tempo total)
        if (t <= 0.5): #Variável de controle do tempo para tempos muito curtos
            c = 5
        elif (t <= 2): 
            c = 20
        elif (t <= 3):
            c = 30
        elif (t <= 4):
            c = 40
        elif (t <= 5):
            c = 50
        else:
            c = 100
        delt_sx = i_vel*math.cos(math.radians(tet))*t #variação da posição total em x
        x_max = x_pos + delt_sx #alcance total
        ey = y_max/10 #variável controle de escala (Coordenada Y)
        ex = delt_sx/20 #variável controle de escala (Coordenada X)
        i_pos = (y_pos*10)/y_max - 5 #posição inicial relativa da partícula na interface do vpython
        ball = sphere(pos = vec(-10, i_pos, 0), radius = 0.5, color = color.red, make_trail=True, trail_type='points', trail_color =color.yellow, interval = c/10) #partícula para a simulação
        L_origem = label(pos=ball.pos, text='('+str(x_pos)+', '+str(y_pos)+') m', yoffset=50, xoffset = -30, space=30, height=14, border=4, font='sans') #posição inicial da partícula
        L_medio = label(pos=vec(((x_y_max-x_pos) -(x_max-x_pos)/2)*(20/delt_sx), 5, 0), text='('+str(round(x_y_max, 2))+', '+str(round(y_max, 2))+') m', yoffset=50, xoffset = 0, space=30, height=14, border=4, font='sans') #posição de máxima da partícula
        L_fim = label(pos=vec(10, -5, 0), text='('+str(round(x_max, 2))+', 0) m', yoffset=50, xoffset = 30, space=30, height=14, border=4, font='sans')
        solo = box(pos=vector(0,-5.6,0), size=vector(26,0.2,2)) #solo para a simulação
        dt = 0.01 #intervalo de tempo para a simulação (quanto menor, mais fluida, mas mais lenta)
        ts = 0 #passagem do tempo
        janela.destroy() #fechar a janela de entrada de dados para a simulação
        while (ts<t):
            rate (c) #controle do tempo (c=100, implica em tempo real)
            curva_pos_y.plot(pos=(ts, y_pos + i_vel*math.sin(math.radians(tet))*ts - (g/2)*(ts**2))) #gráfico posição em y
            curva_pos_x.plot(pos=(ts, x_pos + i_vel*math.cos(math.radians(tet))*ts)) # gráfico posição em x
            curva_vel_y.plot(pos=(ts, i_vel*math.sin(math.radians(tet)) -g*ts)) # gráfico velocidade em y
            ball.pos.y = (((i_vel*math.sin(math.radians(tet))*ts) - ((g/2)*(ts**2)))/ey) + i_pos #mudança de posição em y
            ball.pos.x = ((i_vel*math.cos(math.radians(tet))*ts )/ex) -10 #mudança de posição
            ts += dt
        while True:
            rate(30)
    except:
        lb1['text']='Valores Informados Inválidos!!!'
            
janela = Tk()
janela.geometry('520x490+400+150') #tamanho da janela de entrada de dados (largura x altura + posição x + posição y)
janela.title('SIMULAÇÕES') #título da janela de entrada de dados
janela['pady']=20 #espaçamento entre os elementos da interface gráfica (labels, entry, button) e entre eles mesmos
janela['padx']=30 #espaçamento entre os elementos da interface gráfica (labels, entry, button) e a borda da janela de entrada de dados
container = Frame(janela, highlightbackground='black', highlightthickness=2)
container['pady']=20 #espaçamento entre os elementos da interface gráfica (labels, entry, button) e entre eles mesmos
container['padx']=35 #espaçamento entre os elementos da interface gráfica (labels, entry, button) e a borda do container
container.grid(row=0, column=0) #container para organizar os elementos da janela de entrada de dados
lab_title = Label(container, text='Lançamento Oblíquo', font='times 20 bold', height=3) #título da janela de entrada de dados
lab_i_pos = Label(container, text='Velocidade Inicial (m/s):', font='times 14', height=3) #labels para os dados de entrada
lab_i_vel = Label(container, text='Ângulo (°):', font='times 14 ', height=3) #labels para os dados de entrada
lab_ti = Label(container, text='x_inicial (m):', font='times 14 ', height=3) #labels para os dados de entrada
lab_tf = Label(container, text='y_inicial (m):', font='times 14 ', height=3) #labels para os dados de entrada
lab_title.grid(row=0, column=0, columnspan=4) #organização do título da janela de entrada de dados
lab_i_pos.grid(row=1, column=0, columnspan=2, sticky=W) #organização dos labels para os dados de entrada
lab_i_vel.grid(row=2, column=0, columnspan=2, sticky=W) #organização dos labels para os dados de entrada
lab_ti.grid(row=3, column=0, sticky=W) #organização dos labels para os dados de entrada
lab_tf.grid(row=3, column=2, sticky=W) #organização dos labels para os dados de entrada
ed_i_vel = Entry(container, width=26,font='times 12') #entry para os dados de entrada velocidade inicial
ed_i_tet = Entry(container, width=26,font='times 12') #entry para os dados de entrada ângulo de lançamento
ed_i_x = Entry(container, width=7,font='times 12') #entry para os dados de entrada da posição inicial da partícula na coordenada x
ed_i_y = Entry(container, width=7,font='times 12') #entry para os dados de entrada da posição inicial da partícula na coordenada y
ed_i_vel.grid(row=1, column=2, columnspan=2, sticky=W) #organização dos entry para os dados de entrada
ed_i_tet.grid(row=2, column=2, columnspan=2, sticky=W) #organização dos entry para os dados de entrada
ed_i_x.grid(row=3, column=1, sticky=W) #organização dos entry para os dados de entrada
ed_i_y.grid(row=3, column=3, sticky=W) #organização dos entry para os dados de entrada
lb1 = Label(container, text='', height=2, font='times 12 italic') #label para mensagens de erro (valores de entrada inválidos)
lb1.grid(row=4, column=1, columnspan=2) #organização do label para mensagens de erro (valores de entrada inválidos)
bt = Button(container, text = 'Gerar Simulação', font='times 14 bold', pady=12, command=bt_clic) #botão para iniciar a simulação
bt.grid(row=5, column=1, columnspan=2, sticky=S) #organização do botão para iniciar a simulação
buttonExample = Button(container, text='Ajuda', font='times 12 bold', command=ajuda) #botão para aceder a janela de ajuda
buttonExample.grid(row=5, column=0, columnspan=2, sticky=W) #organização do botão para aceder a janela de ajuda
janela.mainloop() #iniciar a janela de entrada de dados