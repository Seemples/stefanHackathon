(function () {

	var $document = $(document);
	
	var $list = $('#list');
	var $suggestions = $list.find('li');
	var timer;
	var sugLength = 0;
	var sugActive = -1;

	var $input = $('#input');
	var country;

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

	// Down key.
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
		    		alert($suggestions.eq(sugActive).data('placeid') + ' ');
		    	}

		    	return false;

		    } // if (e.keyCode)

		} // if ($input.is)

	}); // $docuemnt.keydown()


	// On changing values.
	$input.on('input', function () {

		if ($input.val().trim()) {

			clearTimeout(timer);
			timer = setTimeout(suggest, 400);

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

	function suggest() {
		$.getJSON('/api/country', {c: $input.val().trim() }, function (data) {

			var c = data.c;			
			var sug = data.result.Places;

			//$input.val(sug[0].PlaceName);
			//console.log(c);

			sugLength = sug.length;
			if (sugLength > 8) sugLength = 5;
			console.log(sugLength);

			$list.html('');
			var i = 0;

			for (i; i < sugLength; i++) {

				var name = sug[i].PlaceName;
				var placeId = sug[i].PlaceId;
				placeId = sug[i].PlaceId = placeId.replace('-sky', '');
				
				$list.append('<li class="sug-list-item" data-placeid="' + placeId + '">' + sug[i].PlaceName + ', ' + placeId + '</li>');
			
			}

			$suggestions = $list.find('li');

			$suggestions.on('click', function () {

				console.log('clicked');

				var $self = $(this);

				$suggestions.removeClass('active');
				$self.addClass('active');

				sugActive = $self.index();
				
				alert($self.data('placeid'));

			});
		
		});
	}


})($);