/*
* Search.js
* This is for menu bar search result
*/

$(function(){
	var url = $('#typeahead').attr('data-url');
	// var url2 = $('#typeahead').attr('data-url2');
	// var url3 = $('#typeahead').attr('data-url3');
	// console.log(url);
	// var usr_url = $('#typeahead').attr('usr-url');

	var nyse_stocks = new Bloodhound({
		datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
		queryTokenizer: Bloodhound.tokenizers.whitespace,
		limit: 5,
		prefetch: {
			url: url,
			ttl : 500,
  		}
	});

	// var my_choice = new Bloodhound({
	// 	datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
	// 	queryTokenizer: Bloodhound.tokenizers.whitespace,
	// 	  limit: 5,
	// 	  prefetch: {
	// 		  url: url3,
	// 		  ttl : 500,
	// 		}
	//   });	
	  


	nyse_stocks.initialize();
	// my_choice.initialize();

	$('#search #typeahead').typeahead({
			highlight : true
		},
		{
			name: 'nyse_stocks',
			displayKey: 'name',
			source: nyse_stocks.ttAdapter(),
			templates: {
			    header: '<p class="league-name">Stocks Name</p>',
			    suggestion: Handlebars.compile('<p class="sugg-title"><strong>{{name}} - {{slug}}</strong></p>'),
			    // empty: '<p><a href="/quote/add/" class="empty-search"></a></p>'
			}
		},

		// {
		// 	name: 'my_choice',
		// 	displayKey: 'name',
		// 	source: my_choice.ttAdapter(),
		// 	templates: {
		// 		header: '<p class="league-name" style="color:#97c950">Our Choices</p>',
		// 		suggestion: Handlebars.compile('<p class="sugg-title"><strong>{{name}} - {{slug}}</strong></p>'),
		// 	}
		// }
		);

	$('.typeahead').on('typeahead:selected', function (e, datum) {
		console.log(datum);
		window.location.href = '/search/' + datum.se + '/' + datum.slug + '/';
	});

});