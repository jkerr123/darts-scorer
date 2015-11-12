            var socket;
            $(document).ready(function(){
                socket = io.connect('https://' + document.domain + ':' + location.port + '/chat');
                socket.on('connect', function() {
                    socket.emit('joined');
                });

                socket.on('status', function(data) {
                    $('#player-list').append(new Option(data.user, data.user))
                    $('#chat').val($('#chat').val() + '<' + data.msg + '>\n');
                    $('#chat').scrollTop($('#chat')[0].scrollHeight);
                });

                socket.on('message received', function(data) {
                    $('#chat').val($('#chat').val() + data.message + '\n');
                    $('#chat').scrollTop($('#chat')[0].scrollHeight);
                });

                $('#text').keypress(function(e) {
                    var code = e.keyCode || e.which;
                    if (code == 13) {
                        text = $('#text').val();
                        $('#text').val('');
                        socket.emit('message', {msg: text});
                    }
                });
            });