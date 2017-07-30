$('form').submit(function(e){
	e.preventDefault();
	$.ajax({
		url: '/search',
		method: 'POST',
		data: $(this).serialize(),
		success:function(search){
			if (search == "None Found"){
				$('#search_results').html("<p>None Found</p>")
			}
			else{
				search = JSON.stringify(search);
				search = JSON.parse(search);
				console.log(search)
				for (person in search){
					$('#search_results').append('<form action=/add_friend/'+search[person]['pk']+'><p>' + search[person]['fields']['name'] + '<input type="submit" value="add friend"></input></p></form>');
				}
			}
		}
	})
});