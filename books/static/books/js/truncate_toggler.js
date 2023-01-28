/**----------------------------------------------------------------------------
 * Toggles the truncated book description.
 * Runs when the user clicks the 'Read more/less' button on the details page.
 -----------------------------------------------------------------------------*/
$(document).ready(function() {
    $('.show-hide-btn').click(function() {
        $('.half-desc').toggle();
        $('.full-desc').toggle();
      });
});