var questions;
var answer=[];
var question_no=-1;
var timer=0;
var myVar;


function create_post() {

     // sanity check
     console.log("inside javascript");
   $.ajax({
  url: "/notification/notificationicon_create",
  type: "POST",
  data: { id : 'menuId' },
  dataType: "text",
  success : function(msg) {
          // log the returned json to the console
          var data=JSON.parse(msg);
          var notifications = JSON.parse(data.notifications);
          var messages = JSON.parse(data.messages);
          notification_body(notifications);
          message_body(messages);
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
  if(Object.keys(notification).length>0){
    $("#n_no").text(Object.keys(notification).length);
    $("#n_no").show();
  }
  else{
    $("#n_no").hide();
  }
  $("#n_body").html( '<li>'+
                               '<p class="green">You have '+ Object.keys(notification).length+' pending notification</p>'+
                            '</li>' );
for(var i=0;i<Object.keys(notification).length;i++){
   var time=(new Date() - new Date(notification[i].fields.time))/(1000);
   var days = Math.floor(time / 86400);
    time -= days * 86400;
    var hours = Math.floor(time / 3600) % 24;
    time -= hours * 3600;
    var minutes = Math.floor(time / 60) % 60;
    time -= minutes * 60;
  $("#n_body").append(' <li>'+

                              '<a href="/notification/notification_view/'+notification[i].pk+'/?next='+document.URL+'" style="white-space: wrap;Overflow:auto;">'+
                                    '<span class="photo"><img alt="avatar" src="/static/assets/img/ui-sam.jpg"></span>'+
                                    '<span class="subject">'+
                                    '<span class="from">'+notification[i].fields.title+'</span>'+
                                    '<span class="time">'+Math.floor(hours)+' Hr '+Math.floor(minutes)+' Mins ago</span>'+
                                    '</span>'+
                                    '<span class="message" style="display:block" >'+notification[i].fields.body+'</span>'+
                                '</a>'+
                            '</li>');
}
  $("#n_body").append( '<li class="external">'+
                                '<a href="/notification/all_notification/">See All Notification</a>'+
                            '</li>' );


}


function message_body(messages){

  if(Object.keys(messages).length>0){
  $("#M_no").text(Object.keys(messages).length);
  $("#M_no").show();
  }
  else{
    $("#M_no").hide();
  }
  $("#M_body").html( '<li>'+
                               '<p class="green">You have '+ Object.keys(messages).length+' pending message</p>'+
                            '</li>' );
for(var i=0;i<Object.keys(messages).length;i++){
  var time=(new Date() - new Date(messages[i].fields.time))/(1000);
  var days = Math.floor(time / 86400);
    time -= days * 86400;
    var hours = Math.floor(time / 3600) % 24;
        time -= hours * 3600;
        var minutes = Math.floor(time / 60) % 60;
        time -= minutes * 60;
  $("#M_body").append(' <li onClick=messageViewed('+messages[i].pk+') data-id='+messages[i].pk+' data-toggle="modal" data-target="#fullMessageModal">'+
                                    '<a href="#" style="white-space: wrap;Overflow:auto;">'+

                                    '<span class="photo"><img alt="avatar" src="/static/uploaded_image/fpp/'+ messages[i].fields.senderImage +'"></span>'+

                                    '<span class="subject">'+
                                    '<span class="from">'+messages[i].fields.senderName+'</span>'+
                                    '<span class="time">'+Math.floor(hours)+' Hr '+Math.floor(minutes)+' Mins ago</span>'+
                                    '</span>'+
                                    '<span  class="time" style="float:left;display: inline-block;padding-right: 5px;clear:both" >'+messages[i].fields.title+'</span>'+
                                '</a>'+
                            '</li>');
}
  $("#M_body").append( '<li class="external">'+
                                '<a href="#">See All Messages</a>'+
                            '</li>' );


}

function addquestion( id){

  $.ajax({
  url: "http://localhost:8000/quiz/addquestion",
  type: "GET",
  data: { id : id },
  dataType: "text",
  success : function(msg) {
          // log the returned json to the console
         
          msg=JSON.parse(msg);
          quiz_id=JSON.parse(msg.quiz_id);
          
          data=JSON.parse(msg.ques);
          console.log(data.length)
         
          addremoveButton(quiz_id,data,id);
           },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom

            console.log("fail"); // provide a bit more info about the error to the console
        }
});
}
function messageViewed(mid){
  $.ajax({
  url: "/notification/message_view/",
  type: "POST",
  data: { id : mid },
  dataType: "text",
  success : function(msg) {
          // log the returned json to the console
          console.log("Success");
          var data=JSON.parse(msg);
          $('#modal_message_title').html(data[0].fields.title);
          $('#modal_message_body').html(data[0].fields.body);
          $('#modal_message_sender').html("Sender:&nbsp;&nbsp"+data[0].fields.senderName);
          $('#modal_message_time').html("Receiving time:&nbsp;&nbsp"+data[0].fields.time);
          $('#fullMessageModal').show();
          create_post()

          },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom

            console.log("fail"); // provide a bit more info about the error to the console
        }
});

}

function viewfullquestion(id){
   $.ajax({
    url: "http://localhost:8000/quiz/view_fullquestion",
    type: "GET",
    data: { id : id },
    dataType: "text",
    success : function(msg) {
            // log the returned json to the console
              msg=JSON.parse(msg)
            
            console.log(msg);
            questionbody(msg);
            
              // another sanity check
          },

          // handle a non-successful response
          error : function(xhr,errmsg,err) {
              $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                  " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
              console.log("fail"); // provide a bit more info about the error to the console
          }
  });
}

function questionbody(msg){


 $("#q_body").html('<p> <h3>1.'+msg[0].fields.statement+'</h3></p>'+
          '<ul>'+
          '<li id="1" class="fa fa-circle" style="display:block">&nbsp;&nbsp;&nbsp;&nbsp;'+msg[0].fields.a+'</li>'+
         '<li id="2" class="fa fa-circle" style="display:block">&nbsp;&nbsp;&nbsp;&nbsp;'+msg[0].fields.b+'</li>'+
          '<li id="3" class="fa fa-circle" style="display:block">&nbsp;&nbsp;&nbsp;&nbsp;'+msg[0].fields.c+'</li>'+
          '<li id="4" class="fa fa-circle" style="display:block">&nbsp;&nbsp;&nbsp;&nbsp;'+msg[0].fields.d+'</li>'+
          '</ul>'+
          '<p>Comment:'+msg[0].fields.extra_info+'</p>');

  if(msg[0].fields.ans=="a"){
       $("#1").toggleClass('fa-circle fa-check');
      }

    else if(msg[0].fields.ans=="b"){
       $("#2").toggleClass('fa-circle fa-check');
      }
      else if(msg[0].fields.ans=="c"){
       $("#3").toggleClass('fa-circle fa-check');
      }
  
   else{
       $("#4").toggleClass('fa-circle fa-check');
      }



}

function addremoveButton(quiz_id,data,id){
  var flag=false;
  var no_quiz=data[0].fields.quizes.length;
  var rating="#R_"+id;
  var add_id="#add"+id;
  var rm_id="#rm"+id;
  var ic_id="#i"+id;
  for(var i=0;i<no_quiz;i++){
  if(quiz_id==data[0].fields.quizes[i])
    flag=true;
  }

  if(flag){
      console.log(flag);
      $(rating).html(no_quiz);
      $(add_id).hide();
      $(rm_id).show();
      $(ic_id).toggleClass('fa-hand-o-right fa-check');
      $(ic_id).css("color","green");
    }
    else{
      console.log(flag);
      $(rating).html(no_quiz);
      $(add_id).show();
      $(rm_id).hide();
      $(ic_id).toggleClass('fa-check fa-hand-o-right');
      $(ic_id).css("color","");
    }
}



function removeQuestion(id){
  $.ajax({
    url: "http://localhost:8000/quiz/removeQuestion",
    type: "GET",
    data: { id : id },
    dataType: "text",
    success : function(msg) {
          // log the returned json to the console
          console.log(msg);
          msg=JSON.parse(msg);
          quiz_id=JSON.parse(msg.quiz_id);
          data=JSON.parse(msg.ques);
          console.log(data[0].fields.quizes.length);
          addremoveButton(quiz_id,data,id);

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


function qizquestions(){


  $.ajax({
    url: "http://localhost:8000/quiz/qizquestions",
    type: "GET",
    data: {},
    dataType: "text",
    success : function(msg) {
          // log the returned json to the console
          console.log(msg);
          msg=JSON.parse(msg);
          console.log(msg[0].pk);
          console.log("success");
          showbutton(msg);

        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log("fail"); // provide a bit more info about the error to the console
        }
});

}

function showbutton(msg){
  for(var i=0;i<msg.length;i++){
    var add_id="#add"+msg[i].pk;
    var rm_id="#rm"+msg[i].pk;
    var ic_id="#i"+msg[i].pk;
      $(add_id).hide();
      $(rm_id).show();
      $(ic_id).toggleClass('fa-hand-o-right fa-check');
      $(ic_id).css("color","green");
  }


}


function message_to_faculty(mail){
  var form = $("#message_form");
  url = "/notification/messageToFaculty/"+mail+"/";
  console.log("action changed");
  $("#message_form").attr('action',url);
}

function send_message(){
var frm = $("#message_form");
        $.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            data: frm.serialize(),
            success: function (data) {
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


function changeQuiz(){
  var pass = $("#q_title").val()
  console.log(pass)
  $.ajax({
    url: "http://localhost:8000/quiz/changeQuiz",
    type: "GET",
    data: { id : pass },
    dataType: "text",
    success : function(msg) {
          // log the returned json to the console
          
          msg=JSON.parse(msg)
          course=msg.course;
          quiz=JSON.parse(msg.quiz);
          
          set_value(quiz,course);
          
            // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log("fail"); // provide a bit more info about the error to the console
        }
});

}

function set_value(msg,course){
$("#q_course").val(course);
$("#q_time").val(msg[0].fields.duration);
$("#q_start").val(msg[0].fields.start_date);
$("#q_end").val(msg[0].fields.end_date);
$("#q_question").val(msg[0].fields.no_Questions);
$("#q_credits").val(msg[0].fields.credit)

}





//student quiz viewfullquestion


function studentQuestions(duration){
  timer=duration*60;
    $.ajax({
    url: "http://localhost:8000/quiz/qizquestions",
    type: "GET",
    data: {},
    dataType: "text",
    success : function(msg) {
        
          // log the returned json to the console
          console.log(msg);
          questions=JSON.parse(msg);
         // questions=JSON.parse(msg);
        
          
         // set_answer(questions);
          next_function();
      

        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log("fail"); // provide a bit more info about the error to the console
        }
});


}


function set_answer(questions){
for(var i=0;i<questions.length;i++){
  answer[questions[i].fields.statement]=questions[i].fields.ans;
}

}


function next_function(){
 clearInterval(myVar);
 uncheck();
  console.log("next");

  question_no=question_no+1;
  if(question_no>questions.length-1){
    
  question_no=0;
}
if(question_no==4){
  $("#q_submit").show();
}
else{
   $("#q_submit").hide();
}


 $("#question").text(questions[question_no].fields.statement);
  $("#option1").text(questions[question_no].fields.a);
  $("#option2").text(questions[question_no].fields.b);
  $("#option3").text(questions[question_no].fields.c);
  $("#option4").text(questions[question_no].fields.d);
 check();
 myVar = setInterval(timer1, 1000);

 
  

}



function previous_function(){
 clearInterval(myVar);
 uncheck();
question_no=question_no-1;
  if(question_no < 0){
    question_no=questions.length-1;
  }

  if(question_no==4){
  $("#q_submit").show();
}
else{
   $("#q_submit").hide();
}
  
    $("#question").text(questions[question_no].fields.statement);
     $("#option1").text(questions[question_no].fields.a);
    $("#option2").text(questions[question_no].fields.b);
    $("#option3").text(questions[question_no].fields.c);
    $("#option4").text(questions[question_no].fields.d);
    check();
myVar = setInterval(timer1, 1000);

}

//for countdown timer
function timer1(){

  timer=timer-1;
  var min=Math.floor(timer/60);
  var second=timer-(min*60);

  $("#q_time").text(min+":"+second);
  //for time end
  if (timer==0){
    clearInterval(myVar);
    //function call for answer submit in data base
  }
}

//for save user answer
function submitanswer(){
  var ans;
var radios = document.getElementsByName("user[role]");
for( i = 0; i < radios.length; i++ ) {
        if( radios[i].checked ) {
          ans= radios[i].value;
        }
    }
var title=$("#question").text();

answer[title]=ans;


}


// for clear radio button selection

function uncheck(){
  var radios = document.getElementsByName("user[role]");
for( i = 0; i < radios.length; i++ ) {
        if( radios[i].checked ) {
          radios[i].checked=false;
        }
    }

}

// for rember user answer
function check(){
  var title=$("#question").text();
  var radios = document.getElementsByName("user[role]");
  for( i = 0; i < radios.length; i++ ) {
        if( radios[i].value == answer[title] ) {
          radios[i].checked=true;
        }
    }
}

function datesem(date,branch,sem){
  
 d=new Date(date);
 var date= d.getFullYear()+"-"+(d.getMonth()+1)+"-"+d.getDate();
 
$("#S_date").val( date);
$("#sem").val(sem);
$("#branch").val(branch);
$("#rating").html("");
for (var i= 0;i<sem;i++)
{
  $("#rating").append('<span class="fa fa-star" data-rating="1"></span>');
}
for (var i= 0;i<5-sem;i++)
{
  $("#rating").append('<span class="fa fa-star-o" data-rating="1"></span>');
}


}

