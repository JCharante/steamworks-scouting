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

Vue.component('event', {
	template:
	'<div class="col-md-6 col-xs-6">' +
		'<div class="panel panel-default">' +
			'<div class="panel-heading">' +
				'<p>Red Team</p>' +
			'</div>' +
			'<div class="panel-body">' +
				//'<a v-for="team_number in red_team" :href="teamAtMatchPageLink(team_number)"><p>Scout Team #{{ team_number }} for this Match</p></a>' +
			'</div>' +
		'</div>' +
	'</div>'
});

Vue.component('events', {
	mounted: function() {
		var self = this;
	},
	props: ['events'],
	template:
	'<div>' +
		'<event v-for="event in events"></event>' +
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
		'<h1 class="text-center">{{ details.team_name }}</h1>' +
		'<hr>' +
		'<teams-list :red_team="details.red_team" :blue_team="details.blue_team" :match_id="details.match_id"></teams-list>' +
	'</div>',
	data: function () {
		return {
			details: {
				team_name: 'Loading Team Name',
				events: []
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
