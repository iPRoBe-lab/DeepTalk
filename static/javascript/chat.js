
$(".messages").animate({ scrollTop: $(document).height() }, "fast");

function newMessage() {
    message = $("#q").val();
    console.log(message)
    if ($.trim(message) == '') {
        return false;
    }
    $('<li class="sent"><img src="static/images/user.png" alt="" /><p>' + message + '</p></li>').appendTo($('.messages ul'));
    $('#q').val(null);
    $(".messages").animate({ scrollTop: $(document).height() }, "fast");

    sendRequest(message);
};

function sendRequest(message) {

    req = { "msg": message }

    $.ajax({
        method: "POST",
        url: "./api/message",
        data: req
    })
        .done(function (response) {
            newReply(response);
        });
}

function newReply(message) {

    if ($.trim(message) == '') {
        return false;
    }

    $('<li class="replies"><img src="static/images/watson_avatar.png" alt="" /><p>' + message + '</p></li>').appendTo($('.messages ul'));
    $('#q').val(null);
    $(".messages").animate({ scrollTop: $(document).height() }, "fast");
};

$('.submit').click(function () {
    newMessage();
});

$(window).on('keydown', function (e) {
    if (e.which == 13) {
        newMessage();
        return false;
    }
});