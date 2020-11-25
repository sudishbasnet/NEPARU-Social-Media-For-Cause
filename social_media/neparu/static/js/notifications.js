const postcontent = '<a href="/neparu/gallery/postid">' +
    '<img class="right" alt="view" style="width:50px;height:30px;border:2px solid darkorange"></a>';


const rentalcontent = '<a href="/neparu/rental/rentalid">' +
    '<img class="right" src="" alt="view" style="width:50px;height:30px;border:2px solid darkorange"></a>';

const currentNotification = '<li class="list-group-item" style="background-color:lightgray">' +
    '<div class="left row">' +
    '<a href="/neparu/user/Actorid">' +
    ' Username </a>' +
    'content </div> postcontentvalue ' +
    '<br><br>date ' +
    '</li>';

const neparu = '<a class="fa fa-hand-point-right">Neparu</a>';

const blood_notification = '<li class="btn-danger" style="padding:10px;border:2px solid black;text-align:left">' +
    '<h5><a href="/neparu/user/Actorid">' +
    'Username </a> </h5>' +
    '<p>description content</p>' +
    '<h5 id="blood_infoNotificationid"><button id="Notificationid" class="blood_available btn-success">If you are available, click here</button></h5>' +
    '<h6 style="color:black"> BloodGroup <br> Location : address <br> date </h6></li>';

const blood_campaign = 'Blood Group needed : BloodGroup';

function receiveNotification() {
    $.get('/notification', function (ReceiveData) {

        if (ReceiveData.length !== 0) {
            for (var i = 0; i < ReceiveData.length; i++) {
                var cdate = new Date(ReceiveData[i].created_at);
                if (ReceiveData[i].action == 'blood') {
                    var msg = blood_notification.replace('Notificationid', ReceiveData[i].id);
                    msg = msg.replace('Notificationid', ReceiveData[i].id);
                    if (ReceiveData[i].blood_group != ''){
                        msg = msg.replace('BloodGroup', blood_campaign);
                    }
                    msg = msg.replace('description', ReceiveData[i].description);
                    msg = msg.replace('BloodGroup', ReceiveData[i].blood_group);
                    msg = msg.replace('address', ReceiveData[i].location);
                }
                else if (ReceiveData[i].action == 'neparu') {
                    var msg = currentNotification.replace('postcontentvalue', ' ');
                    msg = msg.replace('Username',neparu);
                    msg = msg.replace('content', ReceiveData[i].description);
                }
                else {
                    if (ReceiveData[i].action == 'follow') {
                        var msg = currentNotification.replace('postcontentvalue', ' ');
                    }
                    else if (ReceiveData[i].action == 'rental'){
                        var msg = currentNotification.replace('postcontentvalue', rentalcontent);
                        msg = msg.replace('rentalid', ReceiveData[i].rental);
                    }
                    else {
                        var msg = currentNotification.replace('postcontentvalue', postcontent);
                        msg = msg.replace('postid', ReceiveData[i].post);
                    }
                }
                msg = msg.replace('Username', ReceiveData[i].actor);
                msg = msg.replace('content', ReceiveData[i].content);
                msg = msg.replace('Actorid', ReceiveData[i].actor_id);
                msg = msg.replace('date', cdate);
                $('#notificationdiv').prepend(msg);
                $('#notification-alert').attr("class", "clicknotification change shadow col-md-2 col-xs-2 fa fa-bell");
                tonee();

            }
        
        }
    })

    
    $(document).on('click', '.clicknotification', function (e) {
        $('#notification-alert').attr("class", "clicknotification shadow col-md-2 col-xs-2 far fa-bell");
    })
}




