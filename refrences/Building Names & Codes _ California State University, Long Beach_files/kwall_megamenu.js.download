(function ($) {
  Drupal.behaviors.kwall_megamenu = {
    attach: function (context, settings) {
      $('.accessible-mega-menu').once('accessible-mega-menu', function() {
        Drupal.settings.accessibleMegaMenu = $('.kwall-megamenu-wrapper', $(this)).accessibleMegaMenu();
      });
    }
  };
})(jQuery);