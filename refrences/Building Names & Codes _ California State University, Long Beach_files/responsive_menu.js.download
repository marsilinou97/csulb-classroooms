(function ($) {

  Drupal.responsive_menu = {
    menu_created: false,
    responsive_width: 2039,

    mobile_menu: function () {
      var mobile_menu = $('.mobile-menu-popout');
      var wrapper = $('.menu-block-wrapper', mobile_menu);

      if (Drupal.responsive_menu.menu_created) {
        if ($(window).width() >= Drupal.responsive_menu.responsive_width) {
          mobile_menu.hide();
        }

        return;
      }

      var mobile_menu_link = $('.mobile-menu-popout-link, .mobile-menu-close').click(function() {
        // Show the first level of links
        mobile_menu.toggle('fast');
        $('ul.menu', mobile_menu).removeClass('menu-show');
        $('ul.menu', mobile_menu).eq(0).addClass('menu-show');
        wrapper.css('left', 0);
        return false;
      });

      // add back button
      mobile_menu.find(".expanded").each(function () {
        var $levelParent = $(this).children("a");
        var linkSrc = ' href="' + $levelParent.attr('href') + '"';

        if ($levelParent.length == 0) {
          $levelParent = $(this).children("span");
          linkSrc = '';
        }

        var $backAndParentLink = '<li class="title"><a href="#" class="back">Back</a>';
        $backAndParentLink += '<' + $levelParent.prop('tagName') + linkSrc + ' class="responsive-menu-sub-menu-title" ><span>' + $levelParent.text() + "</span></" + $levelParent.tagName + "></li>";

        $(this).children("ul").prepend($backAndParentLink);
      });
/*
      // make page titles open the menu
      var current_page = $('ul.menu a.active', mobile_menu).eq(0);
      if (current_page[0]) {
        var parents = current_page.parents('ul.menu');
        if (parents.size() - 1 == 0) {
          // we need to add the section rather than the top level item, so find where the
          // title item is then use that to get the menu parents.
          parents = current_page.closest('li').children('ul.menu').children('li.title').parents('ul.menu');
        }
        $('h1#page-title').click(function() {
          if ($(window).width() > Drupal.responsive_menu.responsive_width) {
            $(this).css('cursor', '');
            mobile_menu.hide();
            return;
          }
          $(this).css('cursor', 'pointer');
          var depth = parents.size() - 1;
          mobile_menu.show();
          $('ul.menu', mobile_menu).removeClass('menu-show');
          parents.addClass('menu-show');
          wrapper.css('left', (-1 * depth * Drupal.responsive_menu.responsive_width) + 'px');
        }).css('cursor', 'pointer');
      }

      // hide the li for no-mobile items
      $.each($('a.no-mobile', mobile_menu), function() {
        $(this).closest('li').hide();
      });
*/

      $('ul.menu a, ul.menu span', mobile_menu).click(function(event) {
        // make menus open sub items
        var position = wrapper.css("left");
        position = parseInt(position.replace("px", ""));
        var next_position = 0;

        var parent = $(this).closest('li');
        if (parent.hasClass('expanded') && $('ul.menu', parent).eq(0).size() > 0) {
          event.preventDefault();

          var current_width = $(window).width();
          next_position = position - current_width;
          $('ul.menu', parent).css('left', current_width);
          wrapper.stop().animate({
            left: next_position
          }, 250, function () {
            $('ul.menu', parent).eq(0).addClass('menu-show');
          });

          return false;
        }
        else if (parent.hasClass('title') && $(this).hasClass('back')) {
          // add back button functionality
          var current_width = $(window).width();
          parent.closest('ul.menu').removeClass('menu-show');
          wrapper.stop().animate({
            left: position + current_width
          }, 250, function () {
          });
          return false;
        }
      });

      Drupal.responsive_menu.menu_created = true;
    }
  }

  Drupal.behaviors.responsive_menu = {
    attach: function (context, settings) {
      if ($(window).width() <= Drupal.responsive_menu.responsive_width) {
        Drupal.responsive_menu.mobile_menu();
      }
    }
  }

  $(window).resize(function() {
    Drupal.responsive_menu.mobile_menu();
  });
})(jQuery);
