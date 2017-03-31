function onceDocumentReady() {
	var download_page = new Vue({
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
			download: function () {
				var self = this;
				$.ajax({
					method: 'GET',
					url: 'http://achilles.jcharante.com/download',
					contentType: "application/json",
					statusCode: {
						200: function (data) {
							console.log('Server Replied: ', data);
							for (var i = 0; i < data.matches.length; i++) {
								var match = data.matches[i];
								self.saveMatch(match);
							}
							toast('success', 'Success!', 'Scouted Matches Successfully Downloaded');
						}
					}
				});
			}
		}
	});
}


$(document).ready(onceDocumentReady);