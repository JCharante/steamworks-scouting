function onceDocumentReady() {
	if ((localStorage.getItem('scoutName') || '') === '') {
		alert('Please set your scout name in the settings page.');
		window.location.replace('../settings/index.html');
	}
}

$(document).ready(onceDocumentReady);
