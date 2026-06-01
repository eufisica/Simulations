from vpython import *
from tkinter import *
def ajuda():
    newWindow = Toplevel(janela)
    newWindow.geometry('520x490+100+150')
    newWindow.title('AJUDA')
    newWindow['pady']=20
    newWindow['padx']=30
    lab_title2 = Label(newWindow, text='SISTEMA COM POLIA FIXA', font='times 20 bold', height=3)
    lab_title2.grid(row=0, column=0)
    a = 'O sistema se trata de dois blocos ligados por um fio inestensível, '
    a = a + 'que passa por uma polia fixa, tendo um bloco suspenso pelo fio e outro'
    a = a + 'apoiado a uma parede. A partir da massa dos blocos e da altura em que o bloco '
    a = a + 'suspenso se encontra em relação ao solo, é possível caracterizar o estado '
    a = a + 'de movimento do sistema com a sua aceleração. '
    a = a + '\n\nNa simulação, é também possível verificar os vetores do peso e da tração nas cordas.'
    lab_desc = Label(newWindow, font='times 12 ',text=a, wraplength=450)
    lab_desc.grid(row=1, column=0)

def bt_clic():
    try:
        Parede = box(pos=vector(-5,0.5,0),size=vector(10,10,3),color=color.orange)
        Solo = box(pos=vector(-2,-4,0),size=vector(16,1,3),color=color.orange)
        #Construção da Polia (Conjunto de Cilindros e dois Box)
        polia_a = cylinder(pos=vector(1.7,6.2,0),axis=vector(0,0,0.1), radius=0.6, color = color.yellow)
        1
        polia_b = cylinder(pos=vector(1.7,6.2,0.1),axis=vector(0,0,0.2), radius=0.8, color = color.white)
        polia_c = cylinder(pos=vector(1.7,6.2,-0.2),axis=vector(0,0,0.2), radius=0.8, color = color.white)
        barra_polia_b = box(pos=vector(0.8, 5.7, 0.39),size=vector(2.5,0.3,0.1), axis = vector(0.5, 0.3, 0),color=color.gray(0.5))
        barra_polia_c = box(pos=vector(0.8, 5.7, -0.29),size=vector(2.5,0.3,0.1), axis = vector(0.5, 0.3, 0),color=color.gray(0.5))
        #Cordas
        corda_a = cylinder(pos=vector(-7,6.75,0),axis=vector(9,0,0), radius=0.05, color = color.yellow)
        corda_b = cylinder(pos=vector(2.3,5,0),axis=vector(0,1,0), radius=0.05, color = color.yellow)
        #Blocos
        massa_a = box(pos=vector(-8,6.5,0),size=vector(2,2,2),color=color.red, mass = 0)
        massa_b = box(pos=vector(2.3,4,0),size=vector(2,2,2),color=color.blue, mass = 0)
        #Vetores
        vetor_a = arrow(pos = massa_a.pos + vec(0,0.25,0), axis = vec(2.5, 0, 0), shaftwidth=0.15)
        vetor_b = arrow(pos = massa_b.pos, axis = vec(0, 2.5, 0), shaftwidth=0.15)
        vetor_peso = arrow(pos = massa_b.pos, axis = vec(0, -2.5, 0), shaftwidth=0.15)
        #Dados
        massa_a.mass = float(ed_mass_a.get())
        massa_b.mass = float(ed_mass_b.get())
        h = float(ed_h.get())
        #Legenda com a Altura
        h_label = label(pos=vec(3.3,3,0), text='Altura: y = '+ str(h), xoffset=50, yoffset=0, space=30, height=16, border=4, font='sans')
        g = 9.81 #gravidade
        a = massa_b.mass*g/(massa_a.mass+massa_b.mass) #aceleração
        t_total = (2*h/a)**(1/2) #tempo total
        janela.destroy()
        if (t_total <= 0.5): #Variável de controle do tempo para tempos muito curtos
            c = 5
        elif (t_total <= 1):
            c = 10
        elif (t_total <= 2):
            c = 20
        elif (t_total <= 3):
            c = 30
        elif (t_total <= 4):
            c = 40   
        elif (t_total <= 5):
            c = 50
        else:
            c = 100
        e = h/6.5 #controle de escala
        dt=0.01
        t=0
        while(t < t_total):
            rate (c) #Controle do Tempo
            t+=dt
            #Mudança de Posição em A
            massa_a.pos.x = (((a/2)*(t**2))/e) - 8
            corda_a.pos.x = -7 + (((a/2)*(t**2))/e)
            corda_a.axis.x = 9 - (((a/2)*(t**2))/e)
            vetor_a.pos = massa_a.pos + vec(0,0.25,0)
            #Mudança de Posição em B
            massa_b.pos.y = 4 - (((a/2)*(t**2))/e)
            corda_b.pos.y = 5 - (((a/2)*(t**2))/e)
            corda_b.axis.y = 1 + (((a/2)*(t**2))/e)
            vetor_b.pos = massa_b.pos
            vetor_peso.pos = massa_b.pos
            h_label.text = 'h = ' + str(h - round((a/2)*(t**2), 2))
            h_label.pos=massa_b.pos
        #Definindo os Valores Finais dos Vetores
        vetor_a.shaftwidth = 0.01
        vetor_b.shaftwidth = 0.01
        vetor_peso.shaftwidth = 0.01
        h_label.text = 'h = 0'
    except:
        lb1['text']='Valores Informados Inválidos!!!'

janela = Tk()
janela.geometry('650x430+400+150')
janela.title('SIMULAÇÕES')
janela['pady']=20
janela['padx']=30
container = Frame(janela, highlightbackground='black', highlightthickness=2)
container['pady']=20
container['padx']=35
container.grid(row=0, column=0)
lab_title = Label(container, text='SISTEMA COM POLIA FIXA', font='times 20 bold', height=3)
lab_mass_a = Label(container, text='Insira a Massa (kg) do Bloco Suspenso: ', font='times 14 ', height=2)
lab_mass_b = Label(container, text='Insira a Massa (kg) do Bloco Apoiado: ', font='times 14 ', height=2)
lab_h = Label(container, text='Insira a Altura de Queda (m): ', font='times 14 ', height=2)
lab_title.grid(row=0, column=0, columnspan=4)
lab_mass_a.grid(row=1, column=0, columnspan=2, sticky=W)
lab_mass_b.grid(row=2, column=0, columnspan=2, sticky=W)
lab_h.grid(row=3, column=0, columnspan=2, sticky=W)
ed_mass_b = Entry(container, width=26,font='times 12')
ed_mass_a = Entry(container, width=26,font='times 12')
ed_h = Entry(container, width=26,font='times 12')
ed_mass_a.grid(row=1, column=2, columnspan=2, sticky=W)
ed_mass_b.grid(row=2, column=2, columnspan=2, sticky=W)
ed_h.grid(row=3, column=2, columnspan=2, sticky=W)
lb1 = Label(container, text='', height=1, font='times 12 italic')
lb1.grid(row=4, column=1, columnspan=2)
bt = Button(container, text = 'Gerar Simulação', font='times 14 bold', pady=12, command=bt_clic)
bt.grid(row=5, column=1, columnspan=2, sticky=S)
buttonExample = Button(container, text='Ajuda', font='times 12 bold', command=ajuda)
buttonExample.grid(row=5, column=0, columnspan=2, sticky=W)
janela.mainloop()