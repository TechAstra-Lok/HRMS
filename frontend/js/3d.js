// 3D Visualization using Three.js
class ThreeVisualization {
    constructor() {
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.cubes = [];
        this.autoRotate = true;
        this.init();
    }

    init() {
        const container = document.getElementById('threeContainer');
        if (!container) return;

        // Setup scene
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x0F172A);

        // Setup camera
        const aspect = container.clientWidth / container.clientHeight;
        this.camera = new THREE.PerspectiveCamera(60, aspect, 0.1, 1000);
        this.camera.position.set(12, 8, 12);
        this.camera.lookAt(0, 0, 0);

        // Setup renderer
        this.renderer = new THREE.WebGLRenderer({ 
            antialias: true,
            alpha: true
        });
        this.renderer.setSize(container.clientWidth, container.clientHeight);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        container.appendChild(this.renderer.domElement);

        // Lights
        this.setupLights();

        // Grid
        this.setupGrid();

        // Data
        this.createVisualization();

        // Animation
        this.animate();

        // Resize handler
        window.addEventListener('resize', () => this.resize());
    }

    setupLights() {
        // Ambient light
        const ambient = new THREE.AmbientLight(0x404060, 0.5);
        this.scene.add(ambient);

        // Directional light
        const directional = new THREE.DirectionalLight(0xffffff, 1);
        directional.position.set(10, 20, 10);
        directional.castShadow = true;
        directional.shadow.mapSize.width = 1024;
        directional.shadow.mapSize.height = 1024;
        this.scene.add(directional);

        // Fill light
        const fill = new THREE.DirectionalLight(0x4F46E5, 0.3);
        fill.position.set(-10, 5, -10);
        this.scene.add(fill);

        // Point light
        const point = new THREE.PointLight(0x818CF8, 0.5, 50);
        point.position.set(0, 10, 0);
        this.scene.add(point);

        // Hemisphere light
        const hemi = new THREE.HemisphereLight(0x4F46E5, 0x818CF8, 0.6);
        this.scene.add(hemi);
    }

    setupGrid() {
        // Grid helper
        const grid = new THREE.GridHelper(20, 20, 0x334155, 0x1E293B);
        grid.position.y = -0.5;
        this.scene.add(grid);

        // Ground plane
        const geometry = new THREE.PlaneGeometry(20, 20);
        const material = new THREE.MeshStandardMaterial({
            color: 0x0F172A,
            transparent: true,
            opacity: 0.5,
            roughness: 0.8,
            metalness: 0.2
        });
        const ground = new THREE.Mesh(geometry, material);
        ground.rotation.x = -Math.PI / 2;
        ground.position.y = -0.5;
        ground.receiveShadow = true;
        this.scene.add(ground);
    }

    createVisualization() {
        // Create cubes representing departments
        const departments = [
            { name: 'Engineering', count: 45, color: 0x4F46E5 },
            { name: 'Sales', count: 30, color: 0x22C55E },
            { name: 'Marketing', count: 25, color: 0xF59E0B },
            { name: 'HR', count: 20, color: 0xEC4899 },
            { name: 'Finance', count: 15, color: 0x8B5CF6 },
            { name: 'Operations', count: 35, color: 0x14B8A6 }
        ];

        const spacing = 2.5;
        const startX = -(departments.length - 1) * spacing / 2;

        departments.forEach((dept, index) => {
            const x = startX + index * spacing;
            const height = (dept.count / 50) * 3 + 0.5;
            
            // Main cube
            const geometry = new THREE.BoxGeometry(1.8, height, 1.8);
            const material = new THREE.MeshStandardMaterial({
                color: dept.color,
                roughness: 0.3,
                metalness: 0.1,
                transparent: true,
                opacity: 0.9
            });
            const cube = new THREE.Mesh(geometry, material);
            cube.position.set(x, height / 2 - 0.5, 0);
            cube.castShadow = true;
            cube.userData = dept;
            this.scene.add(cube);
            this.cubes.push(cube);

            // Glow outline
            const glowGeo = new THREE.BoxGeometry(2, height + 0.2, 2);
            const glowMat = new THREE.MeshBasicMaterial({
                color: dept.color,
                transparent: true,
                opacity: 0.1,
                wireframe: true
            });
            const glow = new THREE.Mesh(glowGeo, glowMat);
            glow.position.copy(cube.position);
            this.scene.add(glow);

            // Label (using sprite)
            this.createLabel(dept.name, x, height - 0.3);
            this.createLabel(dept.count + ' emp', x, -0.2);
        });
    }

    createLabel(text, x, y) {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = 256;
        canvas.height = 64;

        // Background
        ctx.fillStyle = 'rgba(15, 23, 42, 0.8)';
        ctx.roundRect(0, 0, canvas.width, canvas.height, 8);
        ctx.fill();

        // Text
        ctx.fillStyle = '#F1F5F9';
        ctx.font = 'bold 24px Inter, sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(text, canvas.width / 2, canvas.height / 2);

        const texture = new THREE.CanvasTexture(canvas);
        const material = new THREE.SpriteMaterial({ 
            map: texture,
            transparent: true,
            depthTest: false
        });
        const sprite = new THREE.Sprite(material);
        sprite.position.set(x, y + 0.5, 0);
        sprite.scale.set(3, 0.75, 1);
        this.scene.add(sprite);
    }

    animate() {
        requestAnimationFrame(() => this.animate());

        if (this.autoRotate) {
            const time = Date.now() * 0.0003;
            this.camera.position.x = 12 * Math.cos(time);
            this.camera.position.z = 12 * Math.sin(time);
            this.camera.lookAt(0, 0, 0);
        }

        // Float animation for cubes
        this.cubes.forEach((cube, i) => {
            const offset = i * 0.5;
            const floatY = Math.sin(Date.now() * 0.001 + offset) * 0.1;
            cube.position.y += floatY * 0.01;
        });

        this.renderer.render(this.scene, this.camera);
    }

    resize() {
        const container = document.getElementById('threeContainer');
        if (!container) return;

        const width = container.clientWidth;
        const height = container.clientHeight;

        this.camera.aspect = width / height;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(width, height);
    }
}

// Global functions
let threeViz = null;

document.addEventListener('DOMContentLoaded', () => {
    threeViz = new ThreeVisualization();
});

window.toggle3DView = function() {
    if (threeViz) {
        threeViz.autoRotate = !threeViz.autoRotate;
        showToast(threeViz.autoRotate ? 'Auto-rotate enabled' : 'Auto-rotate disabled', 'info');
    }
};

window.reset3DView = function() {
    if (threeViz) {
        threeViz.camera.position.set(12, 8, 12);
        threeViz.camera.lookAt(0, 0, 0);
        showToast('View reset', 'info');
    }
};

// RoundRect polyfill for canvas
if (!CanvasRenderingContext2D.prototype.roundRect) {
    CanvasRenderingContext2D.prototype.roundRect = function(x, y, w, h, r) {
        if (r > w/2) r = w/2;
        if (r > h/2) r = h/2;
        this.moveTo(x + r, y);
        this.lineTo(x + w - r, y);
        this.quadraticCurveTo(x + w, y, x + w, y + r);
        this.lineTo(x + w, y + h - r);
        this.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
        this.lineTo(x + r, y + h);
        this.quadraticCurveTo(x, y + h, x, y + h - r);
        this.lineTo(x, y + r);
        this.quadraticCurveTo(x, y, x + r, y);
        return this;
    };
}