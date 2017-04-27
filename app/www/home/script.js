function onceDocumentReady() {
	if ((localStorage.getItem('scoutName') || '') === '') {
		/*
		setTimeout is here because while cordova.js loads before this script does,
		cordova_plugins.js does not, and therefor the toast feature isn't available yet.
		 */
		setTimeout(function() {
			window.plugins.toast.showWithOptions({
				message: 'Set your scout name under the settings page',
				duration: 'short',
				position: 'bottom',
				styling: {
					backgroundColor: toastColors.error
				}
			}, function(result) {
				if (result && result.event) {
					if (result.event === 'hide' || result.event === 'touch') {
						window.location.replace('../settings/index.html');
			        }
				}
			});
		}, 1000);
	}
}

$(document).ready(onceDocumentReady);
