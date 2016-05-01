var numberToHit = 0;
var score = 27;

var hitsOnEachNumber =
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

$('#nohit').click(function() {

score = score - (numberToHit * 2)
update();

});

$('#single').click(function() {


score = score + (numberToHit * 2);
    hitsOnEachNumber[numberToHit]+=1;

update();

});

$('#double').click(function() {

score = score + ((numberToHit * 2) * 2);
    hitsOnEachNumber[numberToHit]+=2;

update();
});

$('#treble').click(function() {
    hitsOnEachNumber[numberToHit]+=3;

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
    data = {"score": score, "hitsOnEachNumber": hitsOnEachNumber}

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
                else
                window.location.href = 'bobs-27-summary?game_id=' + obj.id;
            }

        });


}