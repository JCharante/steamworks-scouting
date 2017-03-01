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
		'<create-match v-on:match-creation="fetch_details()"></create-match>' +
		'<hr>' +
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
