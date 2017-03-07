function onceDocumentReady() {
	startSubmitButtonListener();
}


function startSubmitButtonListener() {
	$('#create-team').click(function () {
		var team_name = $('#team-name').val();
		var team_number = $('#team-number').val();
		var data = {
			team_name: team_name,
			team_number: team_number
		};

		$.ajax({
			method: 'POST',
			url: '/api/teams/create',
			data: JSON.stringify(data),
			dataType: "json",
			contentType: "application/json",
			statusCode: {
				200: function (data) {
					console.log('Server Replied: ', data);
					$('#team-name').val('');
					$('#team-number').val('');
					toastr["success"]("", "Created Team")
				},
				400: function (responseObject) {
					console.log('Server Replied: ', responseObject);
					var data = responseObject.responseJSON;
					toastr["error"](data.message, "Error Creating Team");
				}
			}
		});
	});
}

$(document).ready(onceDocumentReady);
