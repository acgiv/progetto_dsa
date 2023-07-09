function send_message_text() {
  $.ajax({
    url: '/send_message',
    type: 'POST',
    success: function(data) {
      $("#chat").append($(data));

      const messageElement = document.getElementById('message');
      messageElement.classList.add('typing-animation');


    }
  });
}

