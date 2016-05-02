var gameMode = document.getElementById("script").getAttribute("data-mode");

var dartsThrown = 0;
var currentNumber = 1;
var dartsAtNumber =
{
    "1": 0,
    "2": 0,
    "3": 0,
    "4": 0,
    "5": 0,
    "6": 0,
    "7": 0,
    "8": 0,
    "9": 0,
    "10": 0,
    "11": 0,
    "12": 0,
    "13": 0,
    "14": 0,
    "15": 0,
    "16": 0,
    "17": 0,
    "18": 0,
    "19": 0,
    "20": 0,
    "Bull": 0
};


$( document ).ready(function(){

update();

$('#hit').click(function() {

    dartsAtNumber[currentNumber]++;
    if (currentNumber == 20)
    {
        currentNumber = "Bull";
        dartsThrown++;
        update();
    }
    else if (currentNumber == "Bull")
    {
        dartsThrown++;
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

    dartsAtNumber[currentNumber]++;

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
            bootbox.alert("You have finished the game in " + dartsThrown + " darts!",function(){



    data = {numberOfDarts: dartsThrown, dartsAtEachNumber: dartsAtNumber, mode: gameMode}

       $.ajax({
        type: "POST",
            url: "/update/around-the-board",
            data: JSON.stringify(data),
            processData: false,
            contentType: "application/json",
            success: function(obj)
            {

}
        });

});
}