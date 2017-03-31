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
				'<a class="navbar-brand" href="../home/index.html">achilles</a>' +
			'</div>' +

			'<!-- Collect the nav links, forms, and other content for toggling -->' +
			'<div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">' +
				'<ul class="nav navbar-nav">' +
					'<li><a href="../home/index.html">Home</a></li>' +
					'<li><a href="../settings/index.html">Settings</a></li>' +
					'<li><a href="../fun/index.html">Sounds</a></li>' +
					'<li><a href="../atAGlance/index.html">At a Glance</a></li>' +

					'<li class="dropdown">' +
					'<a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Match <span class="caret"></span></a>' +
						'<ul class="dropdown-menu">' +
							'<li><a href="../scout_match/index.html">Scout</a></li>' +
							'<li><a href="../scoutedMatches/index.html">View</a></li>' +
							'<li><a href="../scanMatch/index.html">Scan</a></li>' +
						'</ul>' +
					'</li>' +

					'<li class="dropdown">' +
					'<a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Server <span class="caret"></span></a>' +
						'<ul class="dropdown-menu">' +
							'<li><a href="../uploadToServer/index.html">Upload Data</a></li>' +
							'<li><a href="#">Download Data</a></li>' +
						'</ul>' +
					'</li>' +

					'<li class="dropdown">' +
					'<a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Developer <span class="caret"></span></a>' +
						'<ul class="dropdown-menu">' +
							'<li><a href="../localStorageDump/index.html">Local Storage Dump</a></li>' +
							'<li><a href="../compressionTest/index.html">Compression Test</a></li>' +
						'</ul>' +
					'</li>' +
				'</ul>' +
			'</div><!-- /.navbar-collapse -->' +
		'</div><!-- /.container-fluid -->' +
	'</nav>'
});

var navbar = new Vue({
	el: '#achilles-navbar',
	template: '<achilles-navbar></achilles-navbar>'
});