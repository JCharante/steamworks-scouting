Vue.component('match-row', {
	props: ['match_number', 'match_id'],
	mounted: function() {
		var self = this;
		console.log("Match Row: ", self.match_number, self.match_id);
	},
	computed: {
		matchPageLink: function() {
			var self = this;
			return '/app/matches/match?match_id=' + self.match_id;
		}
	},
	template:
	'<div class="col-lg2 col-md-3 col-xs-6">' +
		'<div class="panel panel-default">' +
			'<div class="panel-heading">' +
				'<p>Match #{{ match_number }}:</p>' +
			'</div>' +
			'<div class="panel-body">' +
				'<a :href="matchPageLink"><p>Match Page</p></a>' +
			'</div>' +
		'</div>' +
	'</div>'
});

Vue.component('matches-list', {
	mounted: function() {
		var self = this;
		console.log("Matches List: ", self.matches);
	},
	props: ['matches'],
	template:
	'<div>' +
		'<match-row v-for="match in matches" :match_number="match.match_number" :match_id="match.match_id"></match-row>' +
	'</div>'
});


Vue.component('event-page', {
	mounted: function() {
		var self = this;
		var event_id = $.QueryString.event_id;

		var data = {
			event_id: event_id
		};

		$.ajax({
			method: 'POST',
			url: '/api/event/details',
			data: JSON.stringify(data),
			dataType: "json",
			contentType: 'application/json',
			statusCode: {
				200: function (data) {
					self.$data.details = data.details;
					console.log("Events Page: ", self.$data.details);
				}
			}
		})
	},
	template:
	'<div>' +
		'<h1 class="text-center">{{ details.name }}</h1>' +
		'<matches-list :matches="details.matches"></matches-list>' +
	'</div>',
	data: function () {
		return {
			details: {
				name: 'Loading Event Name',
				event_id: 'Loading Event ID',
				matches: []
			}
		}
	}
});

function onceDocumentReady() {
	var eventPage = new Vue({
		el: '#vue-app',
		template: '<event-page></event-page>'
	});
}

$(document).ready(onceDocumentReady);
