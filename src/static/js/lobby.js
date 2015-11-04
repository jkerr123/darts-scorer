 $(document).ready(function(){

        var socket = io.connect('http://' + document.domain + ':' + location.port + '/lobby');


        // the socket.io documentation recommends sending an explicit package upon connection
        socket.on('connect', function() {
            socket.emit('player joined', {})
        });

         socket.on('player connected', function(data) {
                     $("#player-list").append('<option value="' + data.player + '">' + data.player + '</option>');
                });

        socket.on('message received', function(data) {
                                   $('#chat').val($('#chat').val() + data.message + '\n');
                    $('#chat').scrollTop($('#chat')[0].scrollHeight);
                });

            $('#message').keypress(function(e) {
                    var code = e.keyCode || e.which;
                    if (code == 13) {
                        msg = $('#message').val();
                        $('#message').val('');
                        socket.emit('message', {message: msg});
                    }
                });

    });