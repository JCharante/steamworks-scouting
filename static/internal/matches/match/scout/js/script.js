Vue.component('scout-data', {
	methods: {
		getScoutData: function() {
			var self = this;

			var data = {
				match_id: self.match_id,
				team_number: self.team_number
			};

			$.ajax({
				method: 'POST',
				url: '/api/match/scout/details',
				data: JSON.stringify(data),
				dataType: "json",
				contentType: "application/json",
				statusCode: {
					200: function (data) {
						console.log('Server Replied: ', data);
						self.$data.side = data.details.side;
						self.$data.low_goal = data.details.low_goal;
						self.$data.high_goal = data.details.high_goal;
						self.$data.gears = data.details.gears;
						self.$data.auto_gear_position = data.details.auto_gear_position;
						self.$data.climbing_rating = data.details.climbing_rating;
					},
					400: function (responseObject) {
						console.log('Server Replied: ', responseObject);
						var data = responseObject.responseJSON;
						toastr["error"](data.message, "Error Retrieving Team Info");
					}
				}
			});
		},
		addGear: function() {
			var self = this;
			self.gears += 1;
		},
		subtractGear: function() {
			var self = this;
			self.gears -= 1;
		}
	},
	data: function() {
		return {
			match_id: 'Loading Match ID',
			team_number: 0,
			side: 'red',
			low_goal: 0,
			high_goal: 0,
			gears: 0,
			auto_gear_position: 'None',
			climbing_rating: 0
		}
	},
	mounted: function() {
		var self = this;
		self.$data.team_number = $.QueryString.team_number;
		self.$data.match_id = $.QueryString.match_id;
		self.getScoutData();
	},
	template:
	'<div>' +
		'<h3 class="text-center">Data</h3>' +
		'<form class="form-horizontal" role="form">' +
			'<div class="form-group row">' +
				'<label class="col-lg-3 control-label">Autonomous Gear Position:</label>' +
				'<div class="col-lg-8">' +
					'<div class="ui-select">' +
						'<select class="form-control" v-model="auto_gear_position">' +
							'<option value="Left">Left</option>' +
							'<option value="Middle">Middle</option>' +
							'<option value="Right">Right</option>' +
							'<option value="None">None</option>' +
						'</select>' +
					'</div>' +
				'</div>' +
			'</div>' +
			'<div class="form-group row">' +
				'<label class="col-lg-3 control-label">Low Goal:</label>' +
				'<div class="col-lg-8">' +
					'<div class="ui-select">' +
						'<select class="form-control" v-model="low_goal">' +
							'<option value="-1">Bad</option>' +
							'<option value="0">Neutral</option>' +
							'<option value="1">Good</option>' +
						'</select>' +
					'</div>' +
				'</div>' +
			'</div>' +
			'<div class="form-group row">' +
				'<label class="col-lg-3 control-label">High Goal:</label>' +
				'<div class="col-lg-8">' +
					'<div class="ui-select">' +
						'<select class="form-control" v-model="high_goal">' +
							'<option value="-1">Bad</option>' +
							'<option value="0">Neutral</option>' +
							'<option value="1">Good</option>' +
						'</select>' +
					'</div>' +
				'</div>' +
			'</div>' +
			'<div class="form-group row">' +
				'<label class="col-lg-3 control-label">Gears:</label>' +
				'<div class="input-group col-lg-9">' +
					'<span class="input-group-btn">' +
						'<button class="btn btn-default" type="button" v-on:click="subtractGear"><span class="glyphicon glyphicon-minus"></span></button>' +
					'</span>' +
					'<input type="text" class="form-control col-xs-4" name="qty" v-model="gears">' +
					'<span class="input-group-btn">' +
						'<button class="btn btn-default" type="button" v-on:click="addGear"><span class="glyphicon glyphicon-plus"></span></button>' +
					'</span>' +
				'</div>' +
			'</div>' +
			'<div class="form-group row">' +
				'<label class="col-lg-3 control-label">Climbing Rating:</label>' +
				'<div class="col-lg-8">' +
					'<div class="ui-select">' +
						'<select class="form-control" v-model="climbing_rating">' +
							'<option value="1">Can\'t Climb</option>' +
							'<option value="2">Slow</option>' +
							'<option value="3">15 Seconds or Less</option>' +
							'<option value="4">Scared Cat (Almost Instant Climbing)</option>' +
						'</select>' +
					'</div>' +
				'</div>' +
			'</div>' +
		'</form>' +
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
			team_name: 'Loading Team Name',
			side: 'Loading Side'
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
