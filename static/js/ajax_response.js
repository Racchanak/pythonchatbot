/**
 * Created by RacchanaK on 22/5/17.
 */
const BASE_URL = 'https://chatbot.wow.jobs';
var url= BASE_URL+"/bot/";
var query = $.cookie("c_wow_name");
query = query.replace(/[^a-zA-Z0-9 ]/g, '');
var welcome_msg = ['<p>Hello, How are you?</p>54675','<p>Welcome to the World of '+query.toUpperCase()+'</p>54675',query.toUpperCase()]
var i=0;
if(i==0){
    response_generate(welcome_msg[i],i,'');
}
function cjoption(option){
    query_response(option);
}
$("#button").click(function(){
    if($('#query').val()){
        var query=$('#query').val();
        if(i==1) {
            response_generate(welcome_msg[i], i, query);
        } else {
            query_response(query);
        }
    }else{
        alert('please enter a query');
        $('#query').focus();
        return false;
    }
});
function query_response(query) {
    $.ajax({
        url: url + query,
        type: "GET",
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        crossDomain: true,
        headers: {'Access-Control-Allow-Origin': '*'},
        success: function (data, textStatus, jqXHR) {
            $ans_html = '<div class="scroll answer">' +
                            '<img src= '+BASE_URL+'"/static/images/chat/answ.png" alt="image">' +
                            '<div class="anscontent" id="ans_'+clid+'">' +
                                data.chatData +
                            '</div>' +
                        '</div>';
            var clid = (i++);
            $ques_html = '<div class="quest">' +
                            '<div class="quescontent">' +
                                '<p class="p_' + clid + '">' +query  + '</p>' +
                            '</div>' +
                            '<img src="'+BASE_URL+'static/images/chat/ques.png" alt="image">' +
                        '</div>';
            $('#result').append($ques_html);
            $('#result').append($ans_html);
            var x = $('#ans_'+clid).height();
            var xy= 6;
            var finalX = x - xy +"px";
            $('#ans_'+clid).css('max-height',finalX);
            $('#ans_'+clid).css('overflow','hidden');
            $('body').on('click', '.scroll', function() {
                $('.chatbox-content').animate({scrollTop: "+="+x});
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
function response_generate(data,k,query){
    console.log(query);
    if(k==2) {
        query_response(welcome_msg[k]);
    }
    var clid = k;
    if(query!='') {
       $ques_html = '<div class="quest">' +
                        '<div class="quescontent">' +
                            '<p class="p_' + clid + '">' +query  + '</p>' +
                        '</div>' +
                        '<img src="'+BASE_URL+'/static/images/chat/ques.png" alt="image">' +
                    '</div>';
        $('#result').append($ques_html);
    }
    $ans_html = '<div class="scroll answer">' +
                    '<img src="'+BASE_URL+'/static/images/chat/answ.png" alt="image">' +
                    '<div class="anscontent"  id="ans_'+clid+'">' +
                        data +
                    '</div>' +
                '</div>';
    $('#result').append($ans_html);
    var x = $('#ans_'+clid).height();
    var xy= 6;
    var finalX = x - xy +"px";
    $('#ans_'+clid).css('max-height',finalX);
    $('#ans_'+clid).css('overflow','hidden');
    $('body').on('click', '.scroll', function() {
        $('.chatbox-content').animate({scrollTop: "+="+x});
    });
    $('#query').val('');
    i++;
}
//  var b = 2;
   // $('.chat-boximg').click(function(){
   //     $(".chatbot-holder").toggle();
   //     console.log('sadasd');
   //     if(b%2==0) {
   //         $('.chatbox-content').animate({scrollTop: ($('.chatbox-content')[0].scrollHeight)+30});
   //         var query= decodeURIComponent(location.pathname);
   //
   //         b++;
   //     } else { b++; }
   // });
   //  $("#button").click(function(){
   //  	if($('#query').val()){
   //  	    var query=$('#query').val();
   //  	    query_response(query);
   //      }else{
   //          alert('please enter a query');
   //          $('#query').focus();
   //          return false;
   //      }
   //  });