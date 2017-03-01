Vue.component('team-list', {
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

Vue.component('teams-list', {
	mounted: function() {
		var self = this;
		//console.log("Teams List: ", self.teams);
	},
	props: ['red_team', 'blue_team', 'match_id'],
	methods: {
		teamAtMatchPageLink: function(team_number) {
			var self = this;
			return '/app/matches/match/scout?team_number' + team_number + '&match_id=' + self.match_id;
		}
	},
	template:
	'<div>' +
		'<div class="col-md-6 col-xs-6">' +
			'<div class="panel panel-default">' +
				'<div class="panel-heading">' +
					'<p>Red Team</p>' +
				'</div>' +
				'<div class="panel-body">' +
					'<a v-for="team_number in red_team" :href="teamAtMatchPageLink(team_number)"><p>Scout Team #{{ team_number }} for this Match</p></a>' +
				'</div>' +
			'</div>' +
		'</div>' +
		'<div class="col-md-6 col-xs-6">' +
			'<div class="panel panel-default">' +
				'<div class="panel-heading">' +
					'<p>Blue Team</p>' +
				'</div>' +
				'<div class="panel-body">' +
					'<a v-for="team_number in blue_team" :href="teamAtMatchPageLink(team_number)"><p>Scout Team #{{ team_number }} for this Match</p></a>' +
				'</div>' +
			'</div>' +
		'</div>' +
	'</div>'
});

Vue.component('add-team', {
	methods: {
		add_team: function() {
			var self = this;
			var side = $('input[name=side]:checked').val();
			var team_number = $('#team-number').val();
			var match_id = $.QueryString.match_id;

			var data = {
				team_number: team_number,
				match_id: match_id,
				side: side
			};

			console.log(data);

			$.ajax({
				method: 'POST',
				url: '/api/match/add_team',
				data: JSON.stringify(data),
				dataType: "json",
				contentType: "application/json",
				statusCode: {
					200: function (data) {
						console.log('Server Replied: ', data);
						toastr["success"]("", "Created Match");
						self.$emit('team-added');
						$('#team_number').val('');
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
				'<label for="team-number">Team Number</label>' +
				'<input type="text" class="form-control" id="team-number" placeholder="5687">' +
			'</div>' +
			'<div class="radio row">' +
				'<label class="col-xs-6">' +
					'<input type="radio" name="side" value="red" checked>' +
					'Red Team' +
				'</label>' +
				'<label class="col-xs-6">' +
					'<input type="radio" name="side" value="blue">' +
					'Blue Team' +
				'</label>' +
			'</div>' +
			'<div class="">' +
				'<button v-on:click="add_team()" type="button" class="btn btn-primary btn-lg btn-block">Add Team to Match</button>' +
			'</div>' +
		'</div>' +
	'</div>'
});


Vue.component('match-page', {
	mounted: function() {
		var self = this;
		self.fetch_details()
	},
	methods: {
		fetch_details: function() {
			var self = this;
			var match_id = $.QueryString.match_id;

			var data = {
				match_id: match_id
			};

			$.ajax({
				method: 'POST',
				url: '/api/match/details',
				data: JSON.stringify(data),
				dataType: "json",
				contentType: 'application/json',
				statusCode: {
					200: function (data) {
						console.log("Match Page: ", self);
						self.$data.details = data.details;
						console.log("Match Page: ", self.$data);
					}
				}
			})
		}
	},
	template:
	'<div>' +
		'<h1 class="text-center">{{ details.event_name }} - Match #{{ details.match_number }}</h1>' +
		'<hr>' +
		'<add-team v-on:team-added="fetch_details()"></add-team>' +
		'<hr>' +
		'<teams-list :red_team="details.red_team" :blue_team="details.blue_team" :match_id="details.match_id"></teams-list>' +
	'</div>',
	data: function () {
		return {
			details: {
				event_id: 'Loading event ID',
				event_name: 'Loading Event Name',
				match_number: 'Loading Match Number',
				match_id: 'Loading Match ID',
				red_team: [],
				blue_team: []
			}
		}
	}
});

function onceDocumentReady() {
	var matchPage = new Vue({
		el: '#vue-app',
		template: '<match-page></match-page>'
	});
}

$(document).ready(onceDocumentReady);
