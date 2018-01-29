function reset_input() {
    $('table input').val("");
}

function add_new_song(event_id) {
    var data = new FormData($('#add-new-song-form').get(0));

    $.ajax({
        type: "POST",
        url: "/TEMPO/add-new-song/" + event_id,
        data: data,
        cache: false,
        processData: false,
        contentType: false,
        success: function (result) {
            if (result === 'Add successfully!') {
                    window.location.replace('/TEMPO/songs/' + event_id);
                } else {
                    alert(result);
                }
        },
        error: function (error) {
            // alert(error);
        }
    })
}

function preview_modal(id) {
    $('#SongPreviewModal embed').attr('src', '/TEMPO/get-music-score/' + id);
    $('#SongPreviewModal').modal();
}

$(document).ready(function() {
    reset_input();
});
