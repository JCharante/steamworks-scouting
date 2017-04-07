function onceDocumentReady() {
	if ((localStorage.getItem('scoutName') || '') === '') {
		alert('Please set your name in the settings page.');
		window.location.replace('../settings/index.html');
	}

	if ((localStorage.getItem('serverPassword') || '') === '') {
		alert('Please set the server password in the settings page.');
		window.location.replace('../settings/index.html');
	}

	var upload_page = new Vue({
		el: '#vue-app',
		mounted: function() {
			var self = this;
			self.scout_name = localStorage.getItem('scoutName');
			self.serverPassword = localStorage.getItem('serverPassword');
		},
		data: function() {
			return {
				scout_name: '',
				serverPassword: ''
			}
		},
		methods: {
			markMatchesAsUploaded: function(uploadedMatches) {
				var self = this;
				var matches = JSON.parse(localStorage.getItem('matches') || '{}');
				for (var key in matches) {
					if(!matches.hasOwnProperty(key)) continue;

					var match = matches[key];

					uploadedMatches.forEach( function (uploadedMatch) {
						if (match.match_id === uploadedMatch.match_id) {
							match.changedSinceUpload = false;
						}
					});
				}

				localStorage.setItem('matches', JSON.stringify(matches));
			},
			upload: function () {
				var self = this;
				var matches = JSON.parse(localStorage.getItem('matches') || '{}');
				var data = {
					'matches': [],
					'serverPassword': self.serverPassword
				};

				for (var key in matches) {
					if(!matches.hasOwnProperty(key)) continue;

					var match = matches[key];

					if (!match.team_number) {
						var audio = new Audio('../static/external/media/fog-blast.wav');
						audio.play();
						toast('error', 'Preflight Check Failed', 'Team Number is blank in ' + match.event_name + ' - Q' + match.match_number);
						return null;
					}

					if (!match.match_number) {
						var audio = new Audio('../static/external/media/fog-blast.wav');
						audio.play();
						toast('error', 'Preflight Check Failed', 'Match Number is blank in ' + match.event_name + ' - Q' + match.match_number);
						return null;
					}

					if (match.scout_name == self.scout_name && match.changedSinceUpload) {
						data.matches.push(match)
					}
				}
				console.log(data);
				$.ajax({
					method: 'POST',
					url: 'http://achilles.jcharante.com/match/upload',
					data: JSON.stringify(data),
					dataType: "json",
					contentType: "application/json",
					statusCode: {
						200: function (response) {
							console.log('Server Replied: ', response);
							self.markMatchesAsUploaded(data.matches);
							toast('success', 'Success!', 'Scouted Matches Successfully Uploaded');
						},
						400: function (responseObject) {
							console.log('Server Replied: ', responseObject);
							var data = responseObject.responseJSON;
							toast('error', 'Error Code', data.error.error_code);
							toast('error', 'Message', data.error.message);
							toast('error', 'Fields', data.error.fields);
							playFieldFault();
						},
						500: function (responseObject) {
							console.log('Server Replied: ', responseObject);
							toast('error', 'Oh No!', 'The Server Encountered An Error')
						}
					}
				});
			}
		}
	});
}


$(document).ready(onceDocumentReady);