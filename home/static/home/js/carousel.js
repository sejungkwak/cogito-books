// Display multiple cards in Bootstrap carousel
// Source: Mathias Madsen's Codepen
// https://codepen.io/mathiasmadsen/pen/xxRLKEg

if ( window.matchMedia('(min-width: 768px)').matches ) {
    let cardsPerCarousel = window.matchMedia('(min-width: 992px)').matches ? 4 : 2;

    $('.carousel .carousel-item').each(function() {
        let next = $(this).next();
        if ( !next.length ) {
            next = $(this).siblings(':first');
        }
        next.children(':first-child').clone().appendTo($(this));

        for ( let i = 0; i < cardsPerCarousel; i++ ) {
            next = next.next();
            if ( !next.length ) {
                next = $(this).siblings(':first');
            }
            next.children(':first-child').clone().appendTo($(this));
        }
    });
}