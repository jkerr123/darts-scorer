var dartsThrown = 0;
var currentNumber = 1;


$( document ).ready(function(){

update();

$('#hit').click(function() {

    if (currentNumber == 20)
    {
        currentNumber = "Bull";
        dartsThrown++;
        update();
    }
    else if (currentNumber == "Bull")
    {
        finishGame();
    }
    else
    {
        currentNumber++;
        dartsThrown++;
        update();
    }

});



$('#miss').click(function() {

    dartsThrown++;
    update();

});
});




function update()
{

        $("p#score").text(dartsThrown);
        $("p#currentNumber").text(currentNumber);

}

function finishGame()
{
            bootbox.alert("You have finished the game in " + dartsThrown + " darts!", function() {

        });
}