function create_post() {
    // sanity check
    console.log("inside javascript");
    $.ajax({
        url: "/notification/notificationicon_create",
        type: "POST",
        data: {
            id: 'menuId'
        },
        dataType: "text",
        success: function(msg) {
            // log the returned json to the console
            var data = JSON.parse(msg);
            var notifications = JSON.parse(data.notifications);
            var messages = JSON.parse(data.messages);
            notification_body(notifications);
            message_body(messages);
            // another sanity check
        },

        // handle a non-successful response
        error: function(xhr, errmsg, err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });


}

function notification_body(notification) {
    if (Object.keys(notification).length > 0) {
        $("#n_no").text(Object.keys(notification).length);
        $("#n_no").show();
    } else {
        $("#n_no").hide();
    }
    $("#n_body").html('<li>' +
        '<p class="green">You have ' + Object.keys(notification).length + ' pending notification</p>' +
        '</li>');
    for (var i = 0; i < Object.keys(notification).length; i++) {
        var time = (new Date() - new Date(notification[i].fields.time)) / (1000);
        var days = Math.floor(time / 86400);
        time -= days * 86400;
        var hours = Math.floor(time / 3600) % 24;
        time -= hours * 3600;
        var minutes = Math.floor(time / 60) % 60;
        time -= minutes * 60;
        $("#n_body").append(' <li>' +

            '<a href="/notification/notification_view/' + notification[i].pk + '/?next=' + document.URL + '" style="white-space: wrap;Overflow:auto;">' +
            '<span class="photo"><img alt="avatar" src="/static/assets/img/ui-sam.jpg"></span>' +
            '<span class="subject">' +
            '<span class="from">' + notification[i].fields.title + '</span>' +
            '<span class="time">' + Math.floor(hours) + ' Hr ' + Math.floor(minutes) + ' Mins ago</span>' +
            '</span>' +
            '<span class="message" style="display:block" >' + notification[i].fields.body + '</span>' +
            '</a>' +
            '</li>');
    }
    $("#n_body").append('<li class="external">' +
        '<a href="/notification/all_notification/">See All Notification</a>' +
        '</li>');


}


function message_body(messages) {


    if (Object.keys(messages).length > 0) {
        $("#M_no").text(Object.keys(messages).length);
        $("#M_no").show();
    } else {
        $("#M_no").hide();
    }
    $("#M_body").html('<li>' +
        '<p class="green">You have ' + Object.keys(messages).length + ' pending message</p>' +
        '</li>');
    for (var i = 0; i < Object.keys(messages).length; i++) {
        var time = (new Date() - new Date(messages[i].fields.time)) / (1000);
        var days = Math.floor(time / 86400);
        time -= days * 86400;
        var hours = Math.floor(time / 3600) % 24;
        time -= hours * 3600;
        var minutes = Math.floor(time / 60) % 60;
        time -= minutes * 60;
        $("#M_body").append(' <li onClick=messageViewed(' + messages[i].pk + ') data-id=' + messages[i].pk + ' data-toggle="modal" data-target="#fullMessageModal">' +
            '<a href="#" style="white-space: wrap;Overflow:auto;">' +
            '<span class="photo"><img alt="avatar" src="/static/uploaded_image/fpp/' + messages[i].fields.senderImage + '"></span>' +
            '<span class="subject">' +
            '<span class="from">' + messages[i].fields.senderName + '</span>' +
            '<span class="time">' + Math.floor(hours) + ' Hr ' + Math.floor(minutes) + ' Mins ago</span>' +
            '</span>' +
            '<span  class="time" style="float:left;display: inline-block;padding-right: 5px;clear:both" >' + messages[i].fields.title + '</span>' +
            '</a>' +
            '</li>');
    }
    $("#M_body").append('<li class="external">' +
        '<a href="#">See All Messages</a>' +
        '</li>');


}

function messageViewed(mid) {
    $.ajax({
        url: "/notification/message_view/",
        type: "POST",
        data: {
            id: mid
        },
        dataType: "text",
        success: function(msg) {
            // log the returned json to the console
            console.log("Success");
            var data = JSON.parse(msg);
            $('#modal_message_title').html(data[0].fields.title);
            $('#modal_message_body').html(data[0].fields.body);
            $('#modal_message_sender').html("Sender:&nbsp;&nbsp" + data[0].fields.senderName);
            $('#modal_message_time').html("Receiving time:&nbsp;&nbsp" + data[0].fields.time);
            $('#fullMessageModal').show();
            create_post()
        },

        // handle a non-successful response
        error: function(xhr, errmsg, err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}

function message_to_faculty(mail) {
    var form = $("#message_form");
    url = "/notification/messageToFaculty/" + mail + "/";
    console.log("action changed");
    $("#message_form").attr('action', url);
}

function send_message() {
    var frm = $("#message_form");
    $.ajax({
        type: frm.attr('method'),
        url: frm.attr('action'),
        data: frm.serialize(),
        success: function(data) {
            console.log("Success");
            $("#messageModel").hide();
            console.log("SHide");
            create_post();
        },
        error: function(data) {
            console.log("error");
        }
    });
}



function datesem(date, branch, sem) {
    console.log(sem);
    d = new Date(date);
    var date = d.getFullYear() + "-" + (d.getMonth() + 1) + "-" + d.getDate();

    $("#S_date").val(date);
    $("#sem").val(sem);
    $("#branch").val(branch);
    $("#rating").html("");
    for (var i = 0; i < sem; i++) {
        $("#rating").append('<span class="fa fa-star" data-rating="1"></span>');
    }
    for (var i = 0; i < 5 - sem; i++) {
        $("#rating").append('<span class="fa fa-star-o" data-rating="1"></span>');
    }


}

function course_register(id){
  $.ajax({
        url: "/courseregister/",
        type: "POST",
        data: {
            id: id
        },
        dataType: "text",
        success: function(msg) {
            // log the returned json to the console
            $('#register_button').html("<button type='button' class='btn btn-lg btn-success btn-block' disabled='true'> REGISTERED </button>")
        },

        // handle a non-successful response
        error: function(xhr, errmsg, err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}