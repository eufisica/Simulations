from vpython import *

# --- Configuração da Janela de Animação ---
# Definimos align="left" para que os gráficos tentem alinhar-se à sua direita
scene = canvas(title="Simulação Física: Queda com Resistência do Ar - José Gonçalves (eufisica)", 
               width=500, height=500, 
               background=color.white, 
               align="left")

# --- Configuração dos Gráficos (Inicializados no arranque) ---
# Definimos larguras fixas para forçar o alinhamento horizontal
grafico_pos = graph(title="Altura vs Tempo", xtitle="t (s)", ytitle="y (m)", 
                    width=350, height=250, align="left", background=color.white)
curva_pos = gcurve(graph=grafico_pos, color=color.blue)

grafico_vel = graph(title="Velocidade vs Tempo", xtitle="t (s)", ytitle="v (m/s)", 
                    width=350, height=250, align="left", background=color.white)
curva_vel = gcurve(graph=grafico_vel, color=color.red)

# --- Objetos ---
# Removido 'make_trail=True' para tirar a linha vermelha
chao = box(pos=vector(0, -2, 0), size=vector(300, 4, 300), color=color.gray(0.7))
esfera = sphere(pos=vector(0, 100, 0), radius=6, color=color.orange)

# --- Variáveis Físicas ---
g = vector(0, -9.81, 0)
v = vector(0, 0, 0)
m = 1.0
t = 0
dt = 0.01
k = 0.1
executando = False

def ajustar_camera(altura):
    scene.center = vector(0, altura / 2, 0)
    scene.range = altura * 0.8

# --- Funções de Controlo ---
def toggle_sim():
    global executando
    if esfera.pos.y <= esfera.radius:
        reset_sim()
    executando = not executando
    btn_start.text = "Pausar" if executando else "Largar Esfera"

def reset_sim():
    global v, t, executando
    executando = False
    btn_start.text = "Largar Esfera"
    esfera.pos = vector(0, slider_h.value, 0)
    v = vector(0, 0, 0)
    t = 0
    curva_pos.delete()
    curva_vel.delete()
    ajustar_camera(slider_h.value)

def set_altura(s):
    if not executando:
        esfera.pos.y = s.value
        ajustar_camera(s.value)
    lbl_h.text = f" Altura Inicial: {s.value}m"

def set_resistencia(s):
    global k
    k = s.value
    lbl_k.text = f" Coeficiente de Arrasto (k): {s.value:.2f}"

# --- Interface (HTML abaixo da simulação) ---
scene.append_to_caption("\n")
btn_start = button(text="Largar Esfera", bind=toggle_sim, background=color.green)
button(text="Reiniciar Configurações", bind=reset_sim)
scene.append_to_caption("\n\n")

slider_h = slider(min=10, max=500, value=100, bind=set_altura)
lbl_h = wtext(text=" Altura Inicial: 100m")
scene.append_to_caption("\n\n")

slider_k = slider(min=0, max=2, value=0.1, step=0.01, bind=set_resistencia)
lbl_k = wtext(text=" Coeficiente de Arrasto (k): 0.10")
scene.append_to_caption("\n\n")

# Inicialização da vista
ajustar_camera(100)

# --- Loop de Simulação Realista ---
while True:
    rate(100) # 100 iterações por segundo de tempo real
    
    if executando:
        # 1. Cálculo das Forças (Peso + Resistência do Ar)
        # Força de Arrasto: Fd = -k * v
        f_peso = m * g
        f_arrasto = -k * v
        f_total = f_peso + f_arrasto
        
        # 2. Aceleração (Segunda Lei de Newton)
        a = f_total / m
        
        # 3. Método de Euler-Cromer (Mais estável e realista)
        # Primeiro atualiza-se a velocidade, depois a posição
        v = v + a * dt
        esfera.pos = esfera.pos + v * dt + 1/2 * a * dt * dt
        t += dt
        
        # 4. Atualização dos Gráficos
        curva_pos.plot(t, esfera.pos.y)
        curva_vel.plot(t, mag(v))
        
        # 5. Condição de Paragem (Chão)
        if esfera.pos.y <= esfera.radius:
            esfera.pos.y = esfera.radius
            v = vector(0,0,0)
            executando = False
            btn_start.text = "Fim da Queda (Reiniciar)"
