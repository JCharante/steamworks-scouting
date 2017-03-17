function onceDocumentReady() {
	var scanMatchPage = new Vue({
		el: '#vue-app',
		methods: {
			saveMatch: function (scanned_match) {
				var matches = JSON.parse(localStorage.getItem('matches') || '{}');
				var scanned_match_id = scanned_match.match_id || null;
				if (scanned_match_id in matches) {
					toast('info', 'Duplicate Match', '');
				} else {
					matches[scanned_match_id] = scanned_match;
					localStorage.setItem('matches', JSON.stringify(matches));
					toast('info', 'Imported Match', scanned_match.match_number);
				}
			},
			scan: function () {
				var self = this;
				cordova.plugins.barcodeScanner.scan(
					function (result) {
						if(!result.cancelled) {
							if(result.format == "QR_CODE") {
								console.log('QR Code Scanned', 'Data:', result.text);
								var packed_json = result.text;
								var unpackedJson = null;
								try {
									unpackedJson = JSONC.unpack(packed_json);
								} catch (e) {
									return null;
								}
								console.log('info', 'Scanned Match JSON', JSON.stringify(unpackedJson));
								self.saveMatch(unpackedJson);
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