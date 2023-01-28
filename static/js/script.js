// Close the alert automatically after 5 seconds.
$(document).ready(function() {
    setTimeout(function() {
        $('#msg').alert('close');
    }, 5000);
});

// Allauth alert styling
$(document).ready(function() {
    $('.login .alert-error').addClass('alert-danger');
    $('.login .alert-error ul').css({'list-style': 'none', 'margin': 0, 'padding': 0});
    $('.signup .help-block').addClass('alert alert-danger');
});

// Fix for the mobile dropdown menu not auto-closing issue.
// Hide dropdown menu if another element is selected if the menu is open.
$(document).ready(function() {
    $(document).on('click', function(e) {
        let dropdownMainMenu = $('#dropdownMainMenu');
        if (!dropdownMainMenu.is(e.target) && dropdownMainMenu.has(e.target).length === 0 && dropdownMainMenu.hasClass('show')) {
            dropdownMainMenu.removeClass('show');
        }
    });
});