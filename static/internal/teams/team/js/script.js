Vue.component('match', {
	props: ['side', 'match_id', 'match_number'],
	computed: {
		matchPageLink: function() {
			var self = this;
			return '/app/matches/match?match_id=' + self.match_id;
		}
	},
	template:
	'<div class="col-lg-4 col-md-6 col-xs-12">' +
		'<div class="panel panel-default">' +
			'<div class="panel-heading">' +
				'<p> Match #{{ match_number }}</p>' +
			'</div>' +
			'<div class="panel-body">' +
				'<a class="btn btn-primary" :href="matchPageLink" role="button">Match Page</a>' +
			'</div>' +
		'</div>' +
	'</div>'
});

Vue.component('event', {
	props: ['event_name', 'event_id', 'matches'],
	template:
	'<div>' +
		'<hr>' +
		'<h3 class="text-center">{{ event_name }}</h3>' +
		'<match v-for="match in matches" :side="match.side" :match_id="match.match_id" :match_number="match.match_number"></match>' +
	'</div>'
});

Vue.component('events', {
	mounted: function() {
		var self = this;
	},
	props: ['events'],
	template:
	'<div>' +
		'<h2 class="text-center">Events</h2>' +
		'<event v-for="event in events" :event_name="event.event_name" :event_id="event.event_id" :matches="event.matches"></event>' +
	'</div>'
});


Vue.component('team-page', {
	mounted: function() {
		var self = this;
		self.$data.team_number = $.QueryString.team_number;
		self.fetch_details();
		self.fetch_matches();
	},
	methods: {
		fetch_details: function() {
			var self = this;
			var team_number = $.QueryString.team_number;

			var data = {
				team_number: team_number
			};

			$.ajax({
				method: 'POST',
				url: '/api/team/details',
				data: JSON.stringify(data),
				dataType: "json",
				contentType: 'application/json',
				statusCode: {
					200: function (data) {
						self.$data.details = data.details;
					}
				}
			})
		},
		fetch_matches: function() {
			var self = this;
			var team_number = $.QueryString.team_number;

			var data = {
				team_number: team_number
			};

			$.ajax({
				method: 'POST',
				url: '/api/team/matches',
				data: JSON.stringify(data),
				dataType: "json",
				contentType: 'application/json',
				statusCode: {
					200: function (data) {
						self.$data.events = data.events;
					}
				}
			})
		}
	},
	template:
	'<div>' +
		'<h1 class="text-center">Team #{{ team_number }} - {{ details.team_name }}</h1>' +
		'<events :events="events"></events>' +
	'</div>',
	data: function () {
		return {
			team_number: 0,
			details: {
				team_name: 'Loading Team Name',
				team_number: 0
			},
			events: [
				{
					event_id: "5baa51ac-abcf-40ae-91d2-c1d77fbbca09",
					event_name: "Loading Event Name",
					matches: [
						{
							match_id: "17b0f1d3-f28d-4c4d-8d00-fc2d27a66407",
							match_number: 1,
							side: "red"
						}
					]
				}
			]
		}
	}
});

function onceDocumentReady() {
	var teamPage = new Vue({
		el: '#vue-app',
		template: '<team-page></team-page>'
	});
}

$(document).ready(onceDocumentReady);
