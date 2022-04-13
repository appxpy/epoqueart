(function($) {
  $.fn.toggleAttrVal = function(attr, val1, val2) {
    var test = $(this).attr(attr);
    if ( test === val1) {
      $(this).attr(attr, val2);
      return this;
    }
    if ( test === val2) {
      $(this).attr(attr, val1);
      return this;
    }
    $(this).attr(attr, val1);
    return this;
  };
function getAverageRGB(imgEl) {
  var blockSize = 5,
    defaultRGB = {
      r: 0,
      g: 0,
      b: 0
    },
    canvas = document.createElement('canvas'),
    context = canvas.getContext && canvas.getContext('2d'),
    data, width, height,
    i = -4,
    length,
    rgb = {
      r: 0,
      g: 0,
      b: 0
    },
    count = 0;

  if (!context) {
    return defaultRGB;
  }

  height = canvas.height = imgEl.naturalHeight || imgEl.offsetHeight || imgEl.height;
  width = canvas.width = imgEl.naturalWidth || imgEl.offsetWidth || imgEl.width;

  context.drawImage(imgEl, 0, 0);

  try {
    data = context.getImageData(0, 0, width, height);
  } catch (e) {
    alert('x');
    return defaultRGB;
  }
  length = data.data.length;
  while ((i += blockSize * 4) < length) {
    ++count;
    rgb.r += data.data[i];
    rgb.g += data.data[i + 1];
    rgb.b += data.data[i + 2];
  }
  rgb.r = ~~(rgb.r / count);
  rgb.g = ~~(rgb.g / count);
  rgb.b = ~~(rgb.b / count);
  return rgb
}

function setAverageColor() {
  var rgb = lighter(getAverageRGB(document.getElementsByClassName('splide__slide is-active is-visible')[0].children[0]));
  var root = document.documentElement;
  var h = 'rgb(' + rgb.r + ',' + rgb.g + ',' + rgb.b + ')'
  root.style.setProperty('--adaptive-color', h)
}

function lighter(color) {

  var r, g, b, percent;
  percent = 55;
  r = color.r;
  g = color.g;
  b = color.b;
  rgb = {
    r: r + (256 - r) * percent / 100,
    g: g + (256 - g) * percent / 100,
    b: b + (256 - b) * percent / 100,
  }

  return rgb;
}

function rs() {
  let vh = window.innerHeight * 0.01;
  document.documentElement.style.setProperty('--vh', vh+'px');
}
$(window).resize(function() {
  rs()
});
  rs()
  var outerSlider = new Splide('#outer-slider', {
    autoplay: true,
    interval: 30000,
    pauseOnHover: false,
    pauseOnFocus: false,
    width: '90vw',
    height: '70vh',
    type: 'fade',
    rewind: true,
    pagination: false,
    arrows: 'slider',
    keyboard: true,
  });
  outerSlider.on('moved', function () {
    setAverageColor()
  });
  outerSlider.mount();
  outerSlider.on('autoplay:play autoplay:pause', function () {
    $('.toggle-button').toggleClass("bi-play-fill bi-pause-fill")
  });

  $('a.slider__toggle-desc').on('click', function () {
    $('.slider__desc', $(this).parent()).toggleAttrVal("expanded", "true", "false");
    var text = $(this).text();
    $(this).text(
        text == "Contract" ? "Expand" : "Contract");
  });

  if ($('#outer-slider').hasClass('no-results')) {
    $('.splide__arrows').css('display', 'none');
    $('#navigation-panel').empty();
  }
  
  if ($('.splide__list').children().length == 1) {
    $('.splide__arrows').css('display', 'none');
    $('.toggle-button').css('display', 'none');
  }

  $(window).keypress(function (e) {
    var Autoplay = outerSlider.Components.Autoplay;
    if (e.which == 32) {
      if (Autoplay.isPaused()) {
        Autoplay.play();
      } else {
        Autoplay.pause();
      }
    }
  });

  $('.toggle-button').on('click', function () {
    var Autoplay = outerSlider.Components.Autoplay;
    if (Autoplay.isPaused()) {
      Autoplay.play();
    } else {
      Autoplay.pause();
    }
  });
  $(function () {
    $('#outer-slider').hover(function () {
      $('.splide__arrows').css('opacity', 1);
    }, function () {
      $('.splide__arrows').css('opacity', 0);
    });
  });
  var is_mobile = false;

  if( $('div.is-mobile').css('display')=='none') {
    is_mobile = true;
  }
  var timeout = null
  $(document).on('mousemove click', function () {
    if (timeout !== null) {
      $('.splide__arrows').css("opacity", 1);
      $('html').css({
        cursor: 'default'
      });
      $('#navigation-panel').show();
      $('#header-panel').show();
      clearTimeout(timeout);
    }

    timeout = setTimeout(function () {
      if (!is_mobile & !$('.sidebar').hasClass('active') & !($('#outer-slider').hasClass('no-results'))) {
        $('.splide__arrows').css("opacity", 0);
        $('html').css({
          cursor: 'none'
        });
        $('#navigation-panel').hide();
        $('#header-panel').hide();
      };
    }, 5000);
  });

  function fullscreen() {
    document.fullScreenElement && null !== document.fullScreenElement || !document.mozFullScreen && !document.webkitIsFullScreen ? ($("#fullscreen-button").attr("class", "bi bi-arrows-fullscreen"), document.documentElement.requestFullScreen ? document.documentElement.requestFullScreen() : document.documentElement.mozRequestFullScreen ? document.documentElement.mozRequestFullScreen() : document.documentElement.webkitRequestFullScreen && document.documentElement.webkitRequestFullScreen(Element.ALLOW_KEYBOARD_INPUT)) : ($("#fullscreen-button").attr("class", "bi bi-fullscreen-exit"), document.cancelFullScreen ? document.cancelFullScreen() : document.mozCancelFullScreen ? document.mozCancelFullScreen() : document.webkitCancelFullScreen && document.webkitCancelFullScreen())
  };
  $(document).on("fullscreenchange webkitfullscreenchange mozfullscreenchange MSFullscreenChange", function () {
    FSHandler()
  });

  function FSHandler() {
    if (!document.fullscreenElement && !document.webkitIsFullScreen && !document.mozFullScreen && !document.msFullscreenElement) {
      $('#fullscreen-button').attr("class", "bi bi-arrows-fullscreen")
    } else {
      $('#fullscreen-button').attr("class", "bi bi-fullscreen-exit")
    }
  }
  $('#fullscreen-button').on('click', function () {
    fullscreen();
  });
  $("button").each(function (index) {
    $(this).on("focus", function () {
      $(this).blur();
    });
  });

$(window).on('load', function () {
  sa();
  sb();
  sc();
  sd();
})
$("#log-out").mouseenter(function () {
  $('#log-out-arrow').css("transform", "translate(3px)");
  $('#log-out-box').css("transform", "translate(-1px)");
}).mouseleave(function () {
  $('#log-out-arrow').css("transform", "translate(0px)");
  $('#log-out-box').css("transform", "translate(0px)");
});

$("#log-in").mouseenter(function () {
  $('#log-in-arrow').css("transform", "translate(2px)");
  $('#log-in-box').css("transform", "translate(-1px)");
}).mouseleave(function () {
  $('#log-in-arrow').css("transform", "translate(0px)");
  $('#log-in-box').css("transform", "translate(0px)");
});

$(".menu-button").on("click", function () {
  $(".sidebar").toggleClass("active hidden");
  $(this).toggleClass("sidebar-color");
});
$('#dropdown-collapse').on("show.bs.collapse hide.bs.collapse", function () {
  $('.filter').toggleClass('active hidden')
});
$('#slider_price_min').on('input', function () {
  sa();
});
$('#slider_price_max').on('input', function () {
  sb();
});
$('#slider_year_min').on('input', function () {
  sc();
});
$('#slider_year_max').on('input', function () {
  sd();
});

function sa() {
  if ($('#slider_price_max').val() - $('#slider_price_min').val() <= 1) {
    $('#slider_price_min').val($('#slider_price_max').val() - 1);
  }
  document.getElementById("slider_price_min_value").textContent = $('#slider_price_min').val() + '$';
  fc(1);
}

function sb() {
  if ($('#slider_price_max').val() - $('#slider_price_min').val() <= 1) {
    $('#slider_price_max').val($('#slider_price_min').val() + 1);
  }
  document.getElementById("slider_price_max_value").textContent = $('#slider_price_max').val() + '$';
  fc(1);
}

function sc() {
  if (parseInt(document.getElementById("slider_year_max").value) - parseInt(document.getElementById("slider_year_min").value) <= 1) {
    document.getElementById("slider_year_min").value = parseInt(document.getElementById("slider_year_max").value) - 1;
  }
  document.getElementById("slider_year_min_value").textContent = document.getElementById("slider_year_min").value;
  fc(2);
}

function sd() {
  if (parseInt(document.getElementById("slider_year_max").value) - parseInt(document.getElementById("slider_year_min").value) <= 1) {
    document.getElementById("slider_year_max").value = parseInt(document.getElementById("slider_year_min").value) + 1;
  }
  document.getElementById("slider_year_max_value").textContent = document.getElementById("slider_year_max").value;
  fc(2);
}

function fc(id) {
  switch (id) {
    case 1:
      k = (($('#slider_price_min').val() - $('#slider_price_max').attr("min")) / ($('#slider_price_max').attr("max") - $('#slider_price_max').attr("min")) * 100);
      j = (($('#slider_price_max').val() - $('#slider_price_max').attr("min")) / ($('#slider_price_max').attr("max") - $('#slider_price_max').attr("min")) * 100);
      $('#slider_track__price').css('background', 'linear-gradient(to right, #dadae5 ' + k + '% , #3264fe ' + k + '% , #3264fe ' + j + '%, #dadae5 ' + j + '%)');
      break;
    case 2:
      k = (($('#slider_year_min').val() - $('#slider_year_max').attr("min")) / ($('#slider_year_max').attr("max") - $('#slider_year_max').attr("min")) * 100);
      j = (($('#slider_year_max').val() - $('#slider_year_max').attr("min")) / ($('#slider_year_max').attr("max") - $('#slider_year_max').attr("min")) * 100);
      $('#slider_track__year').css('background', 'linear-gradient(to right, #dadae5 ' + k + '% , #3264fe ' + k + '% , #3264fe ' + j + '%, #dadae5 ' + j + '%)');
      break;
  };
};

var j = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]')).map(function (e) {
  return new bootstrap.Tooltip(e);
})

$("#label-switch-button").on("click", function () {
  $(this).toggleClass("bi-eye bi-eye-slash")
  $(".slider__label").toggleClass("hidden")
  if ($(this).hasClass("bi-eye")) {
    $(this).attr("data-bs-original-title", "Hide labels");
  } else {
    $(this).attr("data-bs-original-title", "Show labels");
  };
});

$(".search-input").on("focus", function () {
  value = $.trim($(this).val());
  $(".search-results-container").addClass('active');
});

$(document).on("click", function (e) {
  if (!$(e.target).closest($(".search")).length) {
    $(".search-results-container").removeClass("active");
  }
});

$("#search-input").on("keyup", function (e) {
  val = $.trim($(this).val());
  if (val.length > 0) {
    $.post('/api/gallery/search', {
      q: val
    }, function (data) {
      switch (data.status) {
        case 0:
          console.log("Error occured while trying to reach API.");
          break;
        case 1:
          if ($(".search-results-container").html() != data.payload.data) {
            $(".search-results-container").html(data.payload.data);
          };
      };
    }).fail(function (data) {
      console.log("Error occured while trying to reach API.");
    });
  } else {
    $(".search-results-container").html("<i class='bi bi-search mx-auto'></i><span class='search-results__empty mx-auto'>Type something</span><span class='search-result__empty_sub mx-auto'>E.g. \"Love in yellow\"</span>");
  }
});
})(jQuery);