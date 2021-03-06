/**
 * Created by RacchanaK on 22/5/17.
 */
const BASE_URL = 'https://chatbot.wow.jobs';
// const BASE_URL = 'http://chatbot.wow.jobs.dev';

var url = BASE_URL + "/bot/";
var query = $.cookie("c_wow_name");
query = query.replace(/[^a-zA-Z0-9 ]/g, '');
var started = query.toLowerCase();
var welcome_msg = ['Started', started];
var i = 0;
var owlid = 0;
var a = [];
$('.custom-input').hide();
if (i == 0) { botfir_sec(welcome_msg[i], i, ''); }

function cjoption(option, this_id='') {
    $('.getstrt').remove();
    $(this_id).addClass('active');
    $(this_id).parent(".owl-item").addClass('show');
    $(this_id).parents(".owl-carousel").css('pointer-events','none');
    $(this_id).parents(".owl-wrapper").css('width','auto');
    if(option!='Interview Tips' || option!='Hr Email') {
        $(this_id).css('margin-left', '0');
        $(this_id).css('margin-right', '0');
    }
    $(this_id).parents(".owl-wrapper").css('transform','none');
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
var xy = 29;
var $loader = '<div class="msgLoad">' +
    '<span></span>' +
    '<span></span>' +
    '<span></span>' +
    '</div>';
function ajax_response(query, second_value,input='') {
    $ans_html = $ques_html = '';
    $('.custom-input').show();
    if (i == 1) {
        $ques_html = '<div class="replies"><div><p></p><p>Welcome to the World of ' + toCamelCase(query) + '</p></div>';
        $('#result').append($ques_html);
        $('#result').append($loader);
        setTimeout(function () {
            ajax_call(query, second_value,input='');
        },1000);
    } else {
        $('#result').append($loader);
        ajax_call(query, second_value,input='');
    }
}

function toCamelCase(word) {
    var out = "";
    word.split(" ").forEach(function (el, idx) {
        var add = el.toLowerCase();
        out += add[0].toUpperCase() + add.slice(1) + ' ';
    });
    return out;
}

function ajax_call(query, second_value,input='') {
    $ans_html = $ques_html = '';
    if ((query.indexOf('Where') >= 1) || query == 'location' || (query.indexOf('where') >= 1) ||
        (query.indexOf('Office') >= 1) || (query.indexOf('office') >= 1) || query == 'Location') {
        query = 'Location';
    }
    $.ajax({
            url: url + query,
            type: "GET",
            dataType: "json",
            contentType: "application/json; charset=utf-8",
            crossDomain: true,
            headers: { 'Access-Control-Allow-Origin': '*' },
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
                    $ques_html = '<div class="replies"><div><p></p><p>What are you looking for today?</p></div>';
                    $('#result').append($ques_html);
                } else {
                    if (second_value != '') {
                        $ques_html = '<div class="answers"><p></p>'+
                            '<p class="' + second_value + '">' + query + '</p></div>';
                    }
                    $('#result').append($ques_html);
                }
                $ans_html += '<div class="replies"><div id="ans_' + i + '">' +data.chatData +'</div></div>';
                var owl_carousel1 = {
                  items : 2, //10 items above 1000px browser width
                  itemsDesktop : [1000,2], //5 items between 1000px and 901px
                  itemsDesktopSmall : [900,3], // betweem 900px and 601px
                  itemsTablet: [600,2], //2 items between 600 and 0
                  itemsMobile : false, // itemsMobile disabled - inherit from itemsTablet option
                  navigation: true,
                  navigationText: ["<img src='" + BASE_URL + "/static/images/chat/arrow-left.png'>", "<img src='" + BASE_URL + "/static/images/chat/arrow-right.png'>"]
                };
                $('#result').append($ans_html);
                var owl_theme = $("#ans_" + i).find('.owl-theme');
                for(var j=0;j<owl_theme.length;j++) {
                    var owl_id = "owl_" + owlid;
                    owl_theme[j].setAttribute("id", owl_id);
                    $('#' + owl_id).owlCarousel(owl_carousel1);
                    owlid++;
                }
                if (query == 'Location') {
                    $("#ans_" + i).find(".map_disp").addClass('mapdisp_'+i);
                    var mapid = 'map_disp_' + i;
                    $(".mapdisp_"+i)[0].setAttribute("id", mapid);
                }
                setTimeout(function() {
                    $(".msgLoad").remove();
                    if (query == 'Location') {
                        var previow_map = $(".map_disp").html();
                        var l = Number($('.lat').text());
                        var ln = Number($('.long').text());
                        var labels = $('.name').text();
                        var labelIndex = 0;
                        var map_id = $('.mapdisp_'+i)[0].id;
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
                        if(previow_map!=''){
                            $('#'+map_id).html(previow_map);
                            $('#'+map_id).css('position','relative');
                            $('#'+map_id).css('overflow','hidden');
                        } else {
                            initialize();
                        }
                    }
                    var x = $('#ans_' + i).height();
                    if(query=='Interview Tips' || query=='Hr Email'){
                        xy = 24;
                    }
                    var finalX = x - xy + "px";
                    $('#ans_' + i).css('max-height', finalX);
                    $('#ans_' + i).css('overflow', 'hidden');
                    $('#ans_' + i).css('margin-left', '-10px');
                    $('#ans_' + i).css('margin-right', '-10px');
                    $('#ans_' + i).css('padding', '0 10px');
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
        $ans_html = '<div class="text-center"><img src="' + BASE_URL + '/static/images/chat/woweee.png" alt="image"></div>' +
            '<div class="first-response"><h3>Hi, I am Wowee.</h3>' +
            '<h4>I am here to help you.</h4>'+
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