# eufisica/Simulations — Simulações de Física em HTML e Python

Este documento é baseado na estrutura e repositório **eufisica/Simulations**, voltado para o desenvolvimento de interatividades e simulações computacionais aplicadas ao ensino e demonstração de fenômenos na área de Física utilizando **HTML/JavaScript** e **Python**.

---

## 1. Visão Geral

O objetivo principal de simulações interativas na física é permitir a visualização intuitiva de fenômenos que podem ser difíceis de abstrair apenas com teorias ou equações estáticas.

### Abordagens de Implementação:

* **HTML5 + JavaScript (Canvas / WebGL / p5.js):** 
  * Ideal para demonstrações acessíveis diretamente pelo navegador sem necessidade de instalação.
  * Altamente interativo, focado em animações em tempo real e interfaces amigáveis.
* **Python (Matplotlib, NumPy, SciPy, VPython, Pygame):**
  * Ideal para modelagem numérica precisa, solução de equações diferenciais e análise gráfica avançada.
  * Excelente para prototipagem de modelos teóricos complexos.

---

## 2. Exemplos de Aplicação por Domínio da Física

### A. Mecânica Clássica
* **Pêndulo Simples e Duplo:** Resolução de equações diferenciais do movimento e caos determinístico.
* **Lançamento de Projéteis:** Simulação com e sem resistência do ar.
* **Órbitas e Gravitação:** Órbitas de Kepler e o problema dos $n$-corpos.

### B. Eletromagnetismo
* **Campos Elétricos e Potencial:** Mapeamento de linhas de campo criadas por cargas pontuais.
* **Movimento de Cargas em Campos Magnéticos:** Trajetórias helicoidais sob a força de Lorentz ($\vec{F} = q\vec{v} \times \vec{B}$).

### C. Ondas e Óptica
* **Interferência e Difração:** Simulação de fenda dupla de Young e ondas na superfície de líquidos.
* **Refração e Lei de Snell:** Demonstrações da propagação da luz através de diferentes meios.

---

## 3. Estruturas Padrão dos Códigos

### Exemplo em Python (NumPy + Matplotlib)
Modelagem e visualização da trajetória de um projétil:

```python
import numpy as np
import matplotlib.pyplot as plt

# Parâmetros Iniciais
v0 = 20.0     # velocidade inicial (m/s)
theta = 45.0  # ângulo de lançamento (graus)
g = 9.81      # aceleração da gravidade (m/s^2)

# Conversão para radianos e componentes
rad = np.radians(theta)
vx0 = v0 * np.cos(rad)
vy0 = v0 * np.sin(rad)

# Tempo de voo
t_total = 2 * vy0 / g
t = np.linspace(0, t_total, 100)

# Equações do movimento
x = vx0 * t
y = vy0 * t - 0.5 * g * t**2

# Plot
plt.plot(x, y)
plt.title("Lançamento de Projétil")
plt.xlabel("Distância (m)")
plt.ylabel("Altura (m)")
plt.grid(True)
plt.show()
```

### Exemplo em HTML/JavaScript (Canvas)
Loop básico de animação para física no navegador:

```html
<!DOCTYPE html>
<html lang="pt">
<head>
  <meta charset="UTF-8">
  <title>Simulação de Movimento</title>
</head>
<body>
  <canvas id="simCanvas" width="600" height="400" style="border:1px solid black;"></canvas>
  <script>
    const canvas = document.getElementById("simCanvas");
    const ctx = canvas.getContext("2d");

    let x = 50, y = 200;
    let vx = 2, vy = 0;
    const g = 0.1; // Gravidade simplificada

    function update() {
      // Atualizar posição e velocidade
      vy += g;
      x += vx;
      y += vy;

      // Colisão com o chão
      if (y >= canvas.height - 15) {
        y = canvas.height - 15;
        vy = -vy * 0.8; // Perda de energia (quique)
      }

      // Renderizar
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.beginPath();
      ctx.arc(x, y, 15, 0, Math.PI * 2);
      ctx.fillStyle = "blue";
      ctx.fill();

      requestAnimationFrame(update);
    }

    update();
  </script>
</body>
</html>
```

---

## 4. Como Executar e Contribuir

1. **Simulações Python:** Instale as dependências padrão via `pip install numpy matplotlib scipy vpython`.
2. **Simulações HTML:** Abra qualquer arquivo `.html` diretamente em seu navegador web moderno ou utilize um servidor local para desenvolvimento.