"use strict";

var container, controls;
var camera, scene, raycaster, renderer;
var lightwood, darkwood, reddarkwood, wood;
var poles, board, turn;

var mouse;
var INTERSECTED;

init();
animate();

function init() {

	container = document.createElement('div');
	document.body.appendChild(container);

	camera = new THREE.PerspectiveCamera(70, window.innerWidth / window.innerHeight, 1, 10000);
	camera.position.z = 1000;

	controls = new THREE.TrackballControls(camera);
	controls.rotateSpeed = 1.0;
	controls.zoomSpeed = 1.2;
	controls.panSpeed = 0.8;
	controls.noZoom = false;
	controls.noPan = false;
	controls.staticMoving = true;
	controls.dynamicDampingFactor = 0.3;

	mouse = new THREE.Vector2();

	scene = new THREE.Scene();
	scene.background = new THREE.Color(0xf0f0f0);

	var light = new THREE.DirectionalLight(0xffffff, 1);
	light.position.set(1, 1, 1).normalize();
	scene.add(light);

	lightwood = new THREE.TextureLoader().load('textures/lightwood1024.jpg');
	darkwood = new THREE.TextureLoader().load('textures/darkwood1024.jpg');
	reddarkwood = new THREE.TextureLoader().load('textures/reddarkwood1024.jpg');
	wood = new THREE.TextureLoader().load('textures/wood1024.jpg');

	board = [];
	poles = [];
	turn = 1;


	for (var i = 0; i <= 3; i++) {
		board[i] = [];
		for (var j = 0; j <= 3; j++) {
			board[i][j] = 0;
			var material = new THREE.MeshBasicMaterial({
				map: darkwood
			});
			var pole = new THREE.Mesh(new THREE.CylinderGeometry(10, 10, 300, 64, 5), material);
			pole.position.set(-150 + 100 * i, -150 + 100 * j, 0);
			pole.rotation.x = Math.PI / 2
			pole.name = `Pole ${i}:${j}`
			pole.is_pole = true;
			pole.numx = i;
			pole.numy = j;
			scene.add(pole);
			poles.push(pole);
		}
	}

	// Board

	var material = new THREE.MeshBasicMaterial({
		map: wood
	});
	var board = new THREE.Mesh(new THREE.BoxGeometry(350, 350, 10), material);
	board.position.set(0, 0, -155);
	scene.add(board);


	raycaster = new THREE.Raycaster();

	renderer = new THREE.WebGLRenderer({
		antialias: true
	});
	renderer.setPixelRatio(window.devicePixelRatio);
	renderer.setSize(window.innerWidth, window.innerHeight);
	container.appendChild(renderer.domElement);

	document.addEventListener('mousemove', onDocumentMouseMove, false);

	document.addEventListener('click', onDocumentMouseClick, false);

	window.addEventListener('resize', onWindowResize, false);

}

function onWindowResize() {

	camera.aspect = window.innerWidth / window.innerHeight;
	camera.updateProjectionMatrix();

	renderer.setSize(window.innerWidth, window.innerHeight);

}

function onDocumentMouseMove(event) {

	event.preventDefault();

	mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
	mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

}

function onDocumentMouseClick(event) {

	event.preventDefault();

	if (INTERSECTED && INTERSECTED.is_pole) {
		var i = INTERSECTED.numx;
		var j = INTERSECTED.numy;
		if (board[i][j] < 4) {
			createBall(i, j, board[i][j]++)
			turn = 1 - turn;
		}

	}
}


function createBall(i, j, n) {
	var texture;
	if (turn == 1) {
		texture = darkwood;
	} else {
		texture = lightwood;
	}
	var material = new THREE.MeshBasicMaterial({
		map: texture
	});
	var object = new THREE.Mesh(new THREE.SphereGeometry(35, 32, 32), material);
	object.position.set(-150 + 100 * i, -150 + 100 * j, -150 + 34 + 68 * n);
	scene.add(object);
}

//

function animate() {

	requestAnimationFrame(animate);

	render();

}

function pick() {
	raycaster.setFromCamera(mouse, camera);

	var intersects = raycaster.intersectObjects(poles);

	if (intersects.length > 0) {

		if (INTERSECTED != intersects[0].object) {

			if (INTERSECTED) INTERSECTED.material.map = darkwood;

			INTERSECTED = intersects[0].object;
			INTERSECTED.material.map = reddarkwood;

		}

	} else {

		if (INTERSECTED) INTERSECTED.material.map = darkwood;

		INTERSECTED = null;

	}

}

function render() {

	controls.update();

	pick();

	renderer.render(scene, camera);
}
