<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sphere Collision Simulation - José Gonçalves (eufisica)</title>
    <style>
        body {
            margin: 0;
            background-color: #1a1a1a;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            font-family: sans-serif;
            color: white;
            overflow: hidden;
        }
        canvas {
            border: 2px solid #333;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            background-color: black;
        }
        .instructions {
            margin-top: 15px;
            font-size: 16px;
            letter-spacing: 1px;
            color: #aaa;
        }
    </style>
</head>
<body>

    <canvas id="simCanvas" width="800" height="600"></canvas>
    <div class="instructions">Pressione ESPAÇO para reiniciar</div>

    <script>
        const canvas = document.getElementById("simCanvas");
        const ctx = canvas.getContext("2d");

        // Constants
        const WIDTH = 800;
        const HEIGHT = 600;
        const GRAVITY = 0.5;
        const DAMPING = 0.98; // Coeficiente de restituição

        class Sphere {
            constructor(x, y, radius, color, vx = 0, vy = 0) {
                this.x = x;
                this.y = y;
                this.radius = radius;
                this.color = color;
                this.vx = vx;
                this.vy = vy;
                this.mass = radius ** 2; // Massa proporcional à área
            }

            update() {
                // Apply gravity
                this.vy += GRAVITY;

                // Update position
                this.x += this.vx;
                this.y += this.vy;

                // Wall collisions (Esquerda / Direita)
                if (this.x - this.radius < 0) {
                    this.x = this.radius;
                    this.vx = -this.vx * DAMPING;
                } else if (this.x + this.radius > WIDTH) {
                    this.x = WIDTH - this.radius;
                    this.vx = -this.vx * DAMPING;
                }

                // Wall collisions (Topo / Fundo)
                if (this.y - this.radius < 0) {
                    this.y = this.radius;
                    this.vy = -this.vy * DAMPING;
                } else if (this.y + this.radius > HEIGHT) {
                    this.y = HEIGHT - this.radius;
                    this.vy = -this.vy * DAMPING;
                }
            }

            draw(context) {
                // Esfera principal
                context.beginPath();
                context.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
                context.fillStyle = this.color;
                context.fill();
                context.closePath();

                // Brilho para o efeito 3D (Highlight)
                context.beginPath();
                const highlightX = this.x - this.radius / 3;
                const highlightY = this.y - this.radius / 3;
                const highlightRadius = this.radius / 4;
                context.arc(highlightX, highlightY, highlightRadius, 0, Math.PI * 2);
                context.fillStyle = "rgba(255, 255, 255, 0.6)";
                context.fill();
                context.closePath();
            }
        }

        function checkCollision(sphere1, sphere2) {
            let dx = sphere2.x - sphere1.x;
            let dy = sphere2.y - sphere1.y;
            let distance = Math.sqrt(dx ** 2 + dy ** 2);

            if (distance < sphere1.radius + sphere2.radius) {
                // Normalize collision vector
                let nx = dx / distance;
                let ny = dy / distance;

                // Separate spheres to prevent sticking
                let overlap = sphere1.radius + sphere2.radius - distance;
                sphere1.x -= (nx * overlap) / 2;
                sphere1.y -= (ny * overlap) / 2;
                sphere2.x += (nx * overlap) / 2;
                sphere2.y += (ny * overlap) / 2;

                // Relative velocity
                let dvx = sphere1.vx - sphere2.vx;
                let dvy = sphere1.vy - sphere2.vy;

                // Relative velocity in normal direction
                let dvn = dvx * nx + dvy * ny;

                // If they are moving apart, do nothing
                if (dvn <= 0) return;

                // Collision impulse formula
                let impulse = ((1 + DAMPING) * dvn) / (sphere1.mass + sphere2.mass);

                // Update velocities
                sphere1.vx -= impulse * sphere2.mass * nx;
                sphere1.vy -= impulse * sphere2.mass * ny;
                sphere2.vx += impulse * sphere1.mass * nx;
                sphere2.vy += impulse * sphere1.mass * ny;
            }
        }

        // Declarar as variáveis das esferas
        let sphere1, sphere2;

        // Função para inicializar/reiniciar o estado
        function resetSimulation() {
            sphere1 = new Sphere(200, 200, 40, "rgb(255, 100, 100)", 5, 2);
            sphere2 = new Sphere(600, 300, 50, "rgb(100, 100, 255)", -3, -1);
        }

        // Escutar tecla Espaço para reiniciar
        window.addEventListener("keydown", (event) => {
            if (event.code === "Space") {
                resetSimulation();
            }
        });

        // Loop principal da animação (Equivalente ao while do Pygame)
        function animate() {
            // Limpar o ecrã com a cor preta
            ctx.fillStyle = "black";
            ctx.fillRect(0, 0, WIDTH, HEIGHT);

            // Atualizar física
            sphere1.update();
            sphere2.update();

            // Verificar colisões
            checkCollision(sphere1, sphere2);

            // Desenhar elementos
            sphere1.draw(ctx);
            sphere2.draw(ctx);

            // Solicitar o próximo frame (Garante os 60 FPS fluidos nativos do browser)
            requestAnimationFrame(animate);
        }

        // Iniciar simulação pela primeira vez
        resetSimulation();
        animate();
    </script>
</body>
</html>
