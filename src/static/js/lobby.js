 $(document).ready(function(){

                   socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
                socket.on('connect', function() {
                    socket.emit('joined', {});
                });

         socket.on('player connected', function(data) {
                     $("#player-list").append('<option value="' + data.data + '">' + data.data + '</option>');
                });

                socket.on('status', function(data) {
                    $('#chat').val($('#chat').val() + '<' + data.msg + '>\n');
                    $('#chat').scrollTop($('#chat')[0].scrollHeight);
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
                        socket.emit('messager', {message: msg});
                    }
                });

    });
