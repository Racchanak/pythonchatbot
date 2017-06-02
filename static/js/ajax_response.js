/**
 * Created by RacchanaK on 22/5/17.
 */
const BASE_URL = 'http://chatbot.wow.jobs:5000';

var url= BASE_URL+"/bot/";
var query = $.cookie("c_wow_name");
query = query.replace(/[^a-zA-Z0-9 ]/g, '');
var welcome_msg = ['<p>Hello, I\'m Wowee?</p>','<p>Welcome to the World of '+query.toUpperCase()+'</p>',query.toUpperCase()]
var i=0;
if(i==0){ botfir_sec(welcome_msg[i],i,''); }
function cjoption(option){ ajax_response(option); }
$("#button").click(function(){
    console.log(i);
    if($('#query').val()){
        var query=$('#query').val();
        if(i==1) {
            botfir_sec(welcome_msg[i], i, query);
        } else {
            if(i==2) {
                    ajax_response(welcome_msg[i], query);
                }
            else
                {
                    ajax_response(query);
                }
        }
    }else{
        alert('please enter a query');
        $('#query').focus();
        return false;
    }
});

function ajax_response(query,second_value='') {
    $ans_html = '';
    $.ajax({
        url: url + query,
        type: "GET",
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        crossDomain: true,
        headers: {'Access-Control-Allow-Origin': '*'},
        success: function (data, textStatus, jqXHR) {
            if(i==2){
                $ques_html = '<div class="answers">'+
                                '<p>What are you looking for, today?</p>'+
                            '</div>';
            } else {
                $ques_html = '<div class="answers">' +
                    '<p>' + query + '</p>' +
                    '</div>';
            }
            $ans_html += '<div class="replies">'+
                            data.chatData+
                        '</div>';
            $('#result').append($ques_html);
            $('#result').append($ans_html);
            $('.bot-content .owl-carousel').owlCarousel({
                nav: true,
                autoWidth: true,
                items: 1,
                margin: 8,
                navText: ["<img src='http://127.0.0.1:5001/static/images/chat/arrow-left.png'>", "<img src='http://127.0.0.1:5001/static/images/chat/arrow-right.png'>"]
            });
            $('#query').val('');
            i++;
            console.log(i);
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
function botfir_sec(data,k,query){
    if(k>1) { ajax_response(welcome_msg[k],query); }
    var clid = k;
    if(query!='') {
        $quest_html = '<div class="replies">'+
                        '<p>'+query+'</p>'+
                      '</div>';
        $('#result').append($quest_html);
    }
    if(k==0){
        $ans_html ='<div class="text-center">'+
                        '<img src="'+BASE_URL+'/static/images/chat/woweee.png" alt="image">'+
                    '</div>'+
                    '<div class="first-response">'+
                    '<h3>'+data+'</h3>'+
                    '<h4>I\'m AI based assistant for you</h4>';
                '</div>';
    } else {
        $ans_html = '<div class="answers">' +
                        data +
                    '</div>';
    }
    $('#result').append($ans_html);
    $('#query').val('');
    i++;
    console.log(i);
}
// function query_response(query) {
//     console.log(query);
//     $.ajax({
//         url: url + query,
//         type: "GET",
//         dataType: "json",
//         contentType: "application/json; charset=utf-8",
//         crossDomain: true,
//         headers: {'Access-Control-Allow-Origin': '*'},
//         success: function (data, textStatus, jqXHR) {
//             $ans_html = '<div class="scroll answer">' +
//                             '<img src= '+BASE_URL+'"/static/images/chat/answ.png" alt="image">' +
//                             '<div class="anscontent" id="ans_'+clid+'">' +
//                                 data.chatData +
//                             '</div>' +
//                         '</div>';
//             var clid = (i++);
//             $ques_html = '<div class="quest">' +
//                             '<div class="quescontent">' +
//                                 '<p class="p_' + clid + '">' +query  + '</p>' +
//                             '</div>' +
//                             '<img src="'+BASE_URL+'static/images/chat/ques.png" alt="image">' +
//                         '</div>';
//             $('#result').append($ques_html);
//             $('#result').append($ans_html);
//             var x = $('#ans_'+clid).height();
//             var xy= 6;
//             var finalX = x - xy +"px";
//             $('#ans_'+clid).css('max-height',finalX);
//             $('#ans_'+clid).css('overflow','hidden');
//             $('body').on('click', '.scroll', function() {
//                 $('.chatbox-content').animate({scrollTop: "+="+x});
//             });
//             $('#query').val('');
//         },
//         error: function (jqXHR, exception) {
//             if (jqXHR.status === 0) {
//                 alert('Not connect.\n Verify Network.');
//             } else if (jqXHR.status == 404) {
//                 alert('Requested page not found. [404]');
//             } else if (jqXHR.status == 500) {
//                 alert('Internal Server Error [500].');
//             } else if (exception === 'parsererror') {
//                 alert('Requested JSON parse failed.');
//             } else if (exception === 'timeout') {
//                 alert('Time out error.');
//             } else if (exception === 'abort') {
//                 alert('Ajax request aborted.');
//             } else {
//                 alert('Uncaught Error.\n' + jqXHR.responseText);
//             }
//         }
//     });
// }
// function response_generate(data,k,query){
//     console.log(k);
//     if(k==2) {
//         query_response(welcome_msg[k]);
//     }
//     var clid = k;
//     if(query!='') {
//        $ques_html = '<div class="quest">' +
//                         '<div class="quescontent">' +
//                             '<p class="p_' + clid + '">' +query  + '</p>' +
//                         '</div>' +
//                         '<img src="'+BASE_URL+'/static/images/chat/ques.png" alt="image">' +
//                     '</div>';
//         $('#result').append($ques_html);
//     }
//     $ans_html = '<div class="scroll answer">' +
//                     '<img src="'+BASE_URL+'/static/images/chat/answ.png" alt="image">' +
//                     '<div class="anscontent"  id="ans_'+clid+'">' +
//                         data +
//                     '</div>' +
//                 '</div>';
//     $('#result').append($ans_html);
//     var x = $('#ans_'+clid).height();
//     var xy= 6;
//     var finalX = x - xy +"px";
//     $('#ans_'+clid).css('max-height',finalX);
//     $('#ans_'+clid).css('overflow','hidden');
//     $('body').on('click', '.scroll', function() {
//         $('.chatbox-content').animate({scrollTop: "+="+x});
//     });
//     $('#query').val('');
//     i++;
// }
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
