function onceDocumentReady() {
	var fun = new Vue({
		el: '#vue-app',
		methods: {
			playSound: function(soundFile) {
				var audio = new Audio('../static/external/media/' + soundFile);
				audio.play();
				return null;
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
