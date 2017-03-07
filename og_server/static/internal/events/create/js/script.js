function onceDocumentReady() {
	startSubmitButtonListener();
}


function startSubmitButtonListener() {
	$('#create-event').click(function () {
		var event_name = $('#event-name').val();
		var data = {
			event_name: event_name
		};

		$.ajax({
			method: 'POST',
			url: '/api/events/create',
			data: JSON.stringify(data),
			dataType: "json",
			contentType: "application/json",
			statusCode: {
				200: function (data) {
					console.log('Server Replied: ', data);
					toastr["success"]("", "Created Event")
				},
				400: function (responseObject) {
					console.log('Server Replied: ', responseObject);
					var data = responseObject.responseJSON;
					toastr["error"](data.message, "Error Creating Event");
				}
			}
		});
	});
}

$(document).ready(onceDocumentReady);
