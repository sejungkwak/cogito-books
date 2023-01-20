/**----------------------------------------------------------------------------
 * Handle the user's interaction with the quantity input box.
 -----------------------------------------------------------------------------*/
$(document).ready(function() {

    /**
     * Disable the +/- buttons when the input value is outside the range of 1-99.
     * @param {number} itemID The primary key(id) of the specified book.
     */
    function DisableBtnHandler(itemID) {
        let currentValue = parseInt($(`#id_qty_${itemID}`).val());
        let minusBtnDisabled = currentValue < 2;
        let plusBtnDisabled = currentValue > 98;
        $(`#decrement-qty_${itemID}`).prop('disabled', minusBtnDisabled);
        $(`#increment-qty_${itemID}`).prop('disabled', plusBtnDisabled);
    }

    // Ensure the +/- buttons' disabling statuses are correct on page load.
    for ( let qtyinputEl of $('.qty_input') ) {
        let itemID = $(qtyinputEl).data('item_id');
        DisableBtnHandler(itemID);
    }

    // Handle the +/- buttons' disabling statuses when the input is changed.
    $('.qty_input').change(function() {
        let itemId = $(this).data('item_id');
        DisableBtnHandler(itemId);
    });

    // Increment quantity.
    $('.increment-qty').click(function(e) {
        e.preventDefault();

        let closestInput = $(this).closest('.input-group').find('.qty_input')[0];
        let currentValue = parseInt($(closestInput).val());
        let itemId = $(this).data('item_id');

        $(closestInput).val(currentValue + 1);
        DisableBtnHandler(itemId);
    });

    // Decrement quantity.
    $('.decrement-qty').click(function(e) {
        e.preventDefault();

        let closestInput = $(this).closest('.input-group').find('.qty_input')[0];
        let currentValue = parseInt($(closestInput).val());
        let itemId = $(this).data('item_id');

        $(closestInput).val(currentValue - 1);
        DisableBtnHandler(itemId);
    });

})