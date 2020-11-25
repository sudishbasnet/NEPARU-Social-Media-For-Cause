$(document).on('click', '#campaign', function (e) {
    if (document.getElementById('campaign').checked) {
        $('#description').attr("style", "");
    }
    else {
        $('#description').val('');
        $('#description').attr("style", "visibility:hidden;margin-top:-50px;");
        $('#warn').html("");
    }
})


$(document).on('click', '.saveblood', function (e) {
    e.preventDefault();
    if (document.getElementById('checkbox').checked){
        if ($('#location').val() == '')
            $('#warn').html("Location must be provided")
        else{
            if (document.getElementById('campaign').checked && $('#description').val() == '')
                $('#warn').html("For campaign description must be given otherwise uncheck the campain");  
            else if (document.getElementById('campaign').checked == false && $('#bloodgroup').val() == '')
                $('#warn').html("Blood Group should be selected for individual request");
            else{
                const div = '#submitblood';
                $.ajax({
                    type: 'POST',
                    url: "/neparu/blood",
                    data: {
                        'bloodgroup': $('#bloodgroup').val(),
                        'location': $('#location').val(),
                        'description': $('#description').val(),
                        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                    },
                    success: function (json) {
                        if (json.warn == 'yes') {
                            $('#warn').html("Cancel Blood Request to perform next or wait until 24 hrs");
                        }
                        else {
                            $(div).html("<button type='submit' class='right btn btn-success' disabled>Blood successfully asked</button>");
                        }
                    },
                    error: function (xhr, errmsg, err) {
                        console.log(xhr.status + ": " + xhr.responseText);
                    }
                });
            }
        }
    }
    else
        $('#warn').html("Check the box if you are sure to request")
});

$(document).on('click', '.cancel_blood', function (e) {
    e.preventDefault();
    var confirmation = confirm("Do you want to delete this request ?",'');
    if (confirmation == true) {
        const div = e.target.id;
        $.ajax({
            type: 'POST',
            url: "/neparu/blood",
            data: {
                'notification_id': div,
                'cancel_blood': 'yes',
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (json) {
                $('#' + div).fadeOut(1000);
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
}
});

$(document).on('click', '.blood_available', function (e) {
    e.preventDefault();
    const div = ('#blood_info'+e.target.id);
    $.ajax({
        type: 'POST',
        url: "/neparu/blood",
        data: {
            'notification_id': e.target.id,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (json) {
            if(json.action == 'add'){
                $(div).html("<button id='" + e.target.id + "' class='blood_available btn-success'>If you are available, click here</button>");
            }
            else{
                $(div).html("<button id='" + e.target.id + "' class='blood_available btn-warning'>Cancel if you aren't available</button>");
            }
            
        },
        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
});



