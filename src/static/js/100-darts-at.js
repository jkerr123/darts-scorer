var gameMode = document.getElementById("script").getAttribute("data-mode");

if (gameMode == "Bull")
    var numberToHit = 25;
else
    var numberToHit = parseInt(gameMode);

var dartsThrown = 0;
var score = 0;
var points = 0;

$( document ).ready(function(){

if (gameMode == "Bull")
{
                   $("#single").text("Outer Bull");
                   $("#double").text("Inner Bull");
                   $("#treble").hide();

}

update();

$('#miss').click(function() {

dartsThrown++;
update();

});


$('#single').click(function() {

dartsThrown++;
score = score + numberToHit;
points = points + 1
update();

});

$('#double').click(function() {
    dartsThrown++;
score = score + (numberToHit * 2);
points = points + 2
update();
});

$('#treble').click(function() {
    dartsThrown++;
score = score + (numberToHit * 3);
points = points + 3
update();
});


});

function update(){
    if (dartsThrown == 100)
    {
        finishGame();
    }
    else
    {
     $("p#score").text(score);
     $("p#dartsThrown").text(dartsThrown);
      $("p#points").text(points);
    }
}

function finishGame()
{
    bootbox.alert("You have a total of  " + points + " which is a score of " + score + "!", save_results());
}

function save_results()
{
    data = {"points": points, "score": score, "dartsThrown": dartsThrown, "number": numberToHit}

    $.ajax({
        type: "POST",
            url: "/update/100-darts-at",
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