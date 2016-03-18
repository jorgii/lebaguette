// submit form on external button click
$("#submit_form").click( function() {
    $('#profile_form').submit();
});

//clear error tooltips on input click
$('input').click(function(){
  var id = $(this).attr('id');
  var errorTooltipId = id + '_error';
  var errorTooltipElement = document.getElementById(errorTooltipId);
  console.log(errorTooltipElement);

  $(errorTooltipElement).remove();
});

// form validation
$('#id_new_password1').on("keyup focusout", function(){
  var progressBar = document.getElementById('password_strength');
  var tooltip = document.getElementById('password_tooltip');
  var password = $.trim($(this).val());
  var count = 0;
  var className, progress, strength;

  //if the password length is less than 6
  if(password.length < 6) count = 0
  //if length is 8 characters or more, increase counter value
  if (password.length > 7) count += 1
  //if password contains both lower and uppercase characters, increase counter value
  if (password.match(/([a-z].*[A-Z])|([A-Z].*[a-z])/)) count += 1
  //if it has numbers and characters, increase counter value
  if (password.match(/([a-zA-Z])/) && password.match(/([0-9])/)) count += 1
  //if it has one special character, increase counter value
  if (password.match(/([!,%,&,@,#,$,^,*,?,_,~])/)) count += 1
  //if it has two special characters, increase counter value
  if (password.match(/(.*[!,%,&,@,#,$,^,*,?,_,~].*[!,%,&,@,#,$,^,*,?,_,~])/)) count += 1

  if (count == 0) {
  className = "short";
  progress = 10;
  message = "At least 6 characters";
  }
  else if (count == 1 ) {
  className = "weak";
  progress = 40;
  message = "You can do better!";
  }
  else if (count == 2 ) {
  className = "good";
  progress = 70;
  message = "Works for me...";
  }
  else {
  className = "strong";
  progress = 100;
  message = "Most awesome password ever!";
  }

  progressBar.MaterialProgress.setProgress(progress);
  //clear old class
  $(progressBar).removeClass('strong');
  $(progressBar).removeClass('good');
  $(progressBar).removeClass('weak');
  $(progressBar).removeClass('short');
  //update class and text
  $(progressBar).addClass(className);
  $(password_tooltip).text(message);

  //clear bar if empty
  if(password.length == 0) {
    progressBar.MaterialProgress.setProgress(0);
    $(progressBar).removeClass('strong');
    $(progressBar).removeClass('good');
    $(progressBar).removeClass('weak');
    $(progressBar).removeClass('short');
  }
});

//new and repeat password match while typing
$('#id_new_password2').on('keyup', isPassValid);
$('#id_new_password1').on('keyup', isPassValid);
$('#id_new_password1').on('keyup', oldPassNeedsValue);
$('#id_old_password').on('keyup', oldPassNeedsValue);

//new and repeat password match function
function isPassValid(){
var passNew = document.getElementById('id_new_password1');
var passOld = document.getElementById('id_new_password2');
var passNewValue = passNew.value;
var passOldValue = passOld.value;

if(passNewValue!=passOldValue) {
  $(passOld).parent().addClass('is-invalid');
}
else {
  $(passOld).parent().removeClass('is-invalid');
}
}
function oldPassNeedsValue(){
var passNew = document.getElementById('id_new_password1');
var passOld = document.getElementById('id_old_password');

if(passNew.value.length > 0) {
  if(passOld.value.length == 0) {
    $(passOld).parent().addClass('is-invalid');
  }
}
else {
  $(passOld).parent().removeClass('is-invalid');
}
}
