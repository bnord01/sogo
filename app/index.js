"use strict";

import lightwoodtexture from './textures/lightwood1024.jpg';
import darkwoodtexture from './textures/darkwood1024.jpg';
import woodtexture from './textures/wood1024.jpg';
import reddarkwoodtexture from './textures/reddarkwood1024.jpg';

import './lib/OrbitControls.js';

var THREE = require('three')
var io = require('socket.io-client')


var socket = io.connect(location.origin)
socket.on('move', move => {
	var i = move.i,
		j = move.j;
	var n = board[i][j];
	board[i][j] = n + 1;
	turn = 1 - turn;
	createBall(i, j, n);
})

socket.on('reset', resetBoard)


var container, controls;
var camera, scene, raycaster, renderer;
var lightwood, darkwood, reddarkwood, wood;
var poles, board, turn, balls;

var mouse, mouse_moved, mouse_valid;
var is_touch;

var INTERSECTED, last_intersected;

init();
animate();

function init() {

	container = document.createElement('div');
	document.body.appendChild(container);

	camera = new THREE.PerspectiveCamera(70, window.innerWidth / window.innerHeight, 1, 10000);
	camera.position.z = 1000;

	renderer = new THREE.WebGLRenderer({
		antialias: true
	});
	renderer.setPixelRatio(window.devicePixelRatio);
	renderer.setSize(window.innerWidth, window.innerHeight);
	container.appendChild(renderer.domElement);


	controls = new THREE.OrbitControls(camera, renderer.domElement);
	controls.enableDamping = true;
	controls.dampingFactor = 0.25;
	controls.panningMode = THREE.HorizontalPanning; // default is THREE.ScreenSpacePanning
	controls.minDistance = 100;
	controls.maxDistance = 800
	controls.maxPolarAngle = Math.PI / 2;

	mouse = new THREE.Vector2();
	mouse_moved = false;
	mouse_valid = false;
	is_touch = false;

	raycaster = new THREE.Raycaster();

	scene = new THREE.Scene();
	scene.background = new THREE.Color(0xf0f0f0);

	var light = new THREE.DirectionalLight(0xffffff, 1);
	light.position.set(1, 1, 1).normalize();
	scene.add(light);

	lightwood = new THREE.TextureLoader().load(lightwoodtexture);
	darkwood = new THREE.TextureLoader().load(darkwoodtexture);
	reddarkwood = new THREE.TextureLoader().load(reddarkwoodtexture);
	wood = new THREE.TextureLoader().load(woodtexture);

	board = [];
	poles = [];
	turn = 1;
	balls = [];


	for (var i = 0; i <= 3; i++) {
		board[i] = [];
		for (var j = 0; j <= 3; j++) {
			board[i][j] = 0;
			var material = new THREE.MeshBasicMaterial({
				map: darkwood
			});
			var pole = new THREE.Mesh(new THREE.CylinderGeometry(10, 10, 300, 64, 5), material);
			pole.position.set(-150 + 100 * i, 0, -150 + 100 * j);
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
	var base = new THREE.Mesh(new THREE.BoxGeometry(350, 10, 350), material);
	base.position.set(0, -155, 0);
	scene.add(base);

	document.addEventListener('mousemove', onDocumentMouseMove, false);
	document.addEventListener('mouseup', onDocumentMouseUp, false);
	document.addEventListener('mousedown', onDocumentMouseDown, false);

	document.addEventListener('touchstart', onDocumentTouchStart, false);
	document.addEventListener('touchend', onDocumentTouchEnd, false);
	document.addEventListener('touchcancel', onDocumentTouchCancel, false);

	window.addEventListener('resize', onWindowResize, false);

	socket.emit('reset', 'new web client')

} // End init()

function onWindowResize() {
	camera.aspect = window.innerWidth / window.innerHeight;
	camera.updateProjectionMatrix();

	renderer.setSize(window.innerWidth, window.innerHeight);
}


function onDocumentMouseDown(event) {
	mouse_moved = false;
}

function onDocumentMouseMove(event) {
	var oldx = mouse.x,
		oldy = mouse.y;
	mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
	mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

	if (oldx != mouse.x || oldy != mouse.y) {
		mouse_moved = true;
	}
	mouse_valid = true;
}


function onDocumentTouchStart(event) {
	last_intersected = INTERSECTED;
	is_touch = true;
	mouse_valid = false;
	unpick();
}

function onDocumentTouchEnd(event) {}

function onDocumentTouchCancel(event) {
	is_touch = false;
}

function onDocumentMouseUp(event) {
	pick();
	if (!mouse_moved && (!is_touch || INTERSECTED == last_intersected)) {
		makeMove();
		if (is_touch) {
			mouse_valid = false;
			unpick();
		}
	}

	is_touch = false;
}

function makeMove() {
	if (INTERSECTED && INTERSECTED.is_pole) {
		var i = INTERSECTED.numx;
		var j = INTERSECTED.numy;
		if (board[i][j] < 4) {
			var n = board[i][j]
			socket.emit('move', {
				i: i,
				j: j
			})
			turn = 1 - turn
			board[i][j]= n + 1
			createBall(i, j, n)
		}
	}
}

function createBall(i, j, n) {
	var material = new THREE.MeshBasicMaterial({
		map: turn == 1 ? darkwood : lightwood
	});

	var ball = new THREE.Mesh(new THREE.SphereGeometry(35, 32, 32), material);
	ball.position.set(-150 + 100 * i, -150 + 34 + 68 * n, -150 + 100 * j);
	ball.rotation.set(Math.random() * 2 * Math.PI, Math.random() * 2 * Math.PI, Math.random() * 2 * Math.PI);
	scene.add(ball);
    balls.push(ball);
    
}

function resetBoard() {
	turn = 1
	for (var i = 0; i <= 3; i++) {
		board[i] = []
		for (var j = 0; j <= 3; j++) {
			board[i][j] = 0;
		}
	}

	balls.forEach(ball => {scene.remove(ball)})
	balls = []

}

function animate() {
	requestAnimationFrame(animate);

	controls.update();

	render();
}

function unpick() {
	if (INTERSECTED) {
		INTERSECTED.material.map = darkwood;
	}
	INTERSECTED = null;
}

function pick() {
	raycaster.setFromCamera(mouse, camera);

	var intersects = raycaster.intersectObjects(poles);

	if (intersects.length > 0) {
		if (INTERSECTED != intersects[0].object) {
			unpick();
			INTERSECTED = intersects[0].object;
			INTERSECTED.material.map = reddarkwood;

		}
	} else {
		unpick();
	}
}


function render() {
	if (!is_touch && mouse_valid) {
		pick();
	}

	renderer.render(scene, camera);
}
