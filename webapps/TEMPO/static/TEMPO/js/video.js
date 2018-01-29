var is_starter = document.getElementById("is_starter");
var username = document.getElementById("username");
var event_id = document.getElementById("event_id");
var bandName = document.getElementById("bandName");
var video_div = $(".video-div");
var start_ctrl;

function stream(event_id) {
    var video_out = document.getElementById("vid-box");
    var phone = window.phone = PHONE({
        number: event_id, // Listen on username else random
        publish_key: 'pub-c-484a8678-6f9f-4179-865b-78c3c76d063f',
        subscribe_key: 'sub-c-fcc92a58-c026-11e7-8aa3-828f8ebefef4',
        oneway: true,
        broadcast: true
    });
    var ctrl = window.ctrl = CONTROLLER(phone);
    start_ctrl = ctrl;
    ctrl.ready(function () {
        ctrl.addLocalStream(video_out); // Place local stream in the video_out div
        ctrl.stream();  // Subscribe to a stream channel to begin broadcasting
    });
    ctrl.receive(function (session) {
        session.ended(function (session) {
            ctrl.getVideoElement(session.number).remove();
        });
    });
    // // Subscribe to presence events on local stream, hands all presence events to the
    // // callback function.
    // ctrl.streamPresence(function(m) {
    //     // Pull off the current occupancy in the local stream channel and display it
    //     // in the here_nwo div.
    //     here_now.innerHTML = m.occupancy;
    // });
    return; // Form does not submit
}

function watch(event_id) {
    var video_out = document.getElementById("vid-box");
    var phone = window.phone = PHONE({
        number: "Viewer" + Math.floor(Math.random() * 100), // Listen on username else random
        publish_key: 'pub-c-484a8678-6f9f-4179-865b-78c3c76d063f',
        subscribe_key: 'sub-c-fcc92a58-c026-11e7-8aa3-828f8ebefef4',
        oneway: true,
    });
    var ctrl = window.ctrl = CONTROLLER(phone, true);
    ctrl.ready(function () {
        ctrl.isStreaming(event_id, function (isOn) {
            if (isOn) ctrl.joinStream(event_id);
            else alert("User is not streaming!");
        });
    });
    ctrl.receive(function (session) {
        session.connected(function (session) {
            video_out.appendChild(session.video);
        });

        session.ended(function (session) {
            var end_message = document.createElement("h3");
            end_message.innerHTML = "Live streaming has ended!";
            video_div.prepend(end_message);
            ctrl.getVideoElement(session.number).remove();
        });
    });
    return;
}

function end() {
    start_ctrl.hangup();

    var end_message = document.createElement("h3");
    end_message.innerHTML = "Live streaming has ended. :(";
    video_div.prepend(end_message);

    $.get("/TEMPO/end_event/" + event_id.innerHTML)
        .done(function() {
            window.location.replace("/TEMPO/live_session/");
        });
}

function guest_back() {
    window.location.replace('/TEMPO/live_session/');
}

String.prototype.trim = function (char, type) {
    if (char) {
        if (type == 'left') {
            return this.replace(new RegExp('^\\'+char+'+', 'g'), '');
        } else if (type == 'right') {
            return this.replace(new RegExp('\\'+char+'+$', 'g'), '');
        }
        return this.replace(new RegExp('^\\'+char+'+|\\'+char+'+$', 'g'), '');
    }
    return this.replace(/^\s+|\s+$/g, '');
};

$(document).ready(function () {
    var mySocket = new WebSocket("ws://"+window.location.hostname+":8000/chat/?roomNumber=" + event_id.innerHTML
                                 + "&username=" + username.innerHTML + "&create=" + is_starter.innerHTML);
    mySocket.onmessage = function (event) {
        var messageFromServer = JSON.parse(event.data);
        if (messageFromServer.state === "create") {
            var list_element = document.createElement('li');
            list_element.classList.add('system-message');
            list_element.innerHTML = "<span>" + messageFromServer.username + " create No." + event_id.innerHTML + " live video room." + "</span>";
            $("#message-list ul").prepend(list_element);
        } else if (messageFromServer.state === "join") {
            var list_element = document.createElement('li');
            list_element.classList.add('system-message');
            list_element.innerHTML = "<span>" + messageFromServer.username + " joined in the room." + "</span>";
            $("#message-list ul").prepend(list_element);
        } else {
            var list_element = document.createElement('li');
            list_element.innerHTML = "<span>" + messageFromServer.username + ": " + messageFromServer.message + "</span>";
            $("#message-list ul").prepend(list_element);
        }
    };

    var inputBox = document.getElementById("inputbox");
    var inputBtn = document.getElementById("inputbtn");
    inputBtn.addEventListener("click", function (e) {
        if (!e) {
            var e = window.event;
        }

        // enter/return probably starts a new line by default
        e.preventDefault();
        var message = inputBox.value;
        if (message.trim() == "") {
            alert('Message cannot be empty!');
            return;
        }
        var data = JSON.stringify({'message': message, 'username': username.innerHTML, 'roomNumber': event_id.innerHTML});
        mySocket.send(data);
        inputBox.value = "";
    }, false);

    if (is_starter.innerText === "Broadcaster") {
        stream(event_id.innerText);
    }
    if (is_starter.innerText === "Guest") {
        $('#back').click(guest_back);
        watch(event_id.innerText);
    }

    if (is_starter.innerHTML === "Broadcaster") {
        var start = "T";
        var bandSocket = new WebSocket("ws://"+window.location.hostname+":8000/live/?bandName=" + bandName.innerHTML + "&start=" + start + "&username=" + username.innerHTML);
    }
});