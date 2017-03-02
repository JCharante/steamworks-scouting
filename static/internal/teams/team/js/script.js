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


Vue.component('robot', {
	props: ['robot'],
	mounted: function() {
		var self = this;
	},
	methods: {
		saveChanges: function() {
			var self = this;
			console.log(self.robot);
			var data = {
				robot_id: self.robot.robot_id,
				robot_name: self.robot.robot_name,
				team_number: self.robot.team_number,
				robot_type: self.robot.robot_type,
				has_actuated_gear_mechanism: self.robot.has_actuated_gear_mechanism
			};

			$.ajax({
				method: 'POST',
				url: '/api/robot/edit',
				data: JSON.stringify(data),
				dataType: "json",
				contentType: "application/json",
				statusCode: {
					200: function (data) {
						console.log('Server Replied: ', data);
						toastr["success"]("", "Modified Robot Details");
						self.$emit('refresh-details');
					},
					400: function (responseObject) {
						console.log('Server Replied: ', responseObject);
						var data = responseObject.responseJSON;
						toastr["error"](data.message, "Error Saving Changes");
					}
				}
			});
		},
		discardChanges: function() {
			var self = this;
			self.$emit('refresh-details');
		}
	},
	template:
	'<div class="row">' +
		'<h2 class="text-center">Robot</h2>' +
		'<form class="form-horizontal" role="form">' +
			'<div class="form-group">' +
				'<label class="col-lg-3 control-label">Robot name:</label>' +
				'<div class="col-lg-8">' +
					'<input class="form-control" type="text" v-model="robot.robot_name">' +
				'</div>' +
			'</div>' +
			'<div class="form-group">' +
				'<label class="col-lg-3 control-label">Robot Type:</label>' +
				'<div class="col-lg-8">' +
					'<div class="ui-select">' +
						'<select id="user_time_zone" class="form-control" v-model="robot.robot_type">' +
							'<option value="Unknown">Unknown</option>' +
							'<option value="Gear">Gear</option>' +
							'<option value="Defender">Defender</option>' +
							'<option value="Shooter">Shooter</option>' +
						'</select>' +
					'</div>' +
				'</div>' +
			'</div>' +
			'<div class="form-group">' +
				'<label class="col-lg-3 control-label">Bools:</label>' +
				'<input type="checkbox" v-model="robot.has_actuated_gear_mechanism"> Uses Actuated Gear Mechanism' +
			'</div>' +
			'<div class="form-group">' +
				'<label class="col-lg-3 control-label">Options:</label>' +
				'<a class="btn btn-primary" role="button" v-on:click="saveChanges">Save Changes</a> ' +
				'<a class="btn btn-default" role="button" v-on:click="discardChanges">Discard Changes</a>' +
			'</div>' +
		'</form>' +
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
		'<hr>' +
		'<robot v-on:refresh-details="fetch_details()" :robot="details.robot"></robot>' +
		'<hr>' +
		'<events :events="events"></events>' +
	'</div>',
	data: function () {
		return {
			team_number: 0,
			details: {
				team_name: 'Loading Team Name',
				team_number: 0,
				robot: {
					robot_name: 'Loading Robot Name',
					robot_id: 'Loading Robot ID',
					team_number: 0,
					robot_type: 'Loading Robot Type',
					has_actuated_gear_mechanism: false
				}
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
