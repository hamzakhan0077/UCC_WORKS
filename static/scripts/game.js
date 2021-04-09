
let threshold = 50;
let points = [];

let canvas;
let ctx;
let width;
let height;

let interval_id;
   
let red = {
    x : 415,
    y : 0,
	ychange:10,
    size: 50,
};
   
let green = {
    x : 490,
    y : 0,
	ychange:10,
	size: 50,
    
};

let plc = {
    x : 170,
    y : 0,
	ychange:10,
	size: 10,
    
};
   
let car = {
    x : 400,
    y : 850,
    size: 10,
};
let road = {
    x:0,
    y:0,
    ychange:29,
}

let roadpic  = document.createElement("img");
roadpic.src = "static/images/road2.png";
let carpic  = document.createElement("img");
carpic.src = "static/images/car.png";

let plcpic  = document.createElement("img");
plcpic.src = "static/images/plc.png";

let greencarpic  = document.createElement("img");
greencarpic.src = "static/images/green.png";

let redcarpic  = document.createElement("img");
redcarpic.src = "static/images/red.png";

let moveRight = false;
let moveUp = false;
let moveDown = false;
let moveLeft = false;
    
document.addEventListener('DOMContentLoaded', init, false); // run init once canvas i loaded
document.addEventListener('keydown', activate, false);
document.addEventListener('keyup', deactivate, false);




function getRandomNumber(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min; // our random function
}

function init() {
    canvas = document.querySelector('canvas'); // go to html and find canvas
	ctx = canvas.getContext('2d'); // establish a context
    width = canvas.width; //  link width to canvas width in html
    height = canvas.height;// link height to canvas height in html
    interval_id = window.setInterval(draw,33) ;// call draw every 33 second
};
	



function draw() {
	ctx.clearRect(0,0,width,height);
	ctx.drawImage(roadpic,road.x,road.y);
	road.y = road.y + road.ychange
	ctx.drawImage(roadpic,road.x,road.y - 800)
	if (road.y >= height-300){
		road.y = road.y * 0
	}
	ctx.drawImage(carpic,car.x,car.y)
	
	//traffic
	//the police car
	ctx.drawImage(plcpic,plc.x,plc.y - 160);
	plc.y = plc.y + plc.ychange
	if (plc.y >= height+150){
		plc.y = plc.y * 0
		plc.x = getRandomNumber(170,255);
		
		
	}
	
	//the red Bentley
	ctx.drawImage(redcarpic,red.x,red.y - 160);
	red.y = red.y + red.ychange
	if (red.y >= height+150){
		red.y = red.y * 0
		red.x = getRandomNumber(415,500);
	}
	// the green Maserati <3
	
	ctx.drawImage(greencarpic,green.x,green.y - 300);
	green.y = green.y + green.ychange
	if (green.y >= height+450){
		green.y = green.y * 0
		green.x = getRandomNumber(415,500);
	}
	
	if (moveRight) {
        car.x += 10;

    }
	if (moveUp) {
        car.y -= 10;
    }
	if (moveDown) {
        car.y += 10;
    }
	if (moveLeft){
		car.x -= 10;
	}
	if (car.x <= 165){car.x=170}
	if (car.x >= 545){car.x=540}
	if (car.y >= 860){car.y=855}
	if (car.y <= 0){car.y = 5}
	
	if (collide()){
			stop();
            window.alert('YOU LOST!');
	}



	

	
}; 

// Core Event Driven Programming



function activate(){
	let keycode = event.keyCode;
	if(keycode === 87){
		moveUp = true;
		
	}
	else if (keycode === 68){
		moveRight = true;
	}
	else if (keycode === 83){
		moveDown = true;
	
	}
	else if (keycode === 65){
		moveLeft = true;
	
	}
};

function deactivate(){
	let keycode = event.keyCode;
	if(keycode === 87){
		moveUp = false;
		
	}
	else if (keycode === 68){
		moveRight = false;
	}
	else if (keycode === 83){
		moveDown = false;
	
	}
	else if (keycode === 65){
		moveLeft = false;
	
	}
};


function stop(){
	window.clearInterval(interval_id);
	window.removeEventListener('keydown', activate);
	window.removeEventListener('keyup', deactivate);
};


//???

function collide(){
	if (car.x + car.size < plc.x ||
        plc.x + plc.size < car.x ||
        car.y > plc.y + plc.size ||
        plc.y > car.y + car.size) {
        return false;
    } else {
        return true;
    }
}
	
	









