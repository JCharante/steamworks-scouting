toastr.options = {
  "closeButton": false,
  "debug": false,
  "newestOnTop": false,
  "progressBar": false,
  "positionClass": "toast-top-left",
  "preventDuplicates": false,
  "onclick": null,
  "showDuration": "200",
  "hideDuration": "200",
  "timeOut": "2000",
  "extendedTimeOut": "5000",
  "showEasing": "swing",
  "hideEasing": "linear",
  "showMethod": "fadeIn",
  "hideMethod": "fadeOut"
}

function toast(occasion, title, body) {
	var type = null;
	switch (occasion) {
		case "info":
			type = "info";
			break;
		case "success":
			type = "success";
			break;
		case "error":
			type = "error";
			break;
		default:
			type = "info";
			break;
	}
	toastr[type](body, title);
}