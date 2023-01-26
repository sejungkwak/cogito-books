// Close the alert automatically after 3 seconds.
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