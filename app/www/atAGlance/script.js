Vue.component('match', {
	props: ['match'],
	methods: {
		viewQrCode: function() {
			var self = this;
			var packed_json_string = JSONC.pack(self.match);
			cordova.plugins.barcodeScanner.encode(cordova.plugins.barcodeScanner.Encode.TEXT_TYPE, packed_json_string, function(success) {
					console.log(success);
				}, function(fail) {
					toast('error', 'Error', 'Generating QR Code Failed');
					console.log(fail);
				}
			);
		},
		deleteMatch: function() {
			var self = this;
			if (confirm("You sure you want to delete " + self.eventName + ' - ' + self.match.match_number)){
				var matches = JSON.parse(localStorage.getItem('matches') || '{}');
				delete matches[self.match.match_id];
				localStorage.setItem('matches', JSON.stringify(matches));
				self.$emit('load-scouted-matches');
			}
		}
	},
	computed: {
		linkToMatch: function() {
			var self = this;
			return '../scout_match/index.html?match_id=' + self.match.match_id;
		},
		eventName: function() {
			var self = this;
			var name = null;
			switch (self.match.event_name) {
				case 'greater-boston':
					name = 'Greater Boston';
					break;
				case 'pine-tree':
					name = 'Pine Tree';
					break;
				case 'practice':
					name = 'Practice';
					break;
				default:
					name = self.match.event_name;
					break;
			}
			return name;
		}
	},
	template:
	'<div class="col-lg4 col-md-6 col-xs-12">' +
		'<div class="panel panel-default">' +
			'<div class="panel-heading">' +
				'<p>{{ eventName }} - Q{{ match.match_number }} - {{ match.team_number }}</p>' +
			'</div>' +
			'<div class="panel-body">' +
				'<a class="btn btn-primary" :href="linkToMatch" role="button">Edit / View Match</a> ' +
				'<a class="btn btn-default" v-on:click="viewQrCode" role="button">View QR Code</a> ' +
				'<hr>' +
				'<a class="btn btn-danger" v-on:click="deleteMatch" role="button">Delete Match</a>' +
			'</div>' +
		'</div>' +
	'</div>'
});


function onceDocumentReady() {
	var app = new Vue({
		el: '#vue-app',
		mounted: function() {
			var self = this;
		},
		methods: {
			loadMatches: function() {
				var self = this;
				self.matches = [];

				var all_matches = JSON.parse(localStorage.getItem('matches') || '{}');

				for (var key in all_matches) {
					if(!all_matches.hasOwnProperty(key)) continue;

					var match = all_matches[key];

					if (match.team_number === self.team_number && match.event_name != 'practice') {
						self.matches.push(match);
					}
				}
			},
			calculateStats: function() {

			}
		},
		watch: {
			team_number: function(val, oldVal){
				var self = this;
				self.loadMatches();
				self.calculateStats();

				var currentEvent = 'pine-tree';  // TODO: Make this an option in the settings page.

				var totalAutokPa = 0;
				var totalTotalkPa = 0;
				var totalGears = 0;
				var matches = 0;

				for (var i = 0; i < self.matches.length; i++) {
					var match = self.matches[i];

					if (match.event_name != 'practice') {
						matches += 1;
						totalAutokPa += match.auto_kpa;
						totalTotalkPa += match.total_kpa;
						totalGears += match.total_gears;

						if (match.collected_fuel_from_floor) {
							self.can_pickup_fuel_from_floor = true;
						}

						if (match.got_gear_from_floor) {
							self.can_pickup_gears_from_floor = true;
						}
					}
				}

				self.averageAutokPa = (totalAutokPa / matches) || 0;
				self.averageTotalkPa = (totalTotalkPa / matches) || 0;
				self.averageGears = (totalGears / matches) || 0;
			}
		},
		data: function () {
			return {
				team_number: null,
				matches: [],
				can_pickup_fuel_from_floor: false,
				can_pickup_gears_from_floor: false,
				averageAutokPa: 0,
				averageTotalkPa: 0,
				averageGears: 0
			}
		}
	})
}

$(document).ready(onceDocumentReady);
