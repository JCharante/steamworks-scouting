function onceDocumentReady() {
	var scanMatchPage = new Vue({
		el: '#vue-app',
		methods: {
			scan: function () {
				cordova.plugins.barcodeScanner.scan(
					function (result) {
						if(!result.cancelled) {
							if(result.format == "QR_CODE") {
								console.log('QR Code Scanned', 'Data:', result.text);
								var packed_json = result.text;
								var unpackedJson = JSONC.unpack(packed_json);
								toast('info', 'Imported A Match!', JSON.stringify(unpackedJson));
							} else {
								toast('error', 'Whoops!', 'QR Code not Scanned. Try Again.');
							}
						}
					},
					function (error) {
						alert("Scanning failed: " + error);
					}
				);
			}
		}
	})
}


$(document).ready(onceDocumentReady);