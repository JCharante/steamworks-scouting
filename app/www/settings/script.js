function onceDocumentReady() {
	var scouted_matches = new Vue({
		el: '#vue-app',
		mounted: function () {
			var self = this;
			self.loadSavedData();
		},
		methods: {
			save: function() {
				var self = this;
				if (!(/\S/.test(self.scoutName))) {
					toast('error', 'Didn\'t Save', 'Scout name cannot be Blank');
					playFieldFault();
					return null;
				}

				localStorage.setItem('scoutName', self.scoutName);
				localStorage.setItem('serverPassword', self.serverPassword);
				localStorage.setItem('preferences', JSON.stringify(self.preferences));
				toast('success', 'Saved Changes', '');
			},
			loadSavedData: function() {
				var self = this;
				self.scoutName = localStorage.getItem('scoutName') || '';
				self.serverPassword = localStorage.getItem('serverPassword') || '';
				self.preferences = JSON.parse(localStorage.getItem('preferences') || '{}');
			}
		},
		data: function () {
			return {
				scoutName: '',
				serverPassword: '',
				preferences: {}
			}
		}
	});
}

$(document).ready(onceDocumentReady);