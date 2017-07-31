var map;
var pos;

function getCoords(map){
	if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(function(position) {
			pos = {
				lat: position.coords.latitude,
				lng: position.coords.longitude
			};
			map.setCenter(pos);
			getLocation(pos);
			placeMarker(pos['lat'], pos['lng'], map);
			}, function() {
			handleLocationError(true, map.getCenter());
		});
	} 
	else {
		// Browser doesn't support Geolocation
		handleLocationError(false, map.getCenter());
	}
}

function getLocation(pos){
	$.ajax({
		url:'https://maps.googleapis.com/maps/api/geocode/json?latlng=' + pos['lat'] + ',' + pos['lng'] + '&key=AIzaSyD6JvfyfYbeSNIGmjjAVQ_94Aq63WYorhY',
		success:function(data){
			$('#lat').val(pos['lat']);
			$('#lng').val(pos['lng']);
			$('#city').val(data.results[3].formatted_address);
			console.log(pos['lat']);
			console.log(pos['lng']);
			console.log(data.results[3].formatted_address);
		}
	});
}

function addMarkers(location_data){
	var locations = []
	for (var things in location_data){
		locations[things] = new google.maps.Marker({
			position: {
				lat: parseFloat(location.latitude),
				lng: parseFloat(location.longitude)
			}
		})
		locations[things].setMap(map)
	}
}

$('#findplace').submit(function(form_data){
	form_data.preventDefault();
	console.log($(this).serialize())
	$.ajax({
		url:'/getall',
		method:'POST',
		data: $(this).serialize(),
		success: function(data) {
			$('#boba_append').html(' ')
			data = JSON.parse(data)
			addMarkers(data.businesses)
			for (var boba in data.businesses){
				var bobajson = {
					'latitude': data.businesses[boba].coordinates.latitude,
					'longitude': data.businesses[boba].coordinates.longitude,
					'name': data.businesses[boba].name,
				}
				$('#boba_append').append('<tr><td><a data-lat='+ bobajson.latitude +' data-lng=' + bobajson.longitude + ' herf="">'+ bobajson.name +'</a></td><td>' + createLocationForm(bobajson) + '</td></tr>')
				placeMarker(bobajson.latitude,bobajson.longitude, map)
			}
		}
	});
});
function createLocationForm(Json){
	var tr = document.createElement('tr');
	var form = document.createElement('form');
	var submit = document.createElement('input');
	$(submit).attr('class', 'join');
	$(submit).attr('type', 'submit');
	$(submit).attr('value', 'join');
	form.appendChild(submit);
	return form;
}

function placeMarker(latitude, longitude, map) {
    var marker = new google.maps.Marker({
        position: {
        	lat: latitude,
        	lng: longitude
        }, 
        map: map
    });
}

$(document).on('click', '#boba_places a', function(e){
	e.preventDefault();
	lats = $(this).attr('data-lat');
	lngs = $(this).attr('data-lng');
	console.log(lats, lngs);
	map.panTo({
		lat: parseFloat(lats) ,
		lng: parseFloat(lngs)
	});
});

function initMap(){
	var options = {
			zoom:15,
			center: {
				lat: 37.3875545,
				lng: -121.8828977
			}
		}
	map = new google.maps.Map(document.getElementById('map'), options);
	getCoords(map);
}