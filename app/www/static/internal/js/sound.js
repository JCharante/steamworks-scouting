/*
To use this you must have
var staticContentPath
Defined in your page head.
 */

function playEndOfMatch() {
	var audio = new Audio(staticContentPath + '/external/media/buzzer.wav');
	audio.play();
}

function playFieldFault() {
	var audio = new Audio(staticContentPath + '/external/media/fog-blast.wav');
	audio.play();
}

function playTeleOpStart() {
	var audio = new Audio(staticContentPath + '/external/media/three-bells.wav');
	audio.play();
}

function playMatchStart() {
	var audio = new Audio(staticContentPath + '/external/media/charge-1.wav');
	audio.play();
}
