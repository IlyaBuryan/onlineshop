"use strict";

$('.basket-list').on('change', 'input[type="number"]', function (event) {
    let elem = event.target;

    $.ajax({
        url: "/basket/update/" + elem.name + "/" + elem.value + "/",

        success: function (data) {
            $('.basket-list').html(data.result);
        },
    });

});

