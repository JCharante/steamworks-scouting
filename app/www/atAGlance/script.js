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


Vue.component('matches', {
	props: ['team_number'],
	template:
	'<div class="row">' +
		'<match v-for="match in matches" :match="match" v-on:load-scouted-matches="loadScoutedMatches()"></match>' +
	'</div>',
	watch: {
		team_number: function(val, oldVal){
			var self = this;
			self.matches = [];

			var all_matches = JSON.parse(localStorage.getItem('matches') || '{}');

			for (var key in all_matches) {
				if(!all_matches.hasOwnProperty(key)) continue;

				var match = all_matches[key];

				if (match.team_number === self.team_number) {
					self.matches.push(match);
				}
			}
		}
	},
	data: function() {
		return {
			matches: []
		}
	}
});


function onceDocumentReady() {
	var app = new Vue({
		el: '#vue-app',
		mounted: function() {
			var self = this;
		},
		data: function () {
			return {
				team_number: null
			}
		}
	})
}

$(document).ready(onceDocumentReady);
