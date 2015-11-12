            var socket;
            $(document).ready(function(){

             if(window.location.protocol==="https:")
             window.location.protocol="http";
                socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
                socket.on('connect', function() {
                    socket.emit('joined');
                });

                socket.on('status', function(data) {
                    data.userlist.forEach(function(user) {
                    $('#player-list').append(new Option(user, user))
                    });
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



