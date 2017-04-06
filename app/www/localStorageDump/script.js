function onceDocumentReady() {
	var localStorageDump = new Vue({
		el: '#vue-app',
		mounted: function () {
			var self = this;
			self.matches = JSON.parse(localStorage.getItem('matches') || '{}');
			self.scoutName = localStorage.getItem('scoutName') || '';
			self.serverPassword = localStorage.getItem('serverPassword') || '';
		},
		methods: {
			wipe_data: function() {
				var self = this;
				toast('info', 'Wiping Data.', '');
				localStorage.setItem('matches', '{}');
				localStorage.setItem('scoutName', '');
				localStorage.setItem('serverPassword', '');
				self.matches = JSON.parse(localStorage.getItem('matches') || '{}');
				self.scoutName = localStorage.getItem('scoutName');
				self.serverPassword = localStorage.getItem('serverPassword');
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
				scoutName: '',
				serverPassword: ''
			}
		}
	})
}

$(document).ready(onceDocumentReady);
