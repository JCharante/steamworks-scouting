function OnceDocumentReady() {
	var scouted_matches = new Vue({
		el: '#vue-app',
		data: function () {
			return {

			}
		}
	})
}

$(document).ready(onceDocumentReady());