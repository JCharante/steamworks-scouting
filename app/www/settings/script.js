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
				if (self.scoutName === '' || !self.scoutName) {
					toast('error', 'Didn\'t Save', 'Invalid Scout Name');
					playFieldFault();
					return null;
				}

				localStorage.setItem('scoutName', self.scoutName);
				toast('success', 'Saved Changes', '');
			},
			loadSavedData: function() {
				var self = this;
				self.scoutName = localStorage.getItem('scoutName') || '';
			}
		},
		data: function () {
			return {
				scoutName: ''
			}
		}
	});
}

$(document).ready(onceDocumentReady);