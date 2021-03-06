// Events fired on window load (infinite scroll handling)
$(window).load(function() {
	var win = $('main'),
      totalPages = $('#total_pages').text(),
      viewParam = $(location).attr('href');

  $('#paginator').addClass('hidden');
	// Each time the user scrolls
	$(win).scroll(function(event) {
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

// GET csrf token
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

// Ajax setup
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

// Event handlers
// Push media action
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
        message: 'Could not remove entry id' + epid + ' Error: ' + ts.status + ' ' + ts.statusText,
        timeout: 7000,
      };
      console.log(ts.responseText);
      snackbarContainer.MaterialSnackbar.showSnackbar(data);
    }
  });
}
// Push media request
function pushRequestMedia(requestMediaData) {
  var requestMediaUrl = '/requestmedia/add/',
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
      $('#requst_media_submit').prop('disabled', false);
      $('#input_movie').val('');
      if ($('[data-page="request"]').length != 0) {
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
        }
    },
    error: function(ts) {
      var snackbarContainer = document.querySelector('#snackbar-error'),
          data = {
        message: 'Error: ' + ts.status + ' ' + ts.statusText,
        timeout: 7000,
      };
      console.log(ts.responseText);
      snackbarContainer.MaterialSnackbar.showSnackbar(data);
      $('#requst_media_submit').prop('disabled', false);
      $('#input_movie').val('');
    }
  });
}

// Event triggers
// Request sumbission trigger
$('#requst_media_submit').click(function(event) {
  var linkRegex = new RegExp(/^.*tt\d{7}.*$/i),
      requestMediaData = $('#input_movie').val();
  if (linkRegex.test(requestMediaData)) {
    event.preventDefault();
    $(this).prop('disabled', true);
    pushRequestMedia(requestMediaData);
  } else {
    event.preventDefault();
    $('#input_movie_error').show(0).text('Please input a valid imdb link!').delay(3000).fadeOut(500);
  }
});
// Media action triggers
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
