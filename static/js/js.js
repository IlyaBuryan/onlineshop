"use strict"

// Mobile Nav toggle
$('.menu-toggle > a').on('click', function (event) {
    event.preventDefault();
    $('#responsive-nav').toggleClass('active');
    $('#responsive-nav-products').toggleClass('active');
})

// Fix cart dropdown from closing
$('.cart-dropdown').on('click', function (event) {
    event.stopPropagation();
});