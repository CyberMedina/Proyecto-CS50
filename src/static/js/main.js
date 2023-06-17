(function ($) {
    "use strict";



    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({ scrollTop: 0 }, 1500, 'easeInOutExpo');
        return false;
    });

    // Date and time picker
    $('.date').datetimepicker({
        format: 'L'
    });
    $('.time').datetimepicker({
        format: 'LT'
    });

    // Testimonials carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1500,
        margin: 30,
        dots: true,
        loop: true,
        center: true,
        responsive: {
            0: {
                items: 1
            },
            576: {
                items: 1
            },
            768: {
                items: 2
            },
            992: {
                items: 3
            }
        }
    });
})(jQuery);

// Verificar si el parámetro 'modal' está presente en la URL
const urlParams = new URLSearchParams(window.location.search);
const modal = urlParams.get('modal');

// Si el parámetro 'modal' es 'true', mostrar el modal
if (modal === 'true') {
    document.addEventListener('DOMContentLoaded', function () {
        const myModal = new bootstrap.Modal(document.getElementById('iniciosesion2'));
        myModal.show();
    });
}

// Cerrar el modal al hacer clic en el botón de cierre
document.getElementById('closeModal').addEventListener('click', function () {
    const myModal = new bootstrap.Modal(document.getElementById('iniciosesion2'));
    myModal.hide();
});








