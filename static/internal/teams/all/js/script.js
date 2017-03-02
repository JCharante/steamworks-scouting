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
	'<div class="col-lg4 col-md-6 col-xs-12">' +
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
	mounted: function() {
		var self = this;
		console.log("Teams List: ", self.teams);
	},
	props: ['teams'],
	template:
	'<div class="row">' +
		'<team-row v-for="team in teams" :team_name="team.team_name" :team_number="team.team_number"></team-row>' +
	'</div>'
});

Vue.component('teams-page', {
	delimiters: ['[[', ']]'],
	mounted: function() {
		var self = this;

		$.ajax({
			method: 'GET',
			url: '/api/teams/all',
			contentType: 'application/json',
			statusCode: {
				200: function (data) {
					self.$data.teams = data.teams;
					console.log("Teams Page: ", self.$data.teams);
				}
			}
		})
	},
	template:
	'<div class="row">' +
		'<h1 class="text-center">Teams</h1>' +
		'<teams-list :teams="teams"></teams-list>' +
	'</div>',
	data: function () {
		return {
			teams: []
		}
	}
});

function onceDocumentReady() {
	var teamsPage = new Vue({
		el: '#vue-app',
		template: '<teams-page></teams-page>'
	});
}

$(document).ready(onceDocumentReady);
