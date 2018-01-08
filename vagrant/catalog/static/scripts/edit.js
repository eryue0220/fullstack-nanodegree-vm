var $form = $('#upgrade-form');

function validation() {
	return false;
}

function submit() {
	$form.attr('method', 'POST');
}

function init() {
	$form.submit(function() {
		return false;
	});
}

init();
