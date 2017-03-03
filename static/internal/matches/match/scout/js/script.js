Vue.component('scout-data', {
	template:
	'<div class="row">' +
		'<h3 class="text-center">Data</h3>' +
	'</div>'
});

Vue.component('banner', {
	props: ['event_name', 'event_id', 'match_number', 'team_number', 'team_name', 'match_id'],
	computed: {
		linkToEventPage: function() {
			var self = this;
			return '/app/events/event?event_id=' + self.event_id;
		},
		linkToMatchPage: function() {
			var self = this;
			return '/app/matches/match?match_id=' + self.match_id;
		},
		teamPageLink: function() {
			var self = this;
			return '/app/teams/team?team_number=' + self.team_number;
		}
	},
	template:
	'<div class="row">' +
		'<h1 class="text-center">Scouting</h1>' +
		'<hr>' +
		'<h3 class="text-center"><a :href="linkToEventPage">{{ event_name }}</a> - <a :href="linkToMatchPage">Match #{{ match_number }}</a></h3>' +
		'<h4 class="text-center">Scouting <a :href="teamPageLink">Team #{{ team_number }} - {{ team_name }}</a></h4>' +
	'</div>'
});

Vue.component('scout-page', {
	methods: {
		getTeamInfo: function() {
			var self = this;

			var data = {
				team_number: self.team_number
			};

			$.ajax({
				method: 'POST',
				url: '/api/team/details',
				data: JSON.stringify(data),
				dataType: "json",
				contentType: "application/json",
				statusCode: {
					200: function (data) {
						console.log('Server Replied: ', data);
						self.$data.team_name = data.details.team_name;
					},
					400: function (responseObject) {
						console.log('Server Replied: ', responseObject);
						var data = responseObject.responseJSON;
						toastr["error"](data.message, "Error Retrieving Team Info");
					}
				}
			});
		},
		getMatchInfo: function() {
			var self = this;

			var data = {
				match_id: self.match_id
			};

			$.ajax({
				method: 'POST',
				url: '/api/match/details',
				data: JSON.stringify(data),
				dataType: "json",
				contentType: "application/json",
				statusCode: {
					200: function (data) {
						console.log('Server Replied: ', data);
						self.$data.event_id = data.details.event_id;
						self.$data.event_name = data.details.event_name;
						self.$data.match_number = data.details.match_number;
					},
					400: function (responseObject) {
						console.log('Server Replied: ', responseObject);
						var data = responseObject.responseJSON;
						toastr["error"](data.message, "Error Retrieving Team Info");
					}
				}
			});
		}
	},
	mounted: function() {
		var self = this;
		self.$data.team_number = $.QueryString.team_number;
		self.$data.match_id = $.QueryString.match_id;
		self.getTeamInfo();
		self.getMatchInfo();
	},
	data: function() {
		return {
			event_name: 'Loading Event Name',
			event_id: 'Loading Event ID',
			match_number: 0,
			match_id: 'Loading Match ID',
			team_number: 0,
			team_name: 'Loading Team Name'
		}
	},
	template:
	'<div class="row">' +
		'<banner :match_id="match_id" :event_name="event_name" :event_id="event_id" :match_number="match_number" :team_number="team_number" :team_name="team_name"></banner>' +
		'<scout-data></scout-data>' +
		'<hr>' +
	'</div>'
});

function onceDocumentReady() {
	var matchPage = new Vue({
		el: '#vue-app',
		template: '<scout-page></scout-page>'
	});
}

$(document).ready(onceDocumentReady);
