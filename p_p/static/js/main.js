(function ($) {
  "use strict";

// Uyarılar
    setTimeout(function () {
      $(".alert").hide(750);
    }, 750);

// Ana sayfadaki tablar
    var triggerTabList = [].slice.call(document.querySelectorAll('#first'))
    triggerTabList.forEach(function (triggerEl) {
      var tabTrigger = new bootstrap.Tab(triggerEl)
    
      triggerEl.addEventListener('click', function (event) {
        event.preventDefault()
        tabTrigger.show()
      })
    })

    var triggerTabList = [].slice.call(document.querySelectorAll('#second'))
    triggerTabList.forEach(function (triggerEl) {
      var tabTrigger = new bootstrap.Tab(triggerEl)
    
      triggerEl.addEventListener('click', function (event) {
        event.preventDefault()
        tabTrigger.show()
      })
    })

    var triggerTabList = [].slice.call(document.querySelectorAll('#third'))
    triggerTabList.forEach(function (triggerEl) {
      var tabTrigger = new bootstrap.Tab(triggerEl)
    
      triggerEl.addEventListener('click', function (event) {
        event.preventDefault()
        tabTrigger.show()
      })
    })

  })(jQuery);

  

  

  
