/* Creates a typing animation of the splash text. */
/* Please note that this file may need to be edited if the content of the splash text is modified. */

var i = 0;
var text = "Hello world";
var speed = 800; // The speed in milliseconds that lines are to be revealed

/* Sleep function for waiting between letters */
/* ms: The speed in ms for letters to be revealed */
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

/* Types out words letter by letter */
/* object: JQuery object to append | text: String to print */
function typeWriter(object, text) {

    /* Determine the typing speed of the individual letters */
    typingSpeed = speed / 20;

    /* Type the individual letters */
    if (i < text.length) {
        $(object).append(text.charAt(i));
        i++;
        sleep(typingSpeed).then(() => typeWriter(object, text));
    } else if (i === text.length) {
        /* Resets index when word is completed */
        i = 0;
    }
    
}

/* Plays the terminal animation when the page loads */
$(document).ready(function() {

    /* Collects each line */
    splashLines = $(".line");

    /* Iterates through splash page lines */
    /* index: line number | value: HTML object */
    jQuery.each(splashLines, function(index, value) {

        setTimeout(function() {
            if ($(value).hasClass("splash-input")) {
                /* Lines that are meant to look like user input are typed out */
                text = $(value).text();
                $(value).text("");
                $(value).toggleClass("invisible");
                typeWriter(value, text);
            } else if ($(value).hasClass("splash-output")) {
                /* Because it is the response of the "system" this text appears instantly */
                $(value).toggleClass("invisible");
            }
        }, speed * index);

    });

});
