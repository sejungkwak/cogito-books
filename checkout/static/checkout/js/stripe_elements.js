/*
Code from the Stripe docs below and Code Institute's walkthrough project Boutique Ado.
https://stripe.com/docs/payments/card-element?client=html&lang=python
*/

$(document).ready(function() {
    const stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
    const clientSecret = $('#id_client_secret').text().slice(1, -1);
    const stripe = Stripe(stripePublicKey);
    const elements = stripe.elements();
    const style = {
        base: {
            iconColor: '#8f96a3',
            color: '#212529',
            fontFamily: '"Montserrat", sans-serif',
            fontSize: '18px',
            fontSmoothing: 'antialiased',
            '::placeholder': {
                color: '#8f96a3',
            },
        },
        invalid: {
            iconColor: '#dc3545',
            color: '#dc3545',
        },
    }
    const card = elements.create('card', {style: style});

    card.mount('#card-element');

    /**
     * Handle realtime validation errors on the card element.
     */
    card.on('change', function(e) {
        if (e.error) {
            showError(e.error.message);
        } else {
            document.querySelector('#card-error').textContent = '';
        }
    })

    /**
     * Show the error from Stripe if the shopper's card fails to charge.
     */
    function showError(errorMsgText) {
        let errorEl = document.querySelector('#card-error');
        errorEl.textContent = errorMsgText;
    };

    /**
     * Show a spinner on payment submission and hide it when completed.
     */
    function loading(isLoading) {
        if ( isLoading ) {
            $('#payment-form').fadeOut(100);
            $('#loadingOverlay').addClass('loading-overlay-show');
            $('#loadingOverlay').fadeIn(100);
            $('#payment-button').prop('disabled', true);
        } else {
            $('#payment-form').fadeIn(100);
            $('#loadingOverlay').removeClass('loading-overlay-show');
            $('#loadingOverlay').fadeOut(100);
            $('#payment-button').prop('disabled', false);
        }
    }

})