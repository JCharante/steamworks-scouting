function onceDocumentReady() {
	var scout_match = new Vue({
		el: '#vue-app',
		mounted: function () {
			var self = this;
			self.matches = JSON.parse(localStorage.getItem('matches') || '{}');
		},
		methods: {
			wipe_data: function() {
				var self = this;
				toast('info', 'Wiping Data.', 'ur a madlad');
				localStorage.setItem('matches', '{}');
				self.matches = JSON.parse(localStorage.getItem('matches') || '{}');
			}
		},
		computed: {
			matches_string: function() {
				var self = this;
				return JSON.stringify(self.matches)
			}
		},
		data: function() {
			var self = this;
			return {
				matches: {}
			}
		}
	})
}

$(document).ready(onceDocumentReady);
