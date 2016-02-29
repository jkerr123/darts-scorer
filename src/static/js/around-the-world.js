var dartCount = 0;
var dartsThrown = 0;
var currentNumber = 1;


$( document ).ready(function(){

update();

$('#number1').click(function() {
    dartCount++;
    dartsThrown++;
      currentNumber++;
    checkDartCount();
   $('#number1').prop('disabled', true);
});

$('#number2').click(function() {
    dartCount++;
    dartsThrown++;
    currentNumber++;
    checkDartCount();
   $('#number2').prop('disabled', true);
});

$('#number3').click(function() {
    dartCount++;
    dartsThrown++;
    currentNumber++;

    checkDartCount();
   $('#number3').prop('disabled', true);
});

$('#nohit').click(function() {
    dartCount++;
    dartsThrown++;

    checkDartCount();
});

});

function checkDartCount()
{
    if (dartCount == 3)
    {
        update();
    }
}



function update()
{

       dartCount = 0;

     $('#number1').html(currentNumber);
    $('#number2').html(currentNumber +1);
    $('#number3').html(currentNumber +2);

       $('#number1').prop('disabled', false);
   $('#number2').prop('disabled', false);
   $('#number3').prop('disabled', false);



    $("p#score").text(dartsThrown);
    $("p#currentNumber").text(currentNumber);
}