
//AJAX TO RETRIEVE CPU DATA
function statusUpdateCpu(){
  $.getJSON('/status/cpu', function(data){
    var index = 0;
    $.each( data.cpu_usage, function() {
      var percent = this,
      svgPath = document.getElementById('cpu' + ++index),
      percentText = document.getElementById('cpu' + index + '_text'),
      oldPercent = percentText.innerHTML,
      oldPercent = oldPercent.replace('%',''),
      path = new ProgressBar.Path(svgPath, {
        easing: 'easeInOut'
      });
      path.set(percent / 100)
      $({transitionPercent: oldPercent}).animate({transitionPercent: percent}, {
        duration: 700,
        step: function() {
          $(percentText).text(parseFloat(Math.round(this.transitionPercent * 10) / 10).toFixed(1) +'%');
        }
      });
    });
  });
}
// AJAX TO RETRIEVE TEMP DATA
function statusUpdateTemp(){
  $.getJSON('/status/temperatures', function(data){
    var index = 0;
    $.each( data, function() {
      var percent = this,
      percentText = document.getElementById('temp' + ++index),
      oldPercent = percentText.innerHTML;
      $({transitionPercent: oldPercent}).animate({transitionPercent: percent}, {
        duration: 700,
        step: function() {
          $(percentText).text(parseFloat(Math.round(this.transitionPercent * 10) / 10).toFixed(1) );
        }
      });
    });
  });
}
// AJAX TO RETRIEVE FAN DATA
function statusUpdateRpm(){
  $.getJSON('/status/fanspeed', function(data){
    var index = 0;
    $.each( data, function() {
      var percent = this,
      percentText = document.getElementById('fan' + ++index),
      oldPercent = percentText.innerHTML;
      $({transitionPercent: oldPercent}).animate({transitionPercent: percent}, {
        duration: 700,
        step: function() {
          $(percentText).text(parseFloat(Math.round(this.transitionPercent * 10) / 10).toFixed(1) );
        }
      });
    });
  });
}
// UPDATE RAM USAGE
function updateRam(){
  var ramText = document.getElementById('ram_text'),
  ramSvgPath = document.getElementById('ram'),
  ramPercent = ramSvgPath.getAttribute('data-value'),
  ramPath = new ProgressBar.Path(ramSvgPath, {
    easing: 'easeInOut'
  });
  ramPath.set(ramPercent / 100)
  $({transitionPercent: 0}).animate({transitionPercent: ramPercent}, {
    duration: 700,
    step: function() {
      $(ramText).text(parseFloat(Math.round(this.transitionPercent * 10) / 10).toFixed(1) +'%');
    }
  });
}
// UPDATE DISK USAGE
function updateDisk(){
  var children = $('#disk_usage svg'),
  index = 0;
  $.each(children, function() {
    var diskText = document.getElementById('disk' + ++index + '_text'),
    diskSvgPath = document.getElementById('disk' + index),
    diskPercent = diskSvgPath.getAttribute('data-value'),
    diskPath = new ProgressBar.Path(diskSvgPath, {
      easing: 'easeInOut'
    });
    diskPath.set(diskPercent / 100)
    $({transitionPercent: 0}).animate({transitionPercent: diskPercent}, {
      duration: 700,
      step: function() {
        $(diskText).text(parseFloat(Math.round(this.transitionPercent * 10) / 10).toFixed(1) +'%');
      }
    });
  });
}
// RUN FUNCTIONS AFTER WINDOWS HAS LOADED
$(window).load(statusUpdateCpu);
$(window).load(statusUpdateTemp);
$(window).load(statusUpdateRpm);
$(window).load(updateRam);
$(window).load(updateDisk);
// SCHEDULED FUNCTION EXECUTION
setInterval(statusUpdateCpu, 2500);
setInterval(statusUpdateTemp, 2500);
setInterval(statusUpdateRpm, 2500);
