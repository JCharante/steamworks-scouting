function onceDocumentReady() {
	var upload_page = new Vue({
		el: '#vue-app',
		methods: {
			upload: function () {
				var matches = JSON.parse(localStorage.getItem('matches') || '{}');
				var data = {
					'matches': []
				};

				for (var key in matches) {
					if(!matches.hasOwnProperty(key)) continue;

					var match = matches[key];

					if (match.team_number == null) {
						var audio = new Audio('../static/external/media/fog-blast.wav');
						audio.play();
						toast('error', 'Preflight Check Failed', 'Team Number is blank in ' + match.event_name + ' - ' + match.match_number);
						return null;
					}

					data.matches.push(match)
				}
				console.log(data);
				$.ajax({
					method: 'POST',
					url: 'http://achilles.jcharante.com/match/upload',
					data: JSON.stringify(data),
					dataType: "json",
					contentType: "application/json",
					statusCode: {
						200: function (data) {
							console.log('Server Replied: ', data);
							toast('success', 'Success!', 'Scouted Matches Successfully Uploaded');
						},
						400: function (responseObject) {
							console.log('Server Replied: ', responseObject);
							var data = responseObject.responseJSON;
							toast('error', 'Oh no!', 'Error while uploading matches');
						}
					}
				});
			}
		}
	});
}


$(document).ready(onceDocumentReady);