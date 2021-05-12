$(function () {


    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader('X-CSRFToken', csrf_token);
            }
        }
    });
    function update_info() {
        var $el = $('#result-description');
        $.ajax({
            type: 'GET',
            url: $el.data('href'),
            success: function (data) {
                $el.text(data.message)
            }
        });
    }

    if ( $("#result-description").length > 0 ) {
       setInterval(update_info, 3000);
    }

});
