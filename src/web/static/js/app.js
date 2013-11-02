(function () {

	function isInt(n) {
		return n % 1 === 0;
	}

	// Cache the document jQuery object.
	var $document = $(document);

	// Timer for preventing AJAX Spam.
	var timer;

	// Caching the suggestion variables.
	var $list = $('#list');
	var $suggestions;
	var sugActive = -1;


	var $input = $('#input');
	var country = '';

	// Clear the list.
	function clearList() {
		$list.html('');
		$suggestions = [];
		sugActive = -1;
	}

	// Complete the input using the autocomplete.
	function complete(n) {
		$suggestions.removeClass('active');

		var $suggestion = $suggestions.eq(sugActive = n);
		$suggestion.addClass('active');
		$input.val($suggestion.html());

		country = $suggestion.data('placeid');
	}

	// Autocomplete suggestions.
	function suggest(country) {
		$.getJSON('/api/country', {c: country }, function (data) {

			clearList();

			var sug = data.result;
			var sugLength = sug.length;
			if (sugLength > 8) sugLength = 8;

			for (var i = 0; i < sugLength; i++) {
				
				var placeName = sug[i].PlaceName;
				var placeId = sug[i].PlaceId.replace('-sky', '');
				
				$list.append('<li class="sug-list-item" data-placeid="' + placeId + '">' + placeName + ', ' + placeId + '</li>');			
			}

			/** Attach new events */

			$suggestions = $list.find('li');

			$suggestions.on('click', function () {
				var $self = $(this);
				complete($self.index());
				clearList();
			});
		
		});
	}

	// Autosuggestions select.
	$document.keydown(function (e) {

		if ($input.is(':focus')) {
		
			if (e.keyCode == 40 && (sugActive + 1) < $suggestions.length) {				
		    	complete(sugActive + 1);
	    	} else if (e.keyCode == 38 && sugActive) {
		    	complete(sugActive - 1);		    
		    } else if (e.keyCode == 13) {
		    	if (sugActive > -1) clearList();
		    	return false;
		    } // if (e.keyCode)

		} // if ($input.is)

	}); // $docuemnt.keydown()

	// On input blur.
	$input.on('input', function () {
		if ($input.val().trim()) {
			clearTimeout(timer);
			timer = setTimeout(suggest($input.val().trim()), 600);
		} else clearList();
	});

	/*$('#select').on('click', function () {
		country = $suggestions.eq(sugActive).data('placeid');
		console.log(country);
	});*/



	//////////////////////////////////////////////////////
	//                   DATES                          //
	//////////////////////////////////////////////////////

	var $date = $('#date');
	var $month = $('#month');
	var $year = $('#year');

	var today = new Date();
	$date.val(today.getDate());
	$month.val(today.getMonth() + 1);
	$year.val(today.getFullYear());


	$year.on('blur', function () {
		var $self = $(this);		
		value = $self.val();

		if (value > 2014) value = 2014;
		else if (value < 2013) value = 2013;
		$self.val(value);
	});

	$date.on('blur', function () {
		var $self = $(this);		
		value = $self.val();

		if (value > 31) value = 31;
		else if (value < 0) value = 1;
		$self.val(value);
	});

	$month.on('blur', function () {
		var $self = $(this);		
		value = $self.val();

		if (value > 12) value = 12;
		else if (value < 0) value = 1;
		$self.val(value);
	});


	//////////////////////////////////////////////////////
	//                   BUDGET                         //
	//////////////////////////////////////////////////////

	var $budget = $('#budget');

	$budget.on('blur', function () {
		var $self = $(this);		
		value = $self.val();

		if (value > 50000) value = 50000;
		else if (value < 50) value = 50;
		$self.val(value);
	});


	//////////////////////////////////////////////////////
	//                   SUBMIT                         //
	//////////////////////////////////////////////////////

	var $submit = $('#submit');

	$submit.click(function () {


		var budget = $budget.val().trim();

		var date = $date.val().trim();
		var month = $month.val().trim();
		var year = $year.val().trim();

		if (!isInt(budget) || !isInt(date) || !isInt(month) || !isInt(year)) {
			alert('Incorrect values entered!');
			return;
		}

		if (date && date < 10) date = '0' + date;
		if (month && month < 10) month = '0' + month;

		if (!year || !budget || !country) {
			alert('All fiels should be filled.');
			return;
		}

		if (month) {
			year += '-' + month;
			if (date) year += '-' + date;
		}

		console.log(year);

	});

})($);