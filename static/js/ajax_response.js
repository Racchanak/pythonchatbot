/**
 * Created by RacchanaK on 22/5/17.
 */
const BASE_URL = 'http://chatbot.wow.jobs';
// const BASE_URL = 'http://chatbot.wow.jobs.dev';

var url= BASE_URL+"/bot/";
var query = $.cookie("c_wow_name");
query = query.replace(/[^a-zA-Z0-9 ]/g, '');
var welcome_msg = ['<p>Hello, how are you?</p>',query.toLowerCase()]
var i=0;
var a = [];
if(i==0){ botfir_sec(welcome_msg[i],i,''); }
function cjoption(option,this_id=''){ $(this_id).addClass('active'); ajax_response(option); }
$('body').on('click', '.scroll', function() {
    $('.bot-content').animate({scrollTop: "+=100px"});
});
$("#button").click(function(){
    if($('#query').val()){
        var query=$('#query').val();
        if(i==1) {
            ajax_response(welcome_msg[i]);
        } else {
            ajax_response(query,'userInput');
        }
    }else{
        alert('please enter a query');
        $('#query').focus();
        return false;
    }
});
function handle(e){
    if(e.keyCode === 13){
        e.preventDefault(); // Ensure it is only this code that rusn
        $("#button").trigger('click');
    }
}
    var xy= 17;
function ajax_response(query,second_value='') {
    $ans_html = $ques_html = '';
    $.ajax({
        url: url + query,
        type: "GET",
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        crossDomain: true,
        headers: {'Access-Control-Allow-Origin': '*'},
        beforeSend: function() {
        // setting a timeout
            $loader = '<div class="msgLoad">'+
                '<span></span>'+
                '<span></span>'+
                '<span></span>'+
            '</div>';
            $('#result').append($loader);
        },
        success: function (data, textStatus, jqXHR) {
            var date=new Date();
            var hours = date.getHours();
            var minutes = date.getMinutes();
            var ampm = hours >= 12 ? 'pm' : 'am';
            hours = hours % 12;
            hours = hours ? hours : 12; // the hour '0' should be '12'
            minutes = minutes < 10 ? '0'+minutes : minutes;
            var strTime = hours + ':' + minutes + ' ' + ampm;
            if(i==1){
                $ques_html = '<div class="answers"><div>' +
                                '<p>Welcome to the World of '+query +'</p>'+
                            '</div></div>'+
                            '<div class="answers">'+
                                '<p>What are you looking for, today?</p>'+
                            '</div>';
                $('#result').append($ques_html);
            } else {
                if(second_value!='') {
                    $ques_html = '<div class="answers">' +
                        '<p class="'+second_value+'">' + query + '</p>' +
                        '</div>';
                }
                $('#result').append($ques_html);
            }
            $ans_html += '<div class="replies"><div id="ans_'+i+'">'+
                            data.chatData+
                        '</div></div>';
            $('#result').append($ans_html);
            // if($.isFunction('owlCarousel')){
                  $('.bot-content .owl-carousel').owlCarousel({
                    nav: true,
                    autoWidth: true,
                    items: 2,
                    margin: 10,
                    navText: ["<img src='"+BASE_URL+"/static/images/chat/arrow-left.png'>", "<img src='"+BASE_URL+"/static/images/chat/arrow-right.png'>"]
                });
            // } else {
            //     console.log("Not Defined");
            // }
            setTimeout(function(){
                $( ".msgLoad" ).remove();
                if(query=='Location'){
                    var l=Number($('.lat').text());
                    var ln=Number($('.long').text());
                    var labels=$('.name').text();
                    var labelIndex = 0;
                    var map_id = $('.map_disp')[0].id;
                    function initialize() {
                        var myLatLng ={lat: l, lng: ln};
                        var map = new google.maps.Map(document.getElementById(map_id), {
                          zoom: 14,
                          center: myLatLng
                        });
                        var marker = new google.maps.Marker({
                          position: myLatLng,
                          map: map,
                           label: labels,
                        });
                    }
                    initialize();
                }
                var x = $('#ans_'+i).height();
                var finalX = x - xy +"px";
                $('#ans_'+i).css('max-height',finalX);
                $('#ans_'+i).css('overflow','hidden');
                $('.bot-content').animate({scrollTop: ($('.bot-content')[0].scrollHeight)+x});
                $('#query').val('');
                i++;
            },100);
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
    var date=new Date();
            var hours = date.getHours();
            var minutes = date.getMinutes();
            var ampm = hours >= 12 ? 'pm' : 'am';
            hours = hours % 12;
            hours = hours ? hours : 12; // the hour '0' should be '12'
            minutes = minutes < 10 ? '0'+minutes : minutes;
            var strTime = hours + ':' + minutes + ' ' + ampm;
    var clid = k;
    if(query!='') {
        $quest_html = '<div class="replies">'+
                        '<p></p><p>'+query+'</p>'+
                      '</div>';
        $('#result').append($quest_html);
    }
    if(k==0){
        $ans_html ='<div class="text-center">'+
                        '<img src="'+BASE_URL+'/static/images/chat/woweee.png" alt="image">'+
                    '</div>'+
                    '<div class="first-response">'+
                        '<h3>Hello, I\'m Wowee</h3>'+
                        '<h4>I\'m AI based assistant for you</h4>'+
                    '</div>' +
                    '<div class="answers"><div id="ans_'+clid+'">' +
                        data +
                    '</div></div>';
    } else {
        $ans_html = '<div class="answers"><div id="ans_'+clid+'">' +
                        data +
                    '</div></div>';
    }
    $('#result').append($ans_html);
    var x = $('#ans_'+clid).height();
    var finalX = x - xy +"px";
    $('#ans_'+clid).css('max-height',finalX);
    $('#ans_'+clid).css('overflow','hidden');
    $('.bot-content').animate({scrollTop: ($('.bot-content')[0].scrollHeight)+x});
    $('#query').val('');
    i++;
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
