Vue.component('event-row', {
	props: ['event_name', 'event_id'],
	mounted: function() {
		var self = this;
		console.log("Event Row: ", self.event_name, self.event_id);
	},
	computed: {
		eventPageLink: function() {
			var self = this;
			return '/app/events/event?event_id=' + self.event_id;
		}
	},
	methods: {
		deleteEvent: function() {
			var self = this;
			var confirm_result = confirm("You are about to delete the " + self.event_name + '. Are you sure? This cannot be undone!');
			if (confirm_result) {
				var event_id = self.event_id;

				var data = {
					event_id: event_id
				};

				$.ajax({
					method: 'POST',
					url: '/api/events/event/delete',
					data: JSON.stringify(data),
					dataType: "json",
					contentType: "application/json",
					statusCode: {
						200: function (data) {
							console.log('Server Replied: ', data);
							toastr["success"]("You mad lad!!", "Deleted Event.");
							self.$emit('event-deleted');
						},
						400: function (responseObject) {
							console.log('Server Replied: ', responseObject);
							var data = responseObject.responseJSON;
							toastr["error"](data.message, "Error Deleting Event");
						}
					}
				});
			}
		}
	},
	template:
	'<div class="col-lg-4 col-md-6 col-xs-12">' +
		'<div class="panel panel-default">' +
			'<div class="panel-heading">' +
				'<p>{{ event_name }}</p>' +
			'</div>' +
			'<div class="panel-body">' +
				'<a class="btn btn-primary" :href="eventPageLink" role="button">Event Page</a>' +
				' ' +
				'<a class="btn btn-danger" role="button" v-on:click="deleteEvent">Delete Event</a>' +
			'</div>' +
		'</div>' +
	'</div>'
});

Vue.component('events-list', {
	mounted: function() {
		var self = this;
		console.log("Events List: ", self.events);
	},
	methods: {
		eventDeleted: function() {
			var self = this;
			self.$emit('event-deleted');
		}
	},
	props: ['events'],
	template:
	'<div>' +
		'<event-row v-on:event-deleted="eventDeleted()" v-for="event in events" :event_name="event.event_name" :event_id="event.event_id"></event-row>' +
	'</div>'
});

Vue.component('events-page', {
	delimiters: ['[[', ']]'],
	mounted: function() {
		var self = this;

		self.fetchData();
	},
	methods: {
		fetchData: function() {
			var self = this;

			$.ajax({
				method: 'GET',
				url: '/api/events/all',
				contentType: 'application/json',
				statusCode: {
					200: function (data) {
						self.$data.events = data.events;
						console.log("Events Page: ", self.$data.events);
					}
				}
			})
		}
	},
	template:
	'<div class="row">' +
		'<h1 class="text-center">Events</h1>' +
		'<events-list v-on:event-deleted="fetchData()" :events="events"></events-list>' +
	'</div>',
	data: function () {
		return {
			events: []
		}
	}
});

function onceDocumentReady() {
	var eventsPage = new Vue({
		el: '#vue-app',
		template: '<events-page></events-page>'
	});
}

$(document).ready(onceDocumentReady);
