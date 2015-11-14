            var socket;
            $(document).ready(function(){
                socket = io.connect('http://' + document.domain + ':' + location.port + '/chat', {'sync disconnect on unload':true});

                socket.on('connect', function() {
                    socket.emit('joined');
                });


                socket.on('status', function(data) {
                    update_players(data.userlist);
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

            $(window).bind('beforeunload', function(){
  socket.emit("playerleft");
});

function update_players(players){
    $('#player-list').empty();
    for (var i = 0; i < players.length; i++) {

        $("#player-list").append(new Option(players[i], players[i]));
        }

}