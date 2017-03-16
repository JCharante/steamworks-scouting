Vue.component('achilles-navbar', {
	template:
	'<nav class="navbar navbar-default">' +
		'<div class="container-fluid">' +
			'<!-- Brand and toggle get grouped for better mobile display -->' +
			'<div class="navbar-header">' +
				'<button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">' +
					'<span class="sr-only">Toggle navigation</span>' +
					'<span class="icon-bar"></span>' +
					'<span class="icon-bar"></span>' +
					'<span class="icon-bar"></span>' +
				'</button>' +
				'<a class="navbar-brand" href="">achilles</a>' +
			'</div>' +

			'<!-- Collect the nav links, forms, and other content for toggling -->' +
			'<div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">' +
				'<ul class="nav navbar-nav">' +
					'<li><a href="../home/index.html">Home</a></li>' +
					'<li><a href="../qr_scan_demo/index.html">QR Scan Demo</a></li>' +
					'<li><a href="../scout_match/index.html">Scout Match</a></li>' +
					'<li><a href="../localStorageDump/index.html">Local Storage Dump</a></li>' +
					'<li><a href="../compressionTest/index.html">Compression Test</a></li>' +
					'<li><a href="../scoutedMatches/index.html">Scouted Matches</a></li>' +
				'</ul>' +
			'</div><!-- /.navbar-collapse -->' +
		'</div><!-- /.container-fluid -->' +
	'</nav>'
});

var navbar = new Vue({
	el: '#achilles-navbar',
	template: '<achilles-navbar></achilles-navbar>'
});