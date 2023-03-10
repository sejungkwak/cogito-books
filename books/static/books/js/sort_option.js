/**----------------------------------------------------------------------------
 * Changes the url parameter when the user selects an option in the dropbox
 * on the book list page.
 -----------------------------------------------------------------------------*/
$(document).ready(function() {
    $('#sort-selector').change(function() {
        let selector = $(this);
        let currentUrl = new URL(window.location);
        let selectedVal = selector.val();
    
        if ( selectedVal != 'reset' ) {
            let sort = selectedVal.split('-')[0];
            let direction = selectedVal.split('-')[1];
    
            currentUrl.searchParams.set('sort', sort);
            currentUrl.searchParams.set('direction', direction);
    
            window.location.replace(currentUrl);
        } else {
            currentUrl.searchParams.delete('sort');
            currentUrl.searchParams.delete('direction');
    
            window.location.replace(currentUrl);
        }
    });
});