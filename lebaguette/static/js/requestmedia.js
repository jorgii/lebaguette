//GET csrf token
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

//Event handler on episode action
function pushRequest(requestUrl,element,cssClass) {
  // var element = event.target,
  var epid = $(element).parents("li").attr("id"),
      dataMerged = {"itemid":epid};
  $(element).addClass(cssClass);

  $.ajax({
    type: 'POST',
    url: requestUrl,
    data: dataMerged,
    dataType: "text",
    success: function() {
      $("#"+epid).fadeOut(800, function(){ $(this).remove();});
      var snackbarContainer = document.querySelector('#snackbar-success'),
          data = {
        message: 'Success!',
        timeout: 1000,
      };
      snackbarContainer.MaterialSnackbar.showSnackbar(data);
    },
    error: function(ts) {
      var snackbarContainer = document.querySelector('#snackbar-error'),
          data = {
        message: 'Could not remove entry '+epid,
        timeout: 3000,
      };
      console.log(ts.responseText);
      snackbarContainer.MaterialSnackbar.showSnackbar(data);
    }
  });
}
$('.episode__approve').click(function(){
  var element = $(this),
      cssClass = "episode__approved";
  pushRequest("/requestmedia/approve/", element, cssClass);
});
$('.episode__reject').click(function(){
  var element = $(this);
      cssClass = "episode__rejected";
  pushRequest("/requestmedia/reject/", element, cssClass);
});
$('.episode__complete').click(function(){
  var element = $(this);
      cssClass = "episode__approved";
  pushRequest("/requestmedia/complete/", element, cssClass);
});
