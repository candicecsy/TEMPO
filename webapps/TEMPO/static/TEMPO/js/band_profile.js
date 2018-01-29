function reset_input() {
    $('table input').val("");
}

$(document).ready(function() {
   reset_input();

   $('#save-btn').click(function() {
        $.ajax({
            type: "POST",
            url: "/TEMPO/add_band_user/",
            data: $('#add-band-user-form').serialize(),
            success: function (result) {
                if (result === 'Successful') {
                    window.location.replace('/TEMPO/my_band');
                } else {
                    alert(result);
                }
            },
            error: function(error) {
                // alert(error);
            }
        })
   });
});