import os

html_cargas_iguais = """<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simulação 3D - Cargas Iguais (Repulsão)</title>
    <style>
        body { margin: 0; padding: 0; overflow: hidden; background-color: #ffffff; font-family: sans-serif; }
        #canvas-container { width: 100vw; height: 100vh; position: absolute; z-index: 1; }
        #controls-panel {
            position: absolute; top: 20px; left: 20px; z-index: 10;
            background: rgba(255, 255, 255, 0.95); padding: 15px 25px;
            border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            border: 1px solid #e0e0e0; width: 320px;
        }
        h2 { margin: 0 0 10px 0; font-size: 16px; color: #222; }
        label { display: block; font-size: 13px; font-weight: bold; margin-bottom: 5px; color: #555; }
        input[type=range] { width: 100%; }
        .value-display { font-weight: normal; color: #dc3545; float: right; }
        .legend { margin-top: 12px; font-size: 11px; color: #666; border-top: 1px solid #eee; padding-top: 8px; }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
</head>
<body>

    <div id="controls-panel">
        <h2>Linhas de Campo - Cargas Iguais</h2>
        <div class="slider-container">
            <label for="distanceSlider">Distância: <span id="distValue" class="value-display">4.0</span></label>
            <input type="range" id="distanceSlider" min="1.5" max="8.0" step="0.1" value="4.0">
        </div>
        <div class="legend">
            <span style="color: #dc3545; font-weight: bold;">● Vermelho:</span> Cargas Positivas (+)<br>
            <span style="font-size: 10px; display:block; margin-top:5px;">Repara como as linhas divergem e evitam o centro exato da simulação.</span>
        </div>
    </div>

    <div id="canvas-container"></div>

    <script>
        const container = document.getElementById('canvas-container');
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0xffffff);

        const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(0, 5, 8);

        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        container.appendChild(renderer.domElement);

        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;

        scene.add(new THREE.AmbientLight(0xffffff, 0.7));
        const dirLight = new THREE.DirectionalLight(0xffffff, 0.5);
        dirLight.position.set(5, 10, 7);
        scene.add(dirLight);

        // Duas esferas vermelhas (ambas positivas)
        const sphereGeo = new THREE.SphereGeometry(0.25, 32, 32);
        const matPos = new THREE.MeshPhongMaterial({ color: 0xff3333 });

        const carga1 = new THREE.Mesh(sphereGeo, matPos);
        const carga2 = new THREE.Mesh(sphereGeo, matPos);
        scene.add(carga1);
        scene.add(carga2);

        let grupoLinhas = new THREE.Group();
        scene.add(grupoLinhas);

        scene.add(new THREE.GridHelper(20, 20, 0xcccccc, 0xf0f0f0));

        // Cálculo do Campo Elétrico para duas cargas POSITIVAS
        function calcularE(ponto, p1, p2) {
            let r1 = new THREE.Vector3().subVectors(ponto, p1);
            let r2 = new THREE.Vector3().subVectors(ponto, p2);
            
            let d1Sq = r1.lengthSq();
            let d2Sq = r2.lengthSq();
            
            if (d1Sq < 0.02 || d2Sq < 0.02) return new THREE.Vector3(0,0,0);
            
            // Ambas as cargas repelem (afastam do centro da carga)
            let E1 = r1.normalize().divideScalar(d1Sq);
            let E2 = r2.normalize().divideScalar(d2Sq);
            
            return new THREE.Vector3().addVectors(E1, E2);
        }

        function desenharLinhas(distancia) {
            while(grupoLinhas.children.length > 0){ 
                grupoLinhas.remove(grupoLinhas.children[0]); 
            }

            const posX = distancia / 2;
            carga1.position.set(posX, 0, 0);
            carga2.position.set(-posX, 0, 0);

            const p1 = carga1.position;
            const p2 = carga2.position;

            const numPhi = 8;
            const numTheta = 8;
            const passo = 0.08;
            const materialLinha = new THREE.LineBasicMaterial({ color: 0x44aa44 });

            // Função interna para traçar a partir de uma posição de carga
            function tracarOrigem(origem) {
                for (let i = 1; i < numPhi; i++) {
                    let phi = Math.PI * i / numPhi;
                    for (let j = 0; j < numTheta; j++) {
                        let theta = 2 * Math.PI * j / numTheta;

                        let ponto = new THREE.Vector3(
                            origem.x + 0.28 * Math.sin(phi) * Math.cos(theta),
                            origem.y + 0.28 * Math.sin(phi) * Math.sin(theta),
                            origem.z + 0.28 * Math.cos(phi)
                        );

                        let pontosDaLinha = [ponto.clone()];

                        for (let k = 0; k < 200; k++) {
                            let E = calcularE(ponto, p1, p2);
                            if (E.lengthSq() < 1e-6) break; // Para se o campo for nulo (região central)

                            E.normalize().multiplyScalar(passo);
                            ponto.add(E);
                            pontosDaLinha.push(ponto.clone());

                            if (ponto.length() > 15) break; // Para se afastar demais
                        }

                        if (pontosDaLinha.length > 1) {
                            const geo = new THREE.BufferGeometry().setFromPoints(pontosDaLinha);
                            grupoLinhas.add(new THREE.Line(geo, materialLinha));
                        }
                    }
                }
            }

            // Traça as linhas a partir de ambas as cargas para o exterior
            tracarOrigem(p1);
            tracarOrigem(p2);
        }

        const slider = document.getElementById('distanceSlider');
        const display = document.getElementById('distValue');

        slider.addEventListener('input', (e) => {
            const val = parseFloat(e.target.value);
            display.innerText = val.toFixed(1);
            desenharLinhas(val);
        });

        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });

        desenharLinhas(parseFloat(slider.value));

        function animate() {
            requestAnimationFrame(animate);
            controls.update();
            renderer.render(scene, camera);
        }
        animate();
    </script>
</body>
</html>
"""

nome_ficheiro = "campo_cargas_iguais.html"
with open(nome_ficheiro, "w", encoding="utf-8") as f:
    f.write(html_cargas_iguais)

print(f"Sucesso! Ficheiro criado em: '{os.path.abspath(nome_ficheiro)}'")