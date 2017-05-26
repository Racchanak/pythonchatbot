/**
 * Created by RacchanaK on 22/5/17.
 */
var url= "http://127.0.0.1:5000/bot/";

$(document).ready(function(){
   $('.chat-boximg').click(function(){
       $(".chatbot-holder").toggle();
       var query='ACT';
       query_response(query);
   });
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
function cjoption(option){
    query_response(option);
}

function query_response(query) {
    $.ajax({
        url: url + query,
        type: "GET",
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        crossDomain: true,
        headers: {'Access-Control-Allow-Origin': '*'},
        success: function (data, textStatus, jqXHR) {
            $ques_html = '<div class="quest">' +
                            '<div class="quescontent">' +
                                '<p>'+ query +'</p>' +
                            '</div>' +
                            '<img src="../static/images/chat/ques.png" alt="image">' +
                          '</div>';

            $('#result').append($ques_html);

            $ans_html = '<div class="scroll answer">' +
                            '<img src="../static/images/chat/answ.png" alt="image">' +
                            '<div class="anscontent">' +
                                data.chatData +
                            '</div>' +
                          '</div>';

            $('#result').append($ans_html);
            var x = $('.anscontent').height();
            $('body').on('click', '.scroll', function() {
                $('.chatbox-content').animate({scrollTop: '+='+x}, 800);
            });
            $('#query').val('');
        },
        error: function (jqXHR, exception) {
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