(function () {

	var $document = $(document);

	var timer;	
	var $list = $('#list');
	var $suggestions;
	var sugLength = 0;
	var sugActive = -1;

	var $input = $('#input');
	var country = '';

	var $date = $('#date');
	var $month = $('#month');
	var $year = $('#year');
	var date;
	var month;
	var year;

	var today = new Date();
	var dd = today.getDate();
	var mm = today.getMonth() + 1; //January is 0!
	var yyyy = today.getFullYear();

	$date.val(dd);
	$month.val(mm);
	$year.val(yyyy);

	// Autosuggestions select.
	$document.keydown(function (e) {

		if ($input.is(':focus')) {
			// Checking for dufferent keys.			
			if (e.keyCode == 40 && (sugActive + 1) < sugLength) {
				
				$suggestions.removeClass('active');
		    	sugActive++;
		    	$suggestions.eq(sugActive).addClass('active');

	    	} else if (e.keyCode == 38 && sugActive) {

		    	$suggestions.removeClass('active');
		    	sugActive--;
		    	$suggestions.eq(sugActive).addClass('active');	    	
		    
		    } else if (e.keyCode == 13 ) {
	    	
	    		if (sugActive > -1) {
		    		console.log($suggestions.eq(sugActive).data('placeid') + ' ');
		    	}

		    	return false;

		    } // if (e.keyCode)
		} // if ($input.is)

	}); // $docuemnt.keydown()


	// On changing values.
	$input.on('input', function () {

		if (country = $input.val().trim()) {
			clearTimeout(timer);
			timer = setTimeout(suggest(country), 400);
		} else {
			$list.html('');
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

	function suggest(country) {
		$.getJSON('/api/country', {c: country }, function (data) {

			$list.html('');

			var sug = data.result;
			sugLength = sug.length;
			if (sugLength > 8) sugLength = 8;

			var c = data.c;			
			var i = 0;

			for (i; i < sugLength; i++) {
				var placeName = sug[i].PlaceName;
				var placeId = sug[i].PlaceId.replace('-sky', '');
				
				$list.append('<li class="sug-list-item" data-placeid="' + placeId + '">' + placeName + ', ' + placeId + '</li>');			
			}

			/** Attach new events */

			$suggestions = $list.find('li');

			$suggestions.on('click', function () {
				$suggestions.removeClass('active');
				var $self = $(this);
				$self.addClass('active');
				sugActive = $self.index();
			});
		
		});
	}


})($);