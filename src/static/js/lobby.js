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

                socket.on('challenged', function(data) {
                    bootbox.confirm(data.msg, function(result) {
                     if(result == true)
                     {

                        data = {player: data.player, newroom: data.newroom}
                        $.ajax({
                                type: "POST",
                                url: "/player-challenged",
                                data: JSON.stringify(data),
                                processData: false,
                                contentType: "application/json",
                                success: function(obj)
                                {
                                    if (obj.error)
                                        {
                                            alert(obj.error)
                                        }
                                        else
                                        {
                                        socket.emit("matchaccepted", {'player': obj.player, 'room': obj.room})
                                        }
                                }
                                });
                     }
                    });
                });

                 socket.on('beginmatch', function(data) {
                     window.location.href = data.url;
                });

                 $("#challenge").click(function(){
                       var playertochallenge = $('#player-list').val();
                    socket.emit('challenge_player', {player: playertochallenge});
                    });

                     socket.on('matchaccepted', function(data) {
                     socket.emit("matchsetup", {'player': data.player})
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

