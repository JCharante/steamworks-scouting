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
	template:
	'<div class="panel panel-default">' +
		'<div class="panel-heading">' +
			'<p>{{ event_name }}</p>' +
		'</div>' +
		'<div class="panel-body">' +
			'<a :href="eventPageLink"><p>Event Page</p></a>' +
		'</div>' +
	'</div>'
});

Vue.component('events-list', {
	mounted: function() {
		var self = this;
		console.log("Events List: ", self.events);
	},
	props: ['events'],
	template:
	'<div>' +
		'<event-row v-for="event in events" :event_name="event.event_name" :event_id="event.event_id"></event-row>' +
	'</div>'
});

Vue.component('events-page', {
	delimiters: ['[[', ']]'],
	mounted: function() {
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
	},
	template:
	'<div class="row">' +
		'<h1 class="text-center">Events</h1>' +
		'<events-list :events="events"></events-list>' +
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
