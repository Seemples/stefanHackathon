(function () {

	// Cache the document jQuery object.
	var $document = $(document);

	// Timer for preventing AJAX Spam.
	var timer;


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

	var date;
	var month;
	var year;

	var $date = $('#date');
	var $month = $('#month');
	var $year = $('#year');

	var today = new Date();
	$date.val(today.getDate());
	$month.val(today.getMonth() + 1);
	$year.val(today.getFullYear());


	$('#year').on('input', function () {

		var $self = $(this);
		year = $self.val();

		if (year > 2014) {			
			year = 2014;
			$self.val(year);
		} else if (year < 2013) {
			year = 2013;
			$self.val(year);			
		}
	});



	// Datepicker.

	$('#date').on('input', function () {

		var $self = $(this);
		date = $self.val();

		if (date > 31) {			
			date = 31;
			$self.val(date);
		} else if (date < 0) {
			date = 1;
			$self.val(date);
		}
	});

	$('#month').on('input', function () {

		var $self = $(this);
		month = $self.val();

		if (month > 12) {			
			month = 12;
			$self.val(month);
		} else if (month < 0) {
			month = 1;
			$self.val(month);			
		}
	});


})($);