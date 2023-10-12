/* This file creates a typing animation of the splash text */

var i = 0;
var text = "Lorem ipsum dolor sit amet adept adipscing elit"; // The text to be typed out
var speed = 50; // The typing speed in milliseconds

function typeWriter() {
    if (i < text.length) {
        document.getElementById("splash-text").innerHTML += text.charAt(i);
        i++;
        setTimeout(typeWriter, speed);
    }
}