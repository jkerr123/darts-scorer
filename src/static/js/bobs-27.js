var numberToHit = 0;
var score = 27;

$( document ).ready(function(){

update();

$('#nohit').click(function() {

score = score - (numberToHit * 2)
update();

});

$('#single').click(function() {


score = score + (numberToHit * 2);
update();

});

$('#double').click(function() {

score = score + ((numberToHit * 2) * 2);
update();
});

$('#treble').click(function() {

score = score + ((numberToHit * 2) * 3);
update();
});


});

function update(){

    if (numberToHit == 20)
    {
        numberToHit = "Bull";
    }
    if (numberToHit == "Bull")
    {
        finishGame();
    }
    else
    {
    numberToHit++;
     $("p#score").text(score);
     $("p#doubleToHit").text(numberToHit);
    }
}

function finishGame()
{
    bootbox.alert("You have a score of " + score + "!", save_results());
}

function save_results()
{
    data = {"score": score,}

    $.ajax({
        type: "POST",
            url: "/update/bobs-27",
            data: JSON.stringify(data),
            processData: false,
            contentType: "application/json",
            success: function(obj)
            {
            if (obj.error)
                alert(obj.error)
            }
        });


}