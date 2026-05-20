from vpython import *

# 1. Configuração da Janela 3D
scene = canvas(title="Campo Elétrico 3D com VPython", width=800, height=600, center=vector(0,0,0))
scene.background = color.gray(0.1)

# Parâmetros físicos
q1_val = 1e-9   # Carga positiva (Cálculo em escala proporcional)
q2_val = -1e-9  # Carga negativa
k = 8.99e9      # Constante de Coulomb

# 2. Criar os Objetos (Cargas)
# Inicialmente separadas por uma distância total de 4 unidades
dist_inicial = 4.0
carga_p = sphere(pos=vector(dist_inicial/2, 0, 0), radius=0.3, color=color.red)
carga_n = sphere(pos=vector(-dist_inicial/2, 0, 0), radius=0.3, color=color.blue)

# Lista para guardar as linhas de campo e podermos apagá-las ao atualizar
linhas_campo = []

# 3. Função para Calcular o Campo Elétrico num ponto do espaço
def calcular_E(ponto):
    r_p = ponto - carga_p.pos
    r_n = ponto - carga_n.pos
    
    # Evitar divisão por zero se estivermos colados à carga
    if r_p.mag < 0.1 or r_n.mag < 0.1:
        return vector(0,0,0)
        
    E_p = (k * q1_val / (r_p.mag**2)) * r_p.hat
    E_n = (k * q2_val / (r_n.mag**2)) * r_n.hat
    return E_p + E_n

# 4. Função Principal para Desenhar as Linhas de Campo
def desenhar_linhas():
    global list_linhas
    # Limpar as linhas anteriores
    for linha in linhas_campo:
        linha.visible = False
        del linha
    linhas_campo.clear()
    
    # Gerar pontos de partida ao redor da carga positiva (Esfera de pontos)
    # Vamos criar linhas distribuídas uniformemente em ângulos esféricos
    N_phi = 6
    N_theta = 6
    ds = 0.1 # Tamanho do passo de cada segmento da linha
    
    for i in range(1, N_phi):
        phi = pi * i / N_phi
        for j in range(N_theta):
            theta = 2 * pi * j / N_theta
            
            # Ponto de partida ligeiramente afastado da superfície da carga positiva
            x = carga_p.pos.x + 0.35 * sin(phi) * cos(theta)
            y = carga_p.pos.y + 0.35 * sin(phi) * sin(theta)
            z = carga_p.pos.z + 0.35 * cos(phi)
            
            ponto_atual = vector(x, y, z)
            
            # Criar um objeto 'curve' do VPython para esta linha de campo
            linha = curve(color=color.green, radius=0.02)
            linha.append(ponto_atual)
            linhas_campo.append(linha)
            
            # Traçar a linha passo a passo (parar se afastar muito ou se chegar à carga negativa)
            contador = 0
            while contador < 300:
                E = calcular_E(ponto_atual)
                if E.mag == 0: 
                    break
                    
                # Avançar na direção do campo elétrico
                ponto_atual += E.hat * ds
                linha.append(ponto_atual)
                
                # Se estiver muito perto da carga negativa, a linha termina
                if (ponto_atual - carga_n.pos).mag < 0.32:
                    break
                # Se fugir do ecrã, para
                if ponto_atual.mag > 15:
                    break
                    
                contador += 1

# 5. Função de Callback para o Slider
def atualizar_distancia(slider_objeto):
    nova_dist = slider_objeto.value
    # Atualizar as posições das cargas simetricamente ao centro (0,0,0)
    carga_p.pos = vector(nova_dist / 2, 0, 0)
    carga_n.pos = vector(-nova_dist / 2, 0, 0)
    
    # Redesenhar as linhas para a nova geometria
    desenhar_linhas()

# 6. Criar o Slider na interface do VPython
scene.append_to_caption("\n\n")
slider_dist = slider(bind=atualizar_distancia, min=1.5, max=8.0, value=dist_inicial, length=400)
scene.append_to_caption("  <- Arrasta para alterar a distância entre as cargas\n\n")

# Desenhar as linhas pela primeira vez
desenhar_linhas()

# Loop estável para manter a janela ativa
while True:
    rate(60)