var practice_session_id = document.getElementById("practice_session_id");
var username = document.getElementById("username");
var bandName = document.getElementById("bandname");
var is_starter = document.getElementById("is_starter");
var starter_name = document.getElementById("starter_name");
var video_out = document.getElementById("vid-box");
var vid_thumb = document.getElementById("vid-thumb");
var vidCount = 0;

function start(num) {
    // PHONE({configs}) is a constructor from the PubNub WebRTC SDK
    var phone = window.phone = PHONE({
        number: num || "Anonymous", // list on username line else Anonymous
        publish_key: 'pub-c-484a8678-6f9f-4179-865b-78c3c76d063f',
        subscribe_key: 'sub-c-fcc92a58-c026-11e7-8aa3-828f8ebefef4',
    });

    // CONTROLLER(phone) is the wrapper library that attaches many useful functions
    // to phone object.
    // PHONE receives a config object with pub/sub keys and a phone number
    var ctrl = window.ctrl = CONTROLLER(phone);

    // Our local stream is ready and we can add it to our thumbnail div using ctrl.addLocalStream
    ctrl.ready(function () {
        ctrl.addLocalStream(vid_thumb);
        addLog("Start practice: " + username.innerText);
    });

    // receive the calling from others
    ctrl.receive(function (session) {
        session.connected(function (session) {
            video_out.appendChild(session.video);
            addLog(session.number + " has joined.");
            vidCount++;
        });
        session.ended(function (session) {
            ctrl.getVideoElement(session.number).remove();
            addLog(session.number + " has left.");
            vidCount--;
        });
    });

    //pause video
    ctrl.videoToggled(function (session, isEnabled) {
        ctrl.getVideoElement(session.number).toggle(isEnabled);
        addLog(session.number + ": video enabled - " + isEnabled);
    });

    //mute the audio
    ctrl.audioToggled(function (session, isEnabled) {
        ctrl.getVideoElement(session.number).css("opacity", isEnabled ? 1 : 0.75);
        addLog(session.number + ": audio enabled - " + isEnabled);
    });
    return;
}

function join(num) {
    // PHONE({configs}) is a constructor from the PubNub WebRTC SDK
    var phone = window.phone = PHONE({
        number: num, // list on username line else Anonymous
        publish_key: 'pub-c-484a8678-6f9f-4179-865b-78c3c76d063f',
        subscribe_key: 'sub-c-fcc92a58-c026-11e7-8aa3-828f8ebefef4',
    });

    // CONTROLLER(phone) is the wrapper library that attaches many useful functions
    // to phone object.
    // PHONE receives a config object with pub/sub keys and a phone number
    var ctrl = window.ctrl = CONTROLLER(phone);

    // Our local stream is ready and we can add it to our thumbnail div using ctrl.addLocalStream
    ctrl.ready(function () {
        ctrl.addLocalStream(vid_thumb);
        addLog("Join practice: " + username.innerText);

        ctrl.isOnline(starter_name.innerText, function (isOn) {
            if (isOn) ctrl.dial(starter_name.innerText);
            else alert("User if Offline");
        });
    });

    // receive the calling from others
    ctrl.receive(function (session) {
        session.connected(function (session) {
            video_out.appendChild(session.video);
            addLog(session.number + " has joined.");
            vidCount++;
        });
        session.ended(function (session) {
            ctrl.getVideoElement(session.number).remove();
            addLog(session.number + " has left.");
            vidCount--;
        });
    });

    //pause video
    ctrl.videoToggled(function (session, isEnabled) {
        ctrl.getVideoElement(session.number).toggle(isEnabled);
        addLog(session.number + ": video enabled - " + isEnabled);
    });

    //mute the audio
    ctrl.audioToggled(function (session, isEnabled) {
        ctrl.getVideoElement(session.number).css("opacity", isEnabled ? 1 : 0.75);
        addLog(session.number + ": audio enabled - " + isEnabled);
    });

    return;
}

function mute() {
    var audio = ctrl.toggleAudio();
    if (!audio) $("#mute").html("Unmute");
    else $("#mute").html("Mute");
}

function end() {
    ctrl.hangup();

    end_message = "You have ended the practice session.";
    addLog(end_message);
    $.get("/TEMPO/end_practice/" + practice_session_id.innerHTML);
}

function hang() {
    ctrl.hangup();

    end_message = "You have left the practice session.";
    addLog(end_message);
}

function back() {
    hang();
    window.location.replace('/TEMPO/practice_session/');
}

function pause() {
    var video = ctrl.toggleVideo();
    if (!video) $('#pause').html('Unpause');
    else $('#pause').html('Pause');
}

function addLog(log) {
    $('#logs').append("<p>" + log + "</p>");
}

function errWarp(fxn, form) {
    try {
        return fxn(form);
    } catch (err) {
        alert("The TEMPO is currently only supported by chrome, Opera, and Firefox");
        return false;
    }
}

$(document).ready(function () {
    if (is_starter.innerText === "T") {
        $('#end').click(end);
        start(starter_name.innerText);

        var starter = "T";
        var bandSocket = new WebSocket("ws://"+window.location.hostname+":8000/practice/?bandName=" + bandName.innerHTML + "&start=" + starter
                                        + "&practiceID=" + practice_session_id.innerHTML);
    }
    if (is_starter.innerText === "F") {
        $('#end').click(hang);
        join(username.innerText);
    }
});