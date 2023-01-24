$(document).ready(function() {
    let currentBalance = parseInt($('#loyaltyBalance').text());
    let redeemInput = $('#redeemInput');
    let redeemBtn = $('#redeemBtn');
    let redemmInfo = $('#redemmInfo');

    redeemBtn.attr('disabled', true);

    // Check the point redemption input value.
    // Change the font colour, button disable status and message depending
    // on the input value.
    redeemInput.change(function() {
        let redeemInputAmount = redeemInput.val();
        if ( redeemInputAmount > currentBalance ) {
            redeemBtn.attr('disabled', true);
            redemmInfo.removeClass('text-black');
            redemmInfo.addClass('text-danger');
            redemmInfo.text('You cannot redeem more than your current balance.');
            return;
        } 
        redeemBtn.attr('disabled', false);
        redemmInfo.removeClass('text-danger');
        redemmInfo.addClass('text-black');
        redemmInfo.text('A loyalty point is equivalent to €0.01');
    });

    // Change the redemption text to the user's input value.
    redeemBtn.click(function(e) {
        e.preventDefault();

        let loyaltyRedemption = $('#loyaltyRedemption');
        let redeemInputAmount = redeemInput.val();

        loyaltyRedemption.text(redeemInputAmount);
        redeemInput.val('');
        redeemBtn.attr('disabled', true);
    });
});