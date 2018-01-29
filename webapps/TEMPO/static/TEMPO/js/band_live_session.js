var mySocket;
var bandName;

function delete_event(id) {
    var socket = mySocket;
    var name = bandName;
    $.post('/TEMPO/delete_event/' + id)
        .done(function (data) {
            // Socket
            message = "delete";
            data = JSON.stringify({'message': message, 'bandName': name.value});
            socket.send(data);
        });
}

$(document).ready(function () {
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

    bandName = document.getElementById("bandname");
    mySocket = new WebSocket("ws://"+window.location.hostname+":8000/live/?bandName=" + bandName.value);
    mySocket.onmessage = function (event) {
        var messageFromServer = JSON.parse(event.data);
        if (messageFromServer.state === "start") {
            window.location.replace('/TEMPO/live_session/');
        } else if (messageFromServer.state === "delete") {
            window.location.replace('/TEMPO/live_session/');
        } else if (messageFromServer.state === "end") {
            window.location.replace('/TEMPO/live_session/');
        }
    };

});