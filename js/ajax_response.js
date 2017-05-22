/**
 * Created by RacchanaK on 22/5/17.
 */
var url= "http://127.0.0.1:5000/bot/"+query;

$(document).ready(function(){
    $("#button").click(function(){
    	if($('#query').val()){
    	    var query=$('#query').val();
    	    query_response(query);
        }else{
            alert('please enter a query');
            $('#query').focus();
            return false;
        }
    });
});
function company_option(option){
    query_response(option);
}

function query_response(query){
        console.log(query);
        $.ajax({
            url: url,
            type:"GET",
            dataType: "json",
            contentType: "application/json; charset=utf-8",
            crossDomain: true,
            headers: {'Access-Control-Allow-Origin': '*'},
            success: function(data, textStatus, jqXHR){
                $('#result').append("<p><b> USER :  "+query+"</b></p>");
                $('#result').append(data.chatData)
                $('#result').append('<br/>');
                $('#query').val('');
            },
            error: function(jqXHR, exception) {
            if (jqXHR.status === 0) {
                alert('Not connect.\n Verify Network.');
            } else if (jqXHR.status == 404) {
                alert('Requested page not found. [404]');
            } else if (jqXHR.status == 500) {
                alert('Internal Server Error [500].');
            } else if (exception === 'parsererror') {
                alert('Requested JSON parse failed.');
            } else if (exception === 'timeout') {
                alert('Time out error.');
            } else if (exception === 'abort') {
                alert('Ajax request aborted.');
            } else {
                alert('Uncaught Error.\n' + jqXHR.responseText);
            }
        }
    });
}