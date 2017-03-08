function scan() {
	toastr["info"]("Begin Scanning", "Info");
	QRScanner.scan(function(err, text) {
		alert(3);
		if (err) {
			toastr["error"]("","");
		} else {
			toastr["success"](text, 'Yay!');
		}
	});

	// Make the webview transparent so the video preview is visible behind it.
	QRScanner.show();
	// Be sure to make any opaque HTML elements transparent here to avoid
	// covering the video.
}


function onDone(err, status){
	if (err) {
		// here we can handle errors and clean up any loose ends.
		toastr["error"](err, "Error");
	}
	if (status.authorized) {
		// W00t, you have camera access and the scanner is initialized.
		// QRscanner.show() should feel very fast.
		toastr["success"]("Successfully Granted Permission", "Great!")
	} else if (status.denied) {
		toastr["error"]("I cannot work without a camera!", "Boo!!");
		// The video preview will remain black, and scanning is disabled. We can
		// try to ask the user to change their mind, but we'll have to send them
		// to their device settings with `QRScanner.openSettings()`.
	} else {
		toastr["info"]("Something happened, no idea what though", 'Whoops!');
		// we didn't get permission, but we didn't get permanently denied. (On
		// Android, a denial isn't permanent unless the user checks the "Don't
		// ask again" box.) We can ask again at the next relevant opportunity.
	}
}

function onDocumentReady() {
	//QRScanner.prepare(onDone);
	$('#scan').click(scan);
}

$(document).ready(function() {
	onDocumentReady()
});