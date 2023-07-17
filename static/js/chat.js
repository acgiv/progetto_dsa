let id_message_click ;

function change_title(text){
    let id_chat = id_message_click.replace("number_chat_", "");
    $.ajax({
    url: '/change_title',
    type: 'POST',
    data:{
      "chat_textarea":text,
      "id_chat": id_chat
    }, success: function(data) {
              if(data !== "false"){
                document.getElementById("title_number_chat_".concat(id_chat)).innerText = data.replace('\"', '');
                $("#new_chat").find("#title_number_chat_".concat(id_chat)).text(data);
            }
        }
     });
}

function send_message_text() {
  let text = document.getElementById("chat_textarea").value;
  $.ajax({
    url: '/send_message',
    type: 'POST',
    data:{
      "chat_textarea":text,
      "id_chat": id_message_click
    },
    success: function(data) {
      $("#chat").append($(data.message));
      document.getElementById("chat_textarea").value="";
      response_message(text);
      change_title(text);

    }
  });
}

function response_message(text, title) {
  $.ajax({
    url: '/respost_message',
    type: 'POST',
    data: {
      "chat_textarea":text,
      "id_chat": id_message_click
    },
    success: function(data) {
      $("#chat").append($(data));
    }
  });
}



function create_new_chat() {
  $.ajax({
    url: '/create_new_chat',
    type: 'POST',
    success: function(data) {
      $("#new_chat").append($(data));
      document.getElementById("send_text").disabled = true;
    }
  });
}

function view_chat_message(element) {
  id_message_click =element.id;
  $.ajax({
    url: '/view_chat_message',
    type: 'POST',
    data: {
      "id_chat":id_message_click,
    },
    success: function(data) {
      $("#chat").html($(data));
      document.getElementById("send_text").disabled = false;
    }
  });
}

function reformulate_message(id){
  let id_message = "message_".concat(id);
  $.ajax({
      url: '/reformulate_message',
      type: 'POST',
      data: {
      "id_chat":id_message_click,
      "id_message":id_message,
      "id_text": document.getElementById(id_message).getAttribute("id_text"),

    },success: function (data){
      const paragrafo = document.getElementById(id_message);
      paragrafo.textContent= data.message;
      document.getElementById(id_message).setAttribute("id_text",data.id_text);
      const info = data.info_message.hour_minutes.concat(" | ").concat(data.info_message.Month_day)
      document.getElementById("info_".concat(id)).textContent = info;
      document.getElementById("back_".concat(id)).classList.remove("d-none");
      document.getElementById("next_".concat(id)).classList.remove("d-none");
      let text_list = document.getElementById("text_".concat(id));
      text_list.textContent =(data.id_text+1).toString().concat("/").concat((data.id_text+1).toString());
      text_list.classList.remove("d-none");


    }
  });
}

function send_message_text_pepper(id){
  let id_message = "message_".concat(id);
  $.ajax({
      url: '/send_message_text_pepper',
      type: 'POST',
      data: {
      "id_chat":id_message_click,
      "id_message":id_message,
      "id_text": document.getElementById(id_message).getAttribute("id_text")
    },success: function (data){
      console.log("cliccato");
    }
  });
}

function goToBack(id){
  let id_message = "message_".concat(id);
  $.ajax({
      url: '/goToBack',
      type: 'POST',
      data: {
      "id_chat":id_message_click,
      "id_message":id_message,
      "id_text": document.getElementById(id_message).getAttribute("id_text"),
      "position_id_text": "",
      "id_max_text": ""
    },success: function (data){
      if(data.on === true){
          document.getElementById(id_message).setAttribute("id_text",data.id_text);
          const paragrafo = document.getElementById(id_message);
          paragrafo.textContent= data.message;
          document.getElementById(id_message).setAttribute("id_text",data.id_text);
          let text_list = document.getElementById("text_".concat(id));
          text_list.textContent =(data.position_id_text).toString().concat("/").concat(data.id_max_text.toString());
      }else{
           document.getElementById("back_".concat(id)).disabled = true;
           document.getElementById("next_".concat(id)).disabled = false;
      }
    }
  });
}


function goToNext(id){
  let id_message = "message_".concat(id);
  $.ajax({
      url: '/goToNext',
      type: 'POST',
      data: {
      "id_chat":id_message_click,
      "id_message":id_message,
      "id_text": document.getElementById(id_message).getAttribute("id_text"),
      "position_id_text": "",
      "id_max_text": ""
    },success: function (data){
      if(data.on === true){
          document.getElementById(id_message).setAttribute("id_text",data.id_text);
          const paragrafo = document.getElementById(id_message);
          paragrafo.textContent= data.message;
          document.getElementById(id_message).setAttribute("id_text",data.id_text);
          let text_list = document.getElementById("text_".concat(id));
          text_list.textContent =(data.position_id_text).toString().concat("/").concat(data.id_max_text.toString());
      }else{
           document.getElementById("next_".concat(id)).disabled = true;
           document.getElementById("next_".concat(id)).disabled = false;
      }
    }
  });
}
