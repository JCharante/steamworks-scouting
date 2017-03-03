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
	computed: {
		linkToEventPage: function() {
			var self = this;
			return '/app/events/event?event_id=' + self.event_id;
		}
	},
	template:
	'<div>' +
		'<hr>' +
		'<h3 class="text-center"><a :href="linkToEventPage">{{ event_name }}</a></h3>' +
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


Vue.component('team-options', {
	props: ['team_number'],
	methods: {
		deleteTeam: function() {
			var self = this;
			var team_number_entered = prompt('To delete the team (Cannot be Undone!!!) enter the team number');
			if (team_number_entered == self.team_number) {
				var data = {
					team_number: self.team_number
				};

				$.ajax({
					method: 'POST',
					url: '/api/team/delete',
					data: JSON.stringify(data),
					dataType: "json",
					contentType: "application/json",
					statusCode: {
						200: function (data) {
							console.log('Server Replied: ', data);
							toastr["success"]("You mad lad!!", "Team Deleted.");
							window.location.replace('/app/teams/all');
						},
						400: function (responseObject) {
							console.log('Server Replied: ', responseObject);
							var data = responseObject.responseJSON;
							toastr["error"](data.message, "Error Deleting Team");
						}
					}
				});
			} else {
				toastr["info"]("Entered Incorrect Team Number", "Did Not Delete Team");
			}
		}
	},
	template:
	'<div class="row">' +
		'<h3 class="text-center">Options</h3>' +
		'<a class="btn btn-danger" role="button" v-on:click="deleteTeam">Delete Team</a>' +
	'</div>'
});

Vue.component('team-notes', {
	mounted: function() {
		var self = this;
		self.$data.team_number = $.QueryString.team_number;
		self.getNotes();
	},
	data: function() {
		return {
			team_number: 0,
			notes: [
				{
					note_id: '1',
					message: 'Loading Note Message...'
				},
				{
					note_id: '2',
					message: 'Loading Note Message...'
				}
			]
		}
	},
	methods: {
		saveChanges: function() {
			var self = this;
			console.log(self.notes);
			for (var i = 0; i < self.notes.length; i++) {
				var note = self.notes[i];
				if (note.message == '') {
					var data = {
						note_id: note.note_id
					};

					$.ajax({
						method: 'POST',
						url: '/api/team/note/delete',
						data: JSON.stringify(data),
						dataType: "json",
						contentType: "application/json",
						statusCode: {
							200: function (data) {
								console.log('Server Replied: ', data);
								self.getNotes();
							},
							400: function (responseObject) {
								console.log('Server Replied: ', responseObject);
								var data = responseObject.responseJSON;
								toastr["error"](data.message, "Error Deleting Note");
							}
						}
					});
				} else {
					var data = {
						note_id: note.note_id,
						message: note.message
					};

					$.ajax({
						method: 'POST',
						url: '/api/team/note/edit',
						data: JSON.stringify(data),
						dataType: "json",
						contentType: "application/json",
						statusCode: {
							200: function (data) {
								console.log('Server Replied: ', data);
								self.getNotes();
							},
							400: function (responseObject) {
								console.log('Server Replied: ', responseObject);
								var data = responseObject.responseJSON;
								toastr["error"](data.message, "Error Updating Note");
							}
						}
					});
				}
			}
		},
		discardChanges: function() {
			var self = this;
			self.getNotes();
		},
		getNotes: function() {
			var self = this;
			var data = {
				team_number: self.team_number
			};

			$.ajax({
				method: 'POST',
				url: '/api/team/notes',
				data: JSON.stringify(data),
				dataType: "json",
				contentType: "application/json",
				statusCode: {
					200: function (data) {
						console.log('Server Replied: ', data);
						self.$data.notes = data.notes;
					},
					400: function (responseObject) {
						console.log('Server Replied: ', responseObject);
						var data = responseObject.responseJSON;
						toastr["error"](data.message, "Error Fetching Notes");
					}
				}
			});
		},
		addNote: function() {
			var self = this;
			var data = {
				team_number: self.team_number,
				message: 'New Note'
			};

			$.ajax({
				method: 'POST',
				url: '/api/team/notes/add',
				data: JSON.stringify(data),
				dataType: "json",
				contentType: "application/json",
				statusCode: {
					200: function (data) {
						console.log('Server Replied: ', data);
						toastr["success"]("", "Added Note");
						self.getNotes();
					},
					400: function (responseObject) {
						console.log('Server Replied: ', responseObject);
						var data = responseObject.responseJSON;
						toastr["error"](data.message, "Error Creating Note");
						self.getNotes();
					}
				}
			});
		}
	},
	template:
	'<div class="row">' +
		'<h3 class="text-center">Team Notes</h3>' +
		'<p class="text-center">Leave Blank to Delete Note</p>' +
		'<form class="form-horizontal" role="form">' +
			'<div v-for="note in notes" class="form-group">' +
				'<label class="col-lg-3 control-label"> </label>' +
				'<div class="col-lg-6">' +
					'<input class="form-control" type="text" v-model="note.message">' +
				'</div>' +
			'</div>' +
			'<div class="form-group">' +
				'<label class="col-lg-3 control-label">Options:</label>' +
				'<a class="btn btn-primary" role="button" v-on:click="saveChanges">Save Changes</a> ' +
				'<a class="btn btn-default" role="button" v-on:click="discardChanges">Discard Changes</a> ' +
				'<a class="btn btn-default" role="button" v-on:click="addNote">Add Note</a> ' +
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
		'<team-options :team_number="team_number"></team-options>' +
		'<hr>' +
		'<team-notes></team-notes>' +
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
