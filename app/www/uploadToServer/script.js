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
						},
						400: function (responseObject) {
							console.log('Server Replied: ', responseObject);
							var data = responseObject.responseJSON;
						}
					}
				});
			}
		}
	});
}


$(document).ready(onceDocumentReady);