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