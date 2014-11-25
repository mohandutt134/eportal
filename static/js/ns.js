$(document).ready(function () {
  $('html').click(function() {
//Hide the menus if visible
    $("#notificationMenu").removeClass("open");
  });

  $("#notificationicon").click(function(event){
    event.stopPropagation();
    $("#notificationMenu").toggleClass("open");
    $("li").removeClass("open");


});
  $("#notificationMenu").click(function(event){
    event.stopPropagation();
    $("li").removeClass("open");

});
});


function create_post() {
     // sanity check
     console.log("inside javascript");
   $.ajax({
  url: "http://localhost:8000/notification/notificationicon_create",
  type: "POST",
  data: { id : 'menuId' },
  dataType: "text",
  success : function(msg) {
          // log the returned json to the console
          var data=JSON.parse(msg);
            console.log(data); 
            console.log(data[0].fields.body)
            notification_body(data);
            message_body(data);
            // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
});
 

}

function notification_body(notification){
  console.log("inside");
  $("#n_no").text(Object.keys(notification).length);
  $("#n_body").append( '<li>'+
                               '<p class="green">You have '+ Object.keys(notification).length+' pending tasks</p>'+
                            '</li>' );
for(var i=0;i<Object.keys(notification).length;i++){
  $("#n_body").append(' <li>'+
                              '<a href="/notification/notification_view/'+notification[0].fields.receiver+'" style="white-space: wrap;Overflow:auto;">'+
                                    '<span class="photo"><img alt="avatar" src="/static/assets/img/ui-sam.jpg"></span>'+
                                    '<span class="subject">'+
                                    '<span class="from">'+notification[0].fields.title+'</span>'+
                                    '<span class="time">Just now</span>'+
                                    '</span>'+
                                    '<span class="message" style="display:block" >'+notification[0].fields.body+'</span>'+
                                '</a>'+
                            '</li>');
}
  $("#n_body").append( '<li class="external">'+
                                '<a href="#">See All Tasks</a>'+
                            '</li>' );


}


function message_body(notification){
  console.log("inside");
  $("#M_no").text(Object.keys(notification).length);
  $("#M_body").append( '<li>'+
                               '<p class="green">You have '+ Object.keys(notification).length+' pending tasks</p>'+
                            '</li>' );
for(var i=0;i<Object.keys(notification).length;i++){
  $("#M_body").append(' <li>'+
                              '<a href="/notification/message_view/'+notification[0].fields.receiver+'" style="white-space: wrap;Overflow:auto;">'+
                                    '<span class="photo"><img alt="avatar" src="/static/assets/img/ui-sam.jpg"></span>'+
                                    '<span class="subject">'+
                                    '<span class="from">'+notification[0].fields.title+'</span>'+
                                    '<span class="time">Just now</span>'+
                                    '</span>'+
                                    '<span class="message" style="display:block" >'+notification[0].fields.body+'</span>'+
                                '</a>'+
                            '</li>');
}
  $("#M_body").append( '<li class="external">'+
                                '<a href="#">See All Tasks</a>'+
                            '</li>' );


}