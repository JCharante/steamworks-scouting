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
					window.plugins.toast.showWithOptions({
						message: 'Scout name cannot be blank',
						duration: 'short',
						position: 'bottom',
						styling: {
							backgroundColor: toastColors.error
						}
					});
					playFieldFault();
					return null;
				}

				localStorage.setItem('scoutName', self.scoutName);
				localStorage.setItem('serverPassword', self.serverPassword);
				localStorage.setItem('preferences', JSON.stringify(self.preferences));

				window.plugins.toast.showWithOptions({
					message: 'Saved Settings',
					duration: 'short',
					position: 'bottom',
					styling: {
						backgroundColor: toastColors.success
					}
				});
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