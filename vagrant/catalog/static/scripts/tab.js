function tabChange() {
	var $listItem = $('.tab-header__list-item');
	var $tabContent = $('.tab-content__item');

	$listItem.on('click', function(e) {
		var $target = $(e.target)
		$listItem.removeClass('active');
		$target.addClass('active');
		$tabContent.removeClass('active')
		$tabContent.eq($target.attr('data-index') - 1).addClass('active')
	});
}

tabChange();
