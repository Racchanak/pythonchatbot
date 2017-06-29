/**
 * Created by RacchanaK on 22/5/17.
 */
const BASE_URL = 'http://chatbot.wow.jobs';
// const BASE_URL = 'http://chatbot.wow.jobs.dev';

var url = BASE_URL + "/bot/";
var query = $.cookie("c_wow_name");
query = query.replace(/[^a-zA-Z0-9 ]/g, '');
var started = query.toLowerCase();
var welcome_msg = ['Started', started];
var i = 0;
var a = [];
$('.custom-input').hide();
if (i == 0) { botfir_sec(welcome_msg[i], i, ''); }

function cjoption(option, this_id='') {
    $('.getstrt').remove();
    $(this_id).addClass('active');
    $(this_id).parent(".owl-item").addClass('show');
    $(this_id).parents(".main-menu").addClass('userselected');
    ajax_response(option,'');
}
$('body').on('click', '.scroll', function() {
    $('.bot-content').animate({ scrollTop: "+=100px" });
});
$("#button").click(function() {
    if ($('#query').val()) {
        var query = $('#query').val();
        if (i == 1) {
            ajax_response(welcome_msg[i],'userInput',query);
        } else {
            ajax_response(query, 'userInput');
        }
    } else {
        $('#query').focus();
        return false;
    }
});

function handle(e) {
    if (e.keyCode === 13) {
        e.preventDefault(); // Ensure it is only this code that rusn
        $("#button").trigger('click');
    }
}
var xy = 17;
function ajax_response(query, second_value,input='') {
    $('.custom-input').show();
    $ans_html = $ques_html = '';
    $.ajax({
        url: url + query,
        type: "GET",
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        crossDomain: true,
        headers: { 'Access-Control-Allow-Origin': '*' },
        beforeSend: function() {
            $loader = '<div class="msgLoad">' +
                '<span></span>' +
                '<span></span>' +
                '<span></span>' +
                '</div>';
            $('#result').append($loader);
        },
        success: function(data, textStatus, jqXHR) {
            var date = new Date();
            var hours = date.getHours();
            var minutes = date.getMinutes();
            var ampm = hours >= 12 ? 'pm' : 'am';
            hours = hours % 12;
            hours = hours ? hours : 12; // the hour '0' should be '12'
            minutes = minutes < 10 ? '0' + minutes : minutes;
            var strTime = hours + ':' + minutes + ' ' + ampm;
            if (i == 1) {
                $ques_html = '<div class="replies"><div><p></p><p>Welcome to the World of ' + query + '</p>'+
                    '<p>What are you looking for, today?</p></div>';
                $('#result').append($ques_html);
            } else {
                if (second_value != '') {
                    $ques_html = '<div class="answers"><p></p>'+
                        '<p class="' + second_value + '">' + query + '</p></div>';
                }
                $('#result').append($ques_html);
            }
            $ans_html += '<div class="replies"><div id="ans_' + i + '">' +data.chatData +'</div></div>';
            $('#result').append($ans_html);
            $('.bot-content .owl-carousel').owlCarousel({
                nav: true,
                autoWidth: true,
                items: 2,
                margin: 10,
                navText: ["<img src='" + BASE_URL + "/static/images/chat/arrow-left.png'>", "<img src='" + BASE_URL + "/static/images/chat/arrow-right.png'>"]
            });
            setTimeout(function() {
                $(".msgLoad").remove();
                if (query == 'Location') {
                    var l = Number($('.lat').text());
                    var ln = Number($('.long').text());
                    var labels = $('.name').text();
                    var labelIndex = 0;
                    var map_id = $('.map_disp')[0].id;
                    function initialize() {
                        var myLatLng = { lat: l, lng: ln };
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
                var x = $('#ans_' + i).height();
                var finalX = x - xy + "px";
                $('#ans_' + i).css('max-height', finalX);
                $('#ans_' + i).css('overflow', 'hidden');
                $('.bot-content').animate({ scrollTop: ($('.bot-content')[0].scrollHeight) + x });
                $('#query').val('');
                i++;
            }, 100);
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

function botfir_sec(data, k, query) {
    var date = new Date();
    var hours = date.getHours();
    var minutes = date.getMinutes();
    var ampm = hours >= 12 ? 'pm' : 'am';
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'
    minutes = minutes < 10 ? '0' + minutes : minutes;
    var strTime = hours + ':' + minutes + ' ' + ampm;
    var clid = k;
    if (query != '') {
        $quest_html = '<div class="replies">' +
            '<p></p><p>' + query + '</p>' +
            '</div>';
        $('#result').append($quest_html);
    }
    if (k == 0) {
        console.log(started);
        $ans_html = '<div class="text-center"><img src="' + BASE_URL + '/static/images/chat/woweee.png" alt="image"></div>' +
            '<div class="first-response"><h3>Hello, I\'m Wowee</h3>' +
            '<h4>I\'m AI based assistant for you</h4>'+
            '<a class="getstrt" onclick="cjoption(\''+started+'\')">Get Started</a></div>';
    } else {
        $ans_html = '<div class="replies"><div id="ans_' + clid + '">' +data +'</div></div>';
    }
    $('#result').append($ans_html);
    var x = $('#ans_' + clid).height();
    var finalX = x - xy + "px";
    $('#ans_' + clid).css('max-height', finalX);
    $('#ans_' + clid).css('overflow', 'hidden');
    $('.bot-content').animate({scrollTop: ($('.bot-content')[0].scrollHeight) + x});
    $('#query').val('');
    i++;
}