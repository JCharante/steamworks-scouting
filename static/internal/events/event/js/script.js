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
				'<a class="btn btn-primary" :href="matchPageLink" role="button">Match Page</a>' +
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

Vue.component('create-match', {
	methods: {
		create_match: function() {
			var self = this;
			var match_number = $('#match-number').val();
			var event_id = $.QueryString.event_id;

			var data = {
				match_number: match_number,
				event_id: event_id
			};

			$.ajax({
				method: 'POST',
				url: '/api/matches/create',
				data: JSON.stringify(data),
				dataType: "json",
				contentType: "application/json",
				statusCode: {
					200: function (data) {
						console.log('Server Replied: ', data);
						toastr["success"]("", "Created Match");
						self.$emit('match-creation');
						$('#match-number').val('');
					},
					400: function (responseObject) {
						console.log('Server Replied: ', responseObject);
						var data = responseObject.responseJSON;
						toastr["error"](data.message, "Error Creating Match");
					}
				}
			});
		}
	},
	template:
	'<div class="row">' +
		'<div class="col-xs-12 col-md-6 col-md-offset-3 col-lg-4 col-lg-offset-4">' +
			'<div class="form-group">' +
				'<label for="match-number">Match Number</label>' +
				'<input type="text" class="form-control" id="match-number" placeholder="42">' +
			'</div>' +
		'</div>' +
		'<div class="col-xs-12 col-md-6  col-md-offset-3 col-lg-4 col-lg-offset-4">' +
			'<button v-on:click="create_match()" id="create-event" type="button" class="btn btn-primary btn-lg btn-block">Create Match</button>' +
		'</div>' +
	'</div>'
});

Vue.component('register-team-at-event', {
	methods: {
		register_team: function() {
			var self = this;
			var team_number = $('#team-number').val();
			var event_id = $.QueryString.event_id;

			var data = {
				team_number: team_number,
				event_id: event_id
			};

			$.ajax({
				method: 'POST',
				url: '/api/event/teams/add',
				data: JSON.stringify(data),
				dataType: "json",
				contentType: "application/json",
				statusCode: {
					200: function (data) {
						console.log('Server Replied: ', data);
						toastr["success"]("", "Registered Team At Event");
						self.$emit('team-registered');
						$('#team-number').val('');
					},
					400: function (responseObject) {
						console.log('Server Replied: ', responseObject);
						var data = responseObject.responseJSON;
						toastr["error"](data.message, "Error Registering Team");
					}
				}
			});
		}
	},
	template:
	'<div class="row">' +
		'<div class="col-xs-12 col-md-6 col-md-offset-3 col-lg-4 col-lg-offset-4">' +
			'<div class="form-group">' +
				'<label for="tean-number">Team Number</label>' +
				'<input type="text" class="form-control" id="team-number" placeholder="5687">' +
			'</div>' +
		'</div>' +
		'<div class="col-xs-12 col-md-6  col-md-offset-3 col-lg-4 col-lg-offset-4">' +
			'<button v-on:click="register_team()" type="button" class="btn btn-primary btn-lg btn-block">Register Team</button>' +
		'</div>' +
	'</div>'
});


Vue.component('team-row', {
	props: ['team_name', 'team_number'],
	mounted: function() {
		var self = this;
		console.log("Team Row: ", self.team_name, self.team_number);
	},
	computed: {
		teamPageLink: function() {
			var self = this;
			return '/app/teams/team?team_number=' + self.team_number;
		}
	},
	template:
	'<div class="col-md-4 col-xs-12">' +
		'<div class="panel panel-default">' +
			'<div class="panel-heading">' +
				'<p>{{ team_number }} - {{ team_name }}</p>' +
			'</div>' +
			'<div class="panel-body">' +
				'<a :href="teamPageLink"><p>Team Page</p></a>' +
			'</div>' +
		'</div>' +
	'</div>'
});

Vue.component('teams-list', {
	props: ['teams'],
	template:
	'<div class="row">' +
		'<team-row v-for="team in teams" :team_name="team.team_name" :team_number="team.team_number"></team-row>' +
	'</div>'
});

Vue.component('teams-at-event', {
	props: ['teams'],
	methods: {
		teamRegistered: function() {
			var self = this;
			self.$emit('team-registered');
		}
	},
	template:
	'<div>' +
		'<h2 class="text-center">Teams</h2>' +
		'<register-team-at-event v-on:team-registered="teamRegistered()"></register-team-at-event>' +
		'<hr>' +
		'<teams-list :teams="teams"></teams-list>' +
	'</div>'
});


Vue.component('event-page', {
	mounted: function() {
		var self = this;
		self.fetch_details()
	},
	methods: {
		fetch_details: function() {
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
						console.log("Events Page: ", self);
						self.$data.details = data.details;
						console.log("Events Page: ", self.$data.details);
					}
				}
			})
		}
	},
	template:
	'<div>' +
		'<h1 class="text-center">{{ details.name }}</h1>' +
		'<hr>' +
		'<teams-at-event v-on:team-registered="fetch_details()" :teams="details.teams"></teams-at-event>' +
		'<hr>' +
		'<h2 class="text-center">Matches</h2>' +
		'<create-match v-on:match-creation="fetch_details()"></create-match>' +
		'<hr>' +
		'<matches-list :matches="details.matches"></matches-list>' +
	'</div>',
	data: function () {
		return {
			details: {
				name: 'Loading Event Name',
				event_id: 'Loading Event ID',
				matches: [],
				teams: []
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
