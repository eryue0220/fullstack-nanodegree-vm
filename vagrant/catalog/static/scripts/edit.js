var $form = $('#upgrade-form');
var $item = $('#item');
var $catalogName = $('#catalog-name')
var $catalogDesc = $('#catalog-desc');
var $errorArea = $('.error-area');
var originItemValue = $item.val();
var originCatalogDesc = $catalogDesc.val();
var originCatalogName = $catalogName.find('option:selected').val();

function isValueEmpty($node) {
	return $node.val() === '';
}

function showErrorTip(error) {
	removeErrorTip();
	$errorArea.append(
		'<h4 class="text-danger">' + error + '</h4>'
	);
}

function removeErrorTip() {
	var $errorText = $errorArea.find('.text-danger');

	if ($errorText.length) {
		$errorText.remove();
	}
}

function validation() {
	if (
		isValueEmpty($item) ||
		isValueEmpty($catalogName) ||
		isValueEmpty($catalogDesc)
	) {
		showErrorTip('Input value should not be empty');
		return false;
	}

	var selectedValue = $catalogName.find('option:selected').val().toLowerCase();

	if (
		$item.val() === originItemValue &&
		originCatalogName.toLowerCase() === selectedValue &&
		$catalogDesc.val() === originCatalogDesc
	) {
		showErrorTip('The value same as Before that no need to submit.');
		return false
	}

	removeErrorTip();
	return true;
}

function init() {
	$form.submit(function() {
		return validation();
	});
}

init();
