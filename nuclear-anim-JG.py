import pygame
import random
import math
import sys

def iniciar_simulacao():
    try:
        pygame.init()
        # Definir dimensões e permitir redimensionamento
        largura_janela, altura_janela = 1100, 750
        ecra = pygame.display.set_mode((largura_janela, altura_janela), pygame.RESIZABLE)
        pygame.display.set_caption("Simulador Nuclear: Reação em Cadeia Colorida (José Gonçalves)")
        
        relogio = pygame.time.Clock()
        
        # --- Configurações de Cores ---
        COR_FUNDO = (10, 10, 15)
        COR_URANIO = (255, 215, 0)
        COR_NEUTRON = (50, 255, 50)
        COR_PAINEL = (30, 35, 45)
        COR_TEXTO = (236, 240, 241)

        INFO_PRODUTOS = {
            "Ba-141": (231, 76, 60), "Kr-92": (52, 152, 219),
            "Xe-140": (155, 89, 182), "Sr-94": (26, 188, 156),
            "Cs-137": (243, 156, 18), "Rb-96": (200, 200, 200)
        }

        fonte_geral = pygame.font.SysFont("Arial", 18, bold=True)
        fonte_pequena = pygame.font.SysFont("Arial", 11, bold=True)

        # --- Classes ---
        class Neutron:
            def __init__(self, x, y, angulo):
                self.x, self.y = x, y
                self.vel = 4.0
                self.vx = math.cos(angulo) * self.vel
                self.vy = math.sin(angulo) * self.vel
                self.ativo = True
            def mover(self, l, a):
                self.x += self.vx
                self.y += self.vy
                if not (0 < self.x < l and 0 < self.y < a - 130): self.ativo = False

        class Nucleo:
            def __init__(self, l, a):
                self.x = random.randint(30, l - 30)
                self.y = random.randint(30, a - 160)
                self.fissionado = False
                self.raio = 14
                self.nome = "U-235"
                self.cor = COR_URANIO
            def fissionar(self):
                self.fissionado = True
                self.nome = random.choice(list(INFO_PRODUTOS.keys()))
                self.cor = INFO_PRODUTOS[self.nome]

        # --- Variáveis do Simulador ---
        num_nucleos = 60
        nucleos = [Nucleo(largura_janela, altura_janela) for _ in range(num_nucleos)]
        neutroes = []
        em_pausa = True
        energia = 0
        
        # Barra Deslizante (Slider)
        slider_rect = pygame.Rect(150, altura_janela - 70, 250, 10)
        slider_pegador = pygame.Rect(150, altura_janela - 82, 15, 25)
        arrastando = False

        # --- Loop Principal ---
        rodando = True
        while rodando:
            l_atual, a_atual = ecra.get_size()
            ecra.fill(COR_FUNDO)
            rato = pygame.mouse.get_pos()

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    rodando = False
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    # Lógica dos botões
                    btn_play = pygame.Rect(l_atual // 2 - 120, a_atual - 85, 100, 40)
                    btn_reset = pygame.Rect(l_atual // 2 + 10, a_atual - 85, 120, 40)
                    
                    if btn_play.collidepoint(rato):
                        em_pausa = not em_pausa
                    elif btn_reset.collidepoint(rato):
                        nucleos = [Nucleo(l_atual, a_atual) for _ in range(num_nucleos)]
                        neutroes, energia, em_pausa = [], 0, True
                    elif slider_pegador.collidepoint(rato):
                        arrastando = True
                    elif rato[1] < a_atual - 130:
                        neutroes.append(Neutron(rato[0], rato[1], random.uniform(0, 2*math.pi)))
                
                if ev.type == pygame.MOUSEBUTTONUP:
                    arrastando = False

                if ev.type == pygame.MOUSEMOTION and arrastando:
                    nx = max(slider_rect.x, min(rato[0], slider_rect.x + slider_rect.width))
                    perc = (nx - slider_rect.x) / slider_rect.width
                    num_nucleos = int(10 + perc * 490)
                    # Atualizar posição visual do pegador
                    slider_pegador.centerx = nx

            # Atualizar Física
            if not em_pausa:
                for n in neutroes[:]:
                    n.mover(l_atual, a_atual)
                    if not n.ativo: 
                        neutroes.remove(n)
                        continue
                    for u in nucleos:
                        if not u.fissionado and math.hypot(n.x - u.x, n.y - u.y) < u.raio + 4:
                            u.fissionar()
                            n.ativo = False
                            energia += 200
                            for _ in range(random.randint(2, 3)):
                                neutroes.append(Neutron(u.x, u.y, random.uniform(0, 2*math.pi)))
                            break

            # --- Desenho ---
            for u in nucleos:
                pygame.draw.circle(ecra, u.cor, (int(u.x), int(u.y)), u.raio if not u.fissionado else 10)
                txt = fonte_pequena.render(u.nome, True, (0,0,0) if not u.fissionado else COR_TEXTO)
                ecra.blit(txt, (u.x - 15, u.y - 6))

            for n in neutroes:
                pygame.draw.circle(ecra, COR_NEUTRON, (int(n.x), int(n.y)), 4)

            # Painel UI
            pygame.draw.rect(ecra, COR_PAINEL, (0, a_atual - 130, l_atual, 130))
            
            # Desenhar Slider
            slider_rect.y = a_atual - 70
            slider_pegador.centery = slider_rect.centery
            pygame.draw.rect(ecra, (100, 100, 100), slider_rect, border_radius=5)
            pygame.draw.rect(ecra, COR_TEXTO, slider_pegador, border_radius=3)
            ecra.blit(fonte_geral.render(f"Urânio: {num_nucleos}", True, COR_TEXTO), (slider_rect.x, a_atual - 105))

            # Botões
            btn_play = pygame.Rect(l_atual // 2 - 120, a_atual - 85, 100, 40)
            btn_reset = pygame.Rect(l_atual // 2 + 10, a_atual - 85, 120, 40)
            pygame.draw.rect(ecra, (46, 204, 113) if em_pausa else (230, 126, 34), btn_play, border_radius=8)
            pygame.draw.rect(ecra, (192, 57, 43), btn_reset, border_radius=8)
            ecra.blit(fonte_geral.render("PLAY" if em_pausa else "PAUSA", True, COR_TEXTO), (btn_play.x + 22, btn_play.y + 8))
            ecra.blit(fonte_geral.render("REINICIAR", True, COR_TEXTO), (btn_reset.x + 15, btn_reset.y + 8))
            
            # Estatísticas
            ecra.blit(fonte_geral.render(f"Energia: {energia} MeV", True, (46, 204, 113)), (l_atual - 250, a_atual - 80))

            pygame.display.flip()
            relogio.tick(60)

    except Exception as e:
        print(f"Ocorreu um erro crítico: {e}")
        input("Pressiona Enter para fechar...")
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    iniciar_simulacao()