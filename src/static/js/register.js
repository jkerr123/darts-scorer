$(document).ready(function(){

 $('#register').validate(
 {
  rules: {
    username: {
      minlength: 3,
      required: true
    },
    password: {
      minlength: 4,
      required: true
    },
        email: {
      required: true,
      email: true
    },
    agree: "required",
    over18: "required",
    feedback: "required"
  },
  messages: {

					username: {
						required: "Please enter a username",
						minlength: "Your username must consist of at least 3 characters"
					},
					password: {
						required: "Please provide a password",
						minlength: "Your password must be at least 4 characters long"
					},
					email: "Please enter a valid email address",
					agree: "Please agree to the terms & conditions",
					over18: "Please confirm that you are over 18 years old",
					feedback: "Please confirm that you give me permission to use feedback in my project report"
				},
				errorElement: "em",
				errorPlacement: function ( error, element ) {
					// Add the `help-block` class to the error element
					error.addClass( "help-block" );
					if ( element.prop( "type" ) === "checkbox" ) {
						error.insertAfter( element.parent( "label" ) );
					} else {
						error.insertAfter( element.parent( "label" ) );
					}
				},
highlight: function ( element, errorClass, validClass ) {
					$( element ).parents( ".form-group" ).addClass( "has-error" ).removeClass( "has-success" );

				},
				unhighlight: function (element, errorClass, validClass) {
					$( element ).parents( ".form-group" ).addClass( "has-success" ).removeClass( "has-error" );
				}
 });
});