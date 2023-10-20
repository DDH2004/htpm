/* This file sets the time displayed in the corner of the screen to the current time */

function setTime() {
    /* Date format: YYYY-MM-DD HH:MM */
    var today = new Date();

    /* Formats date */
    var date = today.getFullYear() + "-" + (today.getMonth() + 1) + "-" + today.getDate();
    var minutes = today.getMinutes();
    if (minutes < 10) { // Corrects minutes displayed as a single digit
        minutes = "0" + minutes;
    }
    var time = today.getHours() + ":" + minutes;

    /* Sets page time to current time */
    $("#login-time").html(date + " " + time);
}

/* Time is updated every 5 seconds */
setInterval(setTime, 5000);