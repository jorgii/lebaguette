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
        message: 'Could not remove entry '+epid + ' ' + ts.statusText,
        timeout: 3000,
      };
      console.log(ts.responseText);
      snackbarContainer.MaterialSnackbar.showSnackbar(data);
    }
  });
}
$(document).on('click', '.episode__approve', function(){
  var element = $(this),
      cssClass = "episode__approved";
  pushRequest("/requestmedia/approve/", element, cssClass);
});
$(document).on('click', '.episode__reject', function(){
  var element = $(this);
      cssClass = "episode__rejected";
  pushRequest("/requestmedia/reject/", element, cssClass);
});
$(document).on('click', '.episode__complete', function(){
  var element = $(this);
      cssClass = "episode__approved";
  pushRequest("/requestmedia/complete/", element, cssClass);
});

$(window).load(function() {
	var win = $('main'),
      totalPages = $('#total_pages').text(),
      viewParam = $(location).attr('href');

  $('#paginator').addClass('hidden');
	// Each time the user scrolls
	$(win).scroll(function() {
		// End of the document reached?
    var element = event.target;
		if(element.scrollHeight - element.scrollTop === element.clientHeight) {
      var currentPage = parseInt($('#current_page_number').text()),
          nextPageNumber = currentPage + 1,
          newCurrentPage = nextPageNumber,
          pageBaseLink = $('#paginator_next').attr('href')
          newNextPageLink = "?page="+(nextPageNumber+1);
      if(newCurrentPage <= totalPages) {
  	    $('#loading').addClass('is-active');
        $('#current_page_number').html(newCurrentPage);
        $('#paginator_next').attr('href', newNextPageLink);
        console.log('ajax fired');

    		$.ajax({
          data: {
                txtsearch: $('#items_list').val()
            },
          type: "GET",
    			url: viewParam + '?page=' + nextPageNumber,
    			dataType: 'html',
    			success: function(data) {
            var result = $('<div />').append(data).find('#items_list').html();
    				$('#items_list').append(result);
    				$('#loading').removeClass('is-active');
    				}
    			});
        }
  		}
	});
});

function pushRequestMedia() {
  var requestMediaUrl = '/requestmedia/add/',
      requestMediaData = $('#input_movie').val(),
      requestMediaDataMerged = {"imdb_id":requestMediaData};
  $.ajax({
    type: 'POST',
    url: requestMediaUrl,
    data: requestMediaDataMerged,
    dataType: "text",
    success: function() {
      var snackbarContainer = document.querySelector('#snackbar-success'),
          data = {
        message: 'Success!',
        timeout: 1000,
      };
      snackbarContainer.MaterialSnackbar.showSnackbar(data);
      $.ajax({
        data: {
              txtsearch: $('#items_list').val()
          },
        type: "GET",
        dataType: 'html',
        success: function(data) {
            $('#items_list').load('/requestmedia/ #items_list');
          }
        });
    },
    error: function(ts) {
      var snackbarContainer = document.querySelector('#snackbar-error'),
          data = {
        message: 'Could not add request: ' + ts.statusText,
        timeout: 3000,
      };
      console.log(ts.responseText);
      snackbarContainer.MaterialSnackbar.showSnackbar(data);
    }
  });
}
$('#requst_media_submit').click(function(event) {
  event.preventDefault();
  pushRequestMedia();
});
