function onceDocumentReady() {
	var scout_match = new Vue({
		el: '#vue-app',
		mounted: function () {
			var self = this;
			self.matches = JSON.parse(localStorage.getItem('matches') || '{}');
			self.scoutName = localStorage.getItem('scoutName') || '';
		},
		methods: {
			wipe_data: function() {
				var self = this;
				toast('info', 'Wiping Data.', '');
				localStorage.setItem('matches', '{}');
				localStorage.setItem('scoutName', '');
				self.matches = JSON.parse(localStorage.getItem('matches') || '{}');
				self.scoutName = localStorage.getItem('scoutName')
			}
		},
		computed: {
			matches_string: function() {
				var self = this;
				return JSON.stringify(self.matches)
			},
			scoutName: function() {
				var self = this;
				return self.scoutName;
			}
		},
		data: function() {
			var self = this;
			return {
				matches: {},
				scoutName: ''
			}
		}
	})
}

$(document).ready(onceDocumentReady);
