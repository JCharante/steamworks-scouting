function scan() {
	cordova.plugins.barcodeScanner.scan(
		function (result) {
			if(!result.cancelled) {
				if(result.format == "QR_CODE") {
					toast("info", "QR Code Scanned!", result.text);
					/*navigator.notification.prompt("Please enter name of data",  function(input){
						var name = input.input1;
						var value = result.text;
						var data = localStorage.getItem("LocalData");
						console.log(data);
						data = JSON.parse(data);
						data[data.length] = [name, value];
						localStorage.setItem("LocalData", JSON.stringify(data));
						alert("Done");
					});*/
				}
			}
		},
		function (error) {
			alert("Scanning failed: " + error);
		}
	);
}

function onDocumentReady() {
	$('#scan').click(scan);
}

$(document).ready(function() {
	onDocumentReady()
});