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
    };
    const card = elements.create('card', {style: style});
    const form = document.getElementById('payment-form');

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
    });

    /**
     * Handle the form submission.
     */
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        payWithCard(stripe, card, clientSecret);
    });

    /**
     * Handle the post request. If successful, submit the form.
     * If not, reload the page and the error message will be in django messages.
     */
    function payWithCard(stripe, card, clientSecret) {
        let saveInfo = Boolean($('#saveInfo').is(':checked'));
        let csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
        let postData = {
            'csrfmiddlewaretoken': csrfToken,
            'client_secret': clientSecret,
            'save_info': saveInfo,
        };
        let url = '/checkout/cache_checkout_data/';

        loading(true);
        card.update({'disabled': true});

        $.post(url, postData).done(function() {
            stripe.confirmCardPayment(clientSecret, {
                payment_method: {
                    card: card,
                    billing_details: {
                        name: $.trim(form.full_name.value),
                        email: $.trim(form.email.value),
                        phone: $.trim(form.phone_number.value),
                        address: {
                            line1: $.trim(form.address_line_1.value),
                            line2: $.trim(form.address_line_2.value),
                            city: $.trim(form.town_or_city.value),
                            state: $.trim(form.county.value),
                            country: $.trim(form.country.value),
                        }
                    }
                },
                shipping: {
                    name: $.trim(form.full_name.value),
                    phone: $.trim(form.phone_number.value),
                    address: {
                        line1: $.trim(form.address_line_1.value),
                        line2: $.trim(form.address_line_2.value),
                        city: $.trim(form.town_or_city.value),
                        state: $.trim(form.county.value),
                        postal_code: $.trim(form.postcode.value),
                        country: $.trim(form.country.value),
                    }
                }
            }).then(function(result) {
                if (result.error) {
                    showError(result.error.message);
                    loading(false);
                    card.update({'disabled': false});
                } else {
                    if (result.paymentIntent.status === 'succeeded') {
                        form.submit();
                    }
                }
            });
        }).fail(function() {
            location.reload();
        });
    }

    /**
     * Show the error from Stripe if the shopper's card fails to charge.
     */
    function showError(errorMsgText) {
        let errorEl = document.querySelector('#card-error');
        errorEl.textContent = errorMsgText;
    }

    /**
     * Show a spinner on payment submission and hide it when completed.
     */
    function loading(isLoading) {
        if ( isLoading ) {
            $('#loadingOverlay').addClass('loading-overlay-show');
            $('#loadingOverlay').fadeIn(100);
            $('#payment-button').prop('disabled', true);
        } else {
            $('#loadingOverlay').removeClass('loading-overlay-show');
            $('#loadingOverlay').fadeOut(100);
            $('#payment-button').prop('disabled', false);
        }
    }

});