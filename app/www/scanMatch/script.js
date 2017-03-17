function onceDocumentReady() {
	var scanMatchPage = new Vue({
		el: '#vue-app',
		methods: {
			saveMatch: function (scanned_match) {
				var matches = JSON.parse(localStorage.getItem('matches') || '{}');
				var scanned_match_id = scanned_match.match_id || null;
				if (scanned_match_id in matches) {
					var stored_match_date = new Date(matches[scanned_match_id].last_modified);
					var scanned_match_date = new Date(scanned_match.last_modified);
					console.log('Stored Match Date:', stored_match_date);
					console.log('Scanned Match Date:', scanned_match_date);
					if (scanned_match_date.getTime() > stored_match_date.getTime()) {
						console.log('Scanned Match was modified more recently');
						matches[scanned_match_id] = scanned_match;
						localStorage.setItem('matches', JSON.stringify(matches));
						toast('info', 'Saved updated Data', '');
					} else if (scanned_match_date.getTime() === stored_match_date.getTime()) {
						console.log('Scanned Match was modified at the same time as Stored Match');
						toast('info', 'Nothing Changed', 'Scanned Data modified at the same time as Stored Data.');
					} else {
						console.log('Stored Match was modified more recently');
						toast('info', 'Nothing Changed', 'Stored Data more recent than Scanned Data');
					}
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
								console.log('info', 'Scanned Match JSON:', unpackedJson);
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