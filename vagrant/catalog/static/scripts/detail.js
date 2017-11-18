var $main = $('#side-cotent');
var $deleteBtn = $('.delete_btn');

function fetchDeleteItem(evt) {
	var item = $(evt).attr('data-item');
	var url = '/api/v1/catalog/' + item + '/delete';

	$.ajax({
		type: 'get',
		url: url,
		success: function(res) {
			if (res && res.status === 0) {
				location.href = '/'
			}
		}
	});
}

function unbindModalEvent() {
	$main
		.off('click.sure')
		.off('click.cancel');
}

function bindModalEvent() {
	$main
		// sure
		.on('click.sure', '.sure', function(e) {
			fetchDeleteItem(e.target);
			removeModal();
			unbindModalEvent();
		})
		// cancel
		.on('click.cancel', '.cancel', function() {
			removeModal();
			unbindModalEvent();
		});
}

function appendModal(item) {
	$main.append(
		'<div class="modal-container">' +
		'<div class="modal-mask"></div>' +
		'<div class="content">' +
		'<div class="modal-title">' +
		'<h4>Are you sure to delete <b>' + item + '</b>? </h4>' +
		'</div>' +
		'<div class="modal-option">' +
		'<button data-item="' + item + '" class="btn btn-danger sure" role="button">Yes</button>' +
		'<button class="btn btn-default cancel" role="button">Cancel</button>' +
		'</div>' +
		'</div>' +
		'</div>'
	);

	bindModalEvent();
}

function removeModal() {
	$('.modal-container').remove();
}

function deleteItem() {
	$deleteBtn.on('click', function(e) {
		var item = $(e.target).attr('data-item')
		appendModal(item);
	});
}

deleteItem();
