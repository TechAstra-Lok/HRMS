/**
 * 3D Visualization Module
 */

let threeScene = null;

function load3DVisualization(data) {
    const container = document.getElementById('threeContainer');
    if (!container) return;
    
    // Clear previous content
    container.innerHTML = '';
    
    // Scene setup
    threeScene = new THREE.Scene();
    threeScene.background = new THREE.Color(0xffffff);
    
    const camera = new THREE.PerspectiveCamera(
        75,
        container.clientWidth / container.clientHeight,
        0.1,
        1000
    );
    
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    container.appendChild(renderer.domElement);
    
    camera.position.set(0, 50, 100);
    camera.lookAt(0, 0, 0);
    
    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    threeScene.add(ambientLight);
    
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(50, 100, 50);
    directionalLight.castShadow = true;
    threeScene.add(directionalLight);
    
    const pointLight = new THREE.PointLight(0xffffff, 0.4);
    pointLight.position.set(-50, 50, -50);
    threeScene.add(pointLight);
    
    // Create attendance cubes
    const attendanceData = data?.attendance || [];
    const cubes = [];
    
    attendanceData.slice(0, 16).forEach((record, index) => {
        const height = Math.max(5, (record.percentage / 100) * 60);
        const geometry = new THREE.BoxGeometry(12, height, 12);
        
        // Color based on status
        let color = 0x27AE60; // Present (Green)
        if (record.status === 'absent') color = 0xE74C3C;
        else if (record.status === 'late') color = 0xF39C12;
        else if (record.status === 'leave') color = 0x3498DB;
        
        const material = new THREE.MeshStandardMaterial({
            color,
            metalness: 0.3,
            roughness: 0.4
        });
        
        const cube = new THREE.Mesh(geometry, material);
        cube.castShadow = true;
        cube.receiveShadow = true;
        
        const x = (index % 4) * 35 - 52.5;
        const z = Math.floor(index / 4) * 35 - 52.5;
        
        cube.position.set(x, height / 2, z);
        
        // Add label
        const canvas = document.createElement('canvas');
        canvas.width = 64;
        canvas.height = 64;
        const ctx = canvas.getContext('2d');
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(0, 0, 64, 64);
        ctx.fillStyle = '#000000';
        ctx.font = '10px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(record.percentage + '%', 32, 32);
        
        const texture = new THREE.CanvasTexture(canvas);
        
        threeScene.add(cube);
        cubes.push({
            mesh: cube,
            baseHeight: height,
            amplitude: height * 0.2,
            frequency: 0.05,
            index
        });
    });
    
    // Create organizational chart (optional)
    createOrgChart(data?.org_chart);
    
    // Animation loop
    let time = 0;
    const animate = () => {
        requestAnimationFrame(animate);
        
        time += 0.01;
        
        cubes.forEach((cubeObj) => {
            const wave = Math.sin(time * cubeObj.frequency + cubeObj.index * 0.5);
            cubeObj.mesh.rotation.x += 0.002;
            cubeObj.mesh.rotation.y += 0.003;
            cubeObj.mesh.position.y = cubeObj.baseHeight / 2 + wave * cubeObj.amplitude;
        });
        
        renderer.render(threeScene, camera);
    };
    
    animate();
    
    // Handle resize
    const handleResize = () => {
        const width = container.clientWidth;
        const height = container.clientHeight;
        
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
        renderer.setSize(width, height);
    };
    
    window.addEventListener('resize', handleResize);
    
    // Mouse controls for rotation
    let isDragging = false;
    let previousMousePosition = { x: 0, y: 0 };
    
    renderer.domElement.addEventListener('mousedown', (e) => {
        isDragging = true;
        previousMousePosition = { x: e.clientX, y: e.clientY };
    });
    
    renderer.domElement.addEventListener('mousemove', (e) => {
        if (!isDragging) return;
        
        const deltaX = e.clientX - previousMousePosition.x;
        const deltaY = e.clientY - previousMousePosition.y;
        
        threeScene.rotation.y += deltaX * 0.01;
        threeScene.rotation.x += deltaY * 0.01;
        
        previousMousePosition = { x: e.clientX, y: e.clientY };
    });
    
    renderer.domElement.addEventListener('mouseup', () => {
        isDragging = false;
    });
}

function createOrgChart(orgData) {
    if (!orgData || !threeScene) return;
    
    // Create nodes
    orgData.forEach((person, index) => {
        const geometry = new THREE.SphereGeometry(5, 32, 32);
        const material = new THREE.MeshStandardMaterial({
            color: 0x4A90D9,
            metalness: 0.5,
            roughness: 0.3
        });
        
        const sphere = new THREE.Mesh(geometry, material);
        sphere.castShadow = true;
        sphere.receiveShadow = true;
        
        const x = (index % 3) * 40 - 40;
        const y = Math.floor(index / 3) * 40 + 80;
        
        sphere.position.set(x, y, 0);
        threeScene.add(sphere);
    });
}
