$(document).ready(function(){

    $("#query").autocomplete({
        source: [],
        select: function( event, ui ) {
            event.preventDefault();
            $("#query").val(ui.item.label);
            window.location.href = ui.item.value;
        },
        focus: function( event, ui ) {
            event.preventDefault();
            $("#query").val(ui.item.label);
        },
        minLength: 3,
    });

    $("input#query").keyup(function(){
        var query = $(this).val();

        if(query.length>3){
            dataString = 'q=' + query;
            $.ajax({
                type: "POST",
                url: "http://127.0.0.1:8000/api/v1/livesearch/",
                data: dataString,
                success: function(response){
                    var availableHints = [];
                    for (var i in response.thoughts){
                        availableHints.push({
                            value: "http://127.0.0.1:8000/view_thought/" + response.thoughts[i].id,
                            label: response.thoughts[i].title
                        });
                    }
                    $("#query").autocomplete({
                        source: availableHints,
                    });
                }
            });
        }
    });

});