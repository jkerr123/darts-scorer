            var socket;
            $(document).ready(function(){
                socket = io.connect('http://' + document.domain + ':' + location.port + '/game', {'sync disconnect on unload':true});


            });