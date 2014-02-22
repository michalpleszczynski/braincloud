$(document).ready(function(){
    $("input#query").keyup(function(){
        var query = $(this).val();

        if(query.length<=3){
            $("#searchresults").remove();
        }else{

            if ( $("#searchresults").length ==0 ) {
                 $('<div id="searchresults"></div>').appendTo('#search_content');
            }

            dataString = 'q=' + query;
            $.ajax({
                type: "POST",
                url: "http://127.0.0.1:8000/api/v1/livesearch/",
                data: dataString,
                beforeSend: function() {
                    $('input#query').addClass('loading');
                },
                success: function(response){
                    $('#searchresults').empty()
                    for (var i in response.thoughts){
                        $('#searchresults').append('<p><a href="http://127.0.0.1:8000/view_thought/' + response.thoughts[i].id + '">' + response.thoughts[i].title + '</a></p>');
                    }
                    $('#searchresults').show();
                }
            });
        }
    });
});