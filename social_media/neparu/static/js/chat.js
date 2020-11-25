let variable = ''

const currentmsg = '<div class="msg right" style="background-color:gray;">' +
    '<h6> CurrentMsg </h6>' +
    '</div>';

const imgrep = '<img class="msgImg right" src="imageurl">';

function ScrollY() {
    $('#msgdiv').animate({
        scrollTop: $('#msgdiv')[0].scrollHeight
    }, 1000);
}

function send(sender, receiver, message, imgurl) {
    if (message != '' && imgurl == null) {
        var msg = currentmsg.replace('CurrentMsg', message);
        $('#msgdiv').append(msg);
    }
    else if (imgurl != null && message == '') {
        var repimg = imgrep.replace('imageurl', imgurl);
        $('#msgdiv').append(repimg);
    }
    else if (message != '' && imgurl != null) {
        var msg = currentmsg.replace('CurrentMsg', message);
        $('#msgdiv').append(msg);
        var repimg = imgrep.replace('imageurl', imgurl);
        $('#msgdiv').append(repimg);
    }

    ScrollY();

}

function receive() {
    $.get('/inbox/' + SenderId + '/' + ReceiverId, function (ReceiveData) {
        if (ReceiveData.length !== 0) {
            for (var i = 0; i < ReceiveData.length; i++) {
                if (ReceiveData[i].message != '') {
                    var msg = currentmsg.replace('CurrentMsg', ReceiveData[i].message);
                    msg = msg.replace('right', 'left bg-primary');
                    msg = msg.replace('background-color:gray', '');
                    $('#msgdiv').append(msg);
                }
                $.ajax({
                    type: 'POST',
                    url: "/neparu/inbox",
                    data: {
                        'sender': SenderId,
                        'receiver': ReceiverId,
                        'action': 'receiveimg',
                        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                    },
                    success: function (json) {
                        if (json.url != '') {
                            var repimg = imgrep.replace('imageurl', json.url);
                            repimg = repimg.replace('right', 'left');
                            $('#msgdiv').append(repimg);
                        }
                    },
                    error: function (xhr, errmsg, err) {
                        console.log(xhr.status + ": " + xhr.responseText);
                    }
                });
                ScrollY();
            }
        }
    })
}


