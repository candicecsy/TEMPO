$(document).ready(function () {

    $('#calendar').fullCalendar({
        editable: false,
        eventLimit: true, // allow "more" link when too many events
        contentHeight: 500,

        eventSources: [
            {
                url: '/TEMPO/band_events/',
                color: 'black',
            }
        ]
    });

    $('#user-calendar').fullCalendar({
        editable: false,
        eventLimit: true, // allow "more" link when too many events
        contentHeight: 500,

        eventSources: [
            {
                url: '/TEMPO/user_events/',
                color: 'black',
            }
        ],

        eventClick: function (event, jsEvent, view) {
            $('#eventName').html(event.title);
            $('#eventDate').html(event.date);
            $('#eventLocation').html(event.location);
            $('#bandName').html(event.band_name);
            $('#bandDescription').html(event.band_description);

            $('#delete-btn').on('click', function (e) {
                // CSRF set-up copied from Django docs
                function getCookie(name) {
                    var cookieValue = null;
                    if (document.cookie && document.cookie != '') {
                        var cookies = document.cookie.split(';');
                        for (var i = 0; i < cookies.length; i++) {
                            var cookie = jQuery.trim(cookies[i]);
                            // Does this cookie string begin with the name we want?
                            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                                break;
                            }
                        }
                    }
                    return cookieValue;
                }

                var csrftoken = getCookie('csrftoken');
                $.ajaxSetup({
                    beforeSend: function (xhr, settings) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                });

                $.post("/TEMPO/delete-from-user-calendar/", {"event_id": event.id})
                    .done(function (data) {
                        alert("Delete successfully!");
                    });
                $('#user-calendar').fullCalendar('removeEvents', event.id);
                $('#userCalendarModal').modal('hide');
            });
            $('#userCalendarModal').modal();
        }
    });

});