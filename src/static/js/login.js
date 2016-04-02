function login()
{

    var formData = $("#login").serialize();

    $.ajax({
        type: 'POST',
        url: '/auth/login',
        data: formData,
        success: function(obj)
            {

            if (obj.error){
               $("#message").addClass("alert alert-danger");
               $("#message").text(obj.error);
            }
                else
                    window.location.href = '/';
            }
        });

}