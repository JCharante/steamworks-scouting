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
	if ((localStorage.getItem('scoutName') || '') === '') {
		alert('Please set your name in the settings page.');
		window.location.replace('../settings/index.html');
	}

	var scouted_matches = new Vue({
		el: '#vue-app',
		mounted: function() {
			var self = this;
			self.loadScoutedMatches();
		},
		methods: {
			loadScoutedMatches: function() {
				var self = this;
				var all_matches = JSON.parse(localStorage.getItem('matches') || '{}');
				var scout_name = localStorage.getItem('scoutName');
				for (var i = 0; i < all_matches.length; i++) {
					var match = all_matches[i];
					if (match.scout_name == scout_name) {
						self.scoutedMatches[match.match_id] = match;
					}
				}

			}
		},
		data: function () {
			return {
				scoutedMatches: {}
			}
		}
	})
}

$(document).ready(onceDocumentReady);