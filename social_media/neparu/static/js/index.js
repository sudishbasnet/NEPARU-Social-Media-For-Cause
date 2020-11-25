


function searchFriends() {
    const url = '/neparu/sathiharu'
    const delay_by_in_ms = 0
    let scheduled_function = false

    let ajax_call = function (url, req_param) {
        $.getJSON(url, req_param)
            .done(response => {
                $('#querydata').promise().then(() => {
                    $('#querydata').html(response['html_view'])
                    $('#querydata').fadeTo('slow', 1)
                })
            })
    }

    const req_param = {
        q: $("#searchdata").val(),
        a: $("#action").val()
    }
    //execution cancel if scehduled is false
    if (scheduled_function) {
        clearTimeout(scheduled_function)
    }
    //to retrn id
    scheduled_function = setTimeout(ajax_call, delay_by_in_ms, url, req_param)
}








function searchRental() {
    const url = '/neparu/rental/0'
    const delay_by_in_ms = 0
    let scheduled_function = false

    let ajax_call = function (url, req_param) {
        $.getJSON(url, req_param)
            .done(response => {
                $('#rentaldata').promise().then(() => {
                    $('#rentaldata').html(response['html_view'])
                    $('#rentaldata').fadeTo('slow', 1)
                })
            })
    }

    const req_param = {
        q: $("#option").val(),
        r: $("#range").val(),
        s: $("#requirenum").val(),
        t: $("#rentallocation").val(),
        u: $("#filterbook").val(),

    }
    //execution cancel if scehduled is false
    if (scheduled_function) {
        clearTimeout(scheduled_function)
    }
    //to retrn id
    scheduled_function = setTimeout(ajax_call, delay_by_in_ms, url, req_param)
}





$(document).on('click', '.addcomment', function (e) {
    e.preventDefault();
    if ($('#content' + e.target.id).val() == '') {
        ('#error' + e.target.id).innerHTML = 'Please enter valid comment';
    }
    else {
        $.ajax({
            type: 'POST',
            url: "/neparu/comment",
            data: {
                content: $('#content' + e.target.id).val(),
                feed: e.target.id,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (json) {
                $('#content' + e.target.id).val('');
                $('#' + json.post).append(
                    '<h6 id="cmm' + json.comment + '">' +
                    "<a href='/neparu/user/" + json.actorid + "' class='col-sm-2 col-xs-3'>" + json.actor + "</a>" +
                    "<button class='delComment btn-danger fa fa-minus-circle right' id='cid"+ json.comment +"'></button>" +
                    "<span style='background-color: lightgray;' class='col-ms-6 col-xs-12'>"+json.content+"</span>"
                    +"</h6>"); 
                    
             
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    }
});


$(document).on('click', '.savepost', function (e) {
    e.preventDefault();
    var str = e.target.id;
    var matchingres = str.match(/(\d+)/);
    if (matchingres) {
        pk=matchingres[0];
    } 
    const div = '#title' + pk;
    if ($('#title').val() == '') {
        alert("Caption can't be null");
    }
    else {
        $.ajax({
            type: 'POST',
            url: "/neparu/upost",
            data: {
                title: $(('#tit')+pk).val(),
                id:pk,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (json) {
                $(div).html(json.title);
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    }
    
});





$(document).on('click', '.saverental', function (e) {
    e.preventDefault();
    var str = e.target.id;
    var matchingres = str.match(/(\d+)/);
    if (matchingres) {
        pk = matchingres[0];
    }
        $.ajax({
            type: 'POST',
            url: "/neparu/rental/"+pk,
            data: {
                title: $('#t'+pk).val(),
                price: $('#p' + pk).val(),
                space_no: $('#s' + pk).val(),
                description: $('#d' + pk).val(),
                location: $('#l' + pk).val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (json) {
                $('#title'+pk).html(json.title);
                $('#location' + pk).html(json.location);
                $('#description' + pk).html(json.description);
                $('#price' + pk).html(json.price);
                $('#space_no' + pk).html(json.space_no);
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });

});




$(document).on('click', '.like-post', function (e) {
    e.preventDefault();
    const div = '#like' + e.target.id;
    const div1 = '#like1' + e.target.id;
    $.ajax({
        type: 'POST',
        url: "/neparu/like",
        data: {
            'id': e.target.id,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (json) {
            $(div).html("<a class='like-post " + json.span + "' id='" + json.id+"'>");
            $(div1).html(json.like);
        },
        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
});



$(document).on('click', '.delComment', function (e) {
    var confirmation = confirm("Do you want to delete this comment ?", '');
    if (confirmation == true) {
        var str = e.target.id;
        var matchingres = str.match(/(\d+)/);
        if (matchingres) {
            id = matchingres[0];
        } 
        const div = '#cmm'+id;
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: "/neparu/delComment",
            data: {
                'id':id,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },     // our data object
            success: function (data) {
                $(div).fadeOut();
                $(div).fadeOut();
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    }
});






$(document).on('click', '.sendfeedback', function (e) {
    e.preventDefault();
    var confirmation = confirm("Do you want to send this message ?", '');
    if (confirmation == true) {
        if ($('#feedbackcontent').val() == ''){
            $('#span').html('Message is empty please fill it.');
        }
        else{
            $.ajax({
                type: 'POST',
                url: "/neparu/feedback",
                data: {
                    'feedback': $('#feedbackcontent').val(),
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                },     // our data object
                success: function (data) {
                    $('#feedbackcontent').val('');
                    alert('Your message is sent, it will be response by our admin.')
                },
                error: function (xhr, errmsg, err) {
                    console.log(xhr.status + ": " + xhr.responseText);
                }
            });
        }
    }
});

$(document).on('click', '.deleteimg', function (e) {
    const div = '#img' + e.target.id;
    e.preventDefault();
    var confirmation = confirm("Do you want to delete this image ?", '');
    if (confirmation == true) {
        $.ajax({
            type: 'POST',
            url: "/neparu/deleteimg",
            data: {
                'id': e.target.id,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },     // our data object
            success: function (data) {
                $(div).fadeOut();

            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    }
});



$(document).on('click', '.deleterentalimg', function (e) {
    const div = '#img' + e.target.id;
    e.preventDefault();
    var confirmation = confirm("Do you want to delete this image ?", '');
    if (confirmation == true) {
        $.ajax({
            type: 'POST',
            url: "/neparu/rental/"+e.target.id,
            data: {
                'action': 'photo',
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },     // our data object
            success: function (data) {
                $(div).fadeOut();

            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    }
});




$(document).on('click', '.deletenotification', function (e) {
    var confirmation = confirm("Do you want to delete this notification ?", '');
    if (confirmation == true) {
        const div = '#notification' + e.target.id;
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: "/neparu/admin/dashboard/none/0",
            data: {
                'id': e.target.id,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },     
            success: function (data) {
                $(div).fadeOut();

            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    }
});



$(document).on('click', '.deleteuser', function (e) {
    var confirmation = confirm("Do you want to delete this user account ?", '');
    if (confirmation == true) {
        const div = '#user' + e.target.id;
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: "/neparu/admin/users/none/0",
            data: {
                'id': e.target.id,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (data) {
                $(div).fadeOut();

            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    }
});







$(document).on('click', '.delete-post', function (e) {
    var confirmation = confirm("Do you want to delete this post ?", '');
    if (confirmation == true) {
        const div = '#posts' + e.target.id;
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: "/neparu/deleteReportPost",
            data: {
                'id': e.target.id,
                'action':'delete',
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },     // our data object
            success: function (data) {
                $(div).fadeOut();
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    }
});

$(document).on('click', '.report-post', function (e) {
    var confirmation = confirm("If you report this post and the number of reports exceeds 10% of the number of followers that user have then it will be deleted");
    if (confirmation == true) {
        var str = e.target.id;
        var matchingres = str.match(/(\d+)/);
        if (matchingres) {
            id = matchingres[0];
        } 
        const div = '#rep'+id;
        const div1 = '#posts'+id;
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: "/neparu/deleteReportPost",
            data: {
                'id':id,
                'action': 'report',
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            }, 
            success: function (json) {
                $(div).html(json.report);
                if(json.action == 'remove')
                    $(div1).fadeOut(); 
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    }
});



$(document).on('click', '.addspace', function (e) {
    $('#rentalservice').fadeOut();
    $('#rentalservice1').attr("style", "");
});

$(document).on('click', '.removeSpace', function (e) {
    e.preventDefault();
    var confirmation = confirm("Do you want to remove this space ?");
    if (confirmation == true) {
        const div = '#'+e.target.id;
        $.ajax({
            type: 'POST',
            url: "/neparu/rental/0",
            data: {
                'id': e.target.id,
                'action': 'delete',
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },    
            success: function (data) {
                $(div).fadeOut();
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    }
});




$(document).on('click', '.deleterental', function (e) {
    e.preventDefault();
    var confirmation = confirm("Do you want to remove this space ?");
    if (confirmation == true) {
        const div = '#rental' + e.target.id;
        $.ajax({
            type: 'POST',
            url: "/neparu/admin/rental/delete/0",
            data: {
                'id': e.target.id,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (data) {
                $(div).fadeOut();
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    }
});




$(document).on('click', '.deletebloodrequest', function (e) {
    e.preventDefault();
    var confirmation = confirm("Do you want to remove this request ?");
    if (confirmation == true) {
        const div = '#blood' + e.target.id;
        $.ajax({
            type: 'POST',
            url: "/neparu/admin/blood/none/0",
            data: {
                'id': e.target.id,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (data) {
                $(div).fadeOut();
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    }
});




$(document).on('click', '.acceptBooking', function (e) {
    e.preventDefault();
    var confirmation = confirm("Are you sure that you want to perform this action ?", '');
    if (confirmation == true) {
        const div = '#book'+e.target.id;
        const user = e.target.id;
        const rental = $(('#rental')+user).val();
        $.ajax({
            type: 'POST',
            url: "/neparu/rental/0",
            data: {
                'id': e.target.id,
                'rental': rental,
                'action': 'bookings',
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (data) {
                if (data.result == 'bookings'){
                    $(div).html('<button class="acceptBooking btn-danger" id="'+user+'" style="width:150px;">Ignore Booking</button>');
                }
                else{
                    $(div).html('<button class="acceptBooking btn-primary" id="'+user+'" style="width:150px;">Accept Booking</button>');
                }
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    }
});



$(document).on('click', '.spaceBook', function (e) {
    var confirmation = confirm("Are you sure you want to perform this action ?");
    if (confirmation == true) {
        const id = e.target.id;
        const div = '#bookSpace'+id;
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: "/neparu/rental/0",
            data: {
                'rental':id ,
                'action': 'book',
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (data) {
                if (data.result == 'book') {
                    $(div).html('<button class="spaceBook right btn-danger" id="'+id+'">Cancel Booking now</button>');
                }
                else {
                    $(div).html('<button class="spaceBook right btn-success" id="'+id+'">Book now</button>');
                }
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    }
});



