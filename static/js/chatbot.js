  // Icons made by Freepik from www.flaticon.com
  const BOT_IMG = "/static/img/chatbot/alice_profile_photo_ai.jpg"
  const PERSON_IMG ="/static/img/user_profile.jpeg"
  const BOT_NAME = "Alice";
  const PERSON_NAME = "You";

$(function() {
  var INDEX = 0; 
  $("#chat-submit").click(function(e) {

    ///avoid page to reload
    e.preventDefault();
    //get sms
    var userInput = $("#chat-input").val(); 
    var fileInput = $("#file-input")[0].files[0];

    if(userInput.trim() != ''){
      //add user message to ui 
      generate_message(PERSON_NAME,PERSON_IMG, 'user' ,userInput );  

      //generate response from bot
      botResponse(userInput)
     
    }

    //clean input bar
    $("#chat-input").val('');

    if(!fileInput){
      return false;
    }

      // Create a FormData object to hold the text and/or file data
      var fileToUpload = new FormData();
      fileToUpload.append('file', fileInput);
      generate_message(PERSON_NAME, PERSON_IMG, 'user', 'Sending File: ' + fileInput.name);

      uploadPdfFile(fileToUpload)
      //generate_message(PERSON_NAME, PERSON_IMG, 'user', 'File uploaded: ' + fileInput.name);
      $("#file-input").val('');

    if(userInput.trim() == ''){
      return false;
    }
    //clean input bar
    $("#chat-input").val('');
    
  })
  
  function generate_message(name, img, type, msgText) {
    INDEX++;
    //construct message 
    var str="";
    str += '<div id="cm-msg-0" class="chat-msg '+type+'">'
    //depending on the user show immage in one side or the other 
    str += '<div class="' + (type === "user" ? 'msg-avatar-user' : 'msg-avatar') + '">';

    str +=(type === "user" ?'  <img style="float:right" src="' + img + '" />' :  '  <img src="' + img + '" />');
    str += '</div>'

    str += '<div class="cm-msg-text">'
    str += '  <div class="msg-info">'
    str += '    <div class="msg-info-name">'+name+'</div>'
    str += '    <div class="msg-info-time">'+getCurrentTime()+'</div>'
    str += '  </div>'

    str += '  <div class="msg-text">'
    str += msgText
    str += '  </div>'
    str += '</div>'
    str += '</div>'

    $(".chat-logs").append(str);
    $("#cm-msg-"+INDEX).hide().fadeIn(300);
    if(type == 'user'){
     $("#chat-input").val(''); 
    }    
    $(".chat-logs").stop().animate({ scrollTop: $(".chat-logs")[0].scrollHeight}, 1000);    
  } 
  
  
  function botResponse(rawText) {
    // Bot Response
    $.get("/get", { msg: rawText }).done(function (data) {
      console.log(rawText);
      console.log(data);
      const msgText = data;
      generate_message(BOT_NAME, BOT_IMG, "bot", msgText);
    });
  }
  function uploadPdfFile(fileInput){
    // Use $.ajax with the style of $.get
    $.ajax({
      url: '/upload',  // Your Flask route
      type: 'POST',
      data: fileInput,
      processData: false,
      contentType: false
    })
    .done(function(data) {
      
      console.log(data);

      // Assuming 'data' contains the bot response
      const msgText = "File uploaded successfully, now you can ask questions about your pdf file!";//data.response; // Adjust based on your server response structure
      generate_message(BOT_NAME, BOT_IMG, "bot", msgText);
    })
    .fail(function(error) {
      const msgText = "Failed to upload the file, try later!";//data.response; // Adjust based on your server response structure
      generate_message(BOT_NAME, BOT_IMG, "bot", msgText);
      console.log('Error:', error);
    });
  }
  
  $(document).delegate(".chat-btn", "click", function() {
    var value = $(this).attr("chat-value");
    var name = $(this).html();
    $("#chat-input").attr("disabled", false);
    generate_message(name, 'bot');
  })
  
  $("#chat-circle").click(function() {    
    $("#chat-circle").toggle('scale');
    $(".chat-box").toggle('scale');
  })
  
  $(".chat-box-toggle").click(function() {
    $("#chat-circle").toggle('scale');
    $(".chat-box").toggle('scale');
  })
 
  
// // chat bot original
//   const msgerForm = get(".msger-inputarea");
//   const msgerInput = get(".chat-input");
//   const msgerChat = get(".chat-logs");



//   msgerForm.addEventListener("submit", event => {
//     event.preventDefault();

//     const msgText = msgerInput.value;
//     if (!msgText) return;

//     appendMessage(PERSON_NAME, PERSON_IMG, "right", msgText);
//     msgerInput.value = "";
//     botResponse(msgText);
//   });

//   function appendMessage(name, img, side, text) {
//     //   Simple solution for small apps
//     const msgHTML = `
// <div class="msg ${side}-msg">
// <div class="msg-img" style="background-image: url(${img})"></div>

// <div class="msg-bubble">
//   <div class="msg-info">
//     <div class="msg-info-name">${name}</div>
//     <div class="msg-info-time">${getCurrentTime()}</div>
//   </div>

//   <div class="msg-text">${text}</div>
// </div>
// </div>
// `;

//     msgerChat.insertAdjacentHTML("beforeend", msgHTML);
//     msgerChat.scrollTop += 500;
//   }

  // function botResponse(rawText) {
  //   // Bot Response
  //   $.get("/get", { msg: rawText }).done(function (data) {
  //     console.log(rawText);
  //     console.log(data);
  //     const msgText = data;
  //     appendMessage(BOT_NAME, BOT_IMG, "left", msgText);

  //   });
  // }


  // Utils
  function get(selector, root = document) {
    return root.querySelector(selector);
  }

  function getCurrentTime() {
    var today = new Date();
    var hours = today.getHours();
    var minutes = today.getMinutes();
    var timeFormat = hours + ":" + (minutes < 10 ? '0' : '') + minutes;
    return timeFormat;
  }

  document.getElementById('current-time').innerHTML = getCurrentTime();

})