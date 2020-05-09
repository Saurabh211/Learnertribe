// Only Accepting alphabets & space
$.validator.addMethod("onlyLetters", function(value, element) {
  return this.optional(element) || /^^[a-zA-Z ][A-Za-z ]+$/.test(value);
}, "This field contains only alphabets");

$.validator.addMethod("emailRule", function (value, element) {
    return this.optional(element) || /^([_a-z0-9]+(\.[_a-z0-9]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,5}))|(\d+$)$/.test(value);
}, "Please enter a valid email address.");

$.validator.addMethod("atLeastOneUppercaseLetter", function (value, element) {
    return this.optional(element) || /[A-Z]+/.test(value);
}, "Please enter valid password");

$.validator.addMethod("atLeastOneNum00000000ber", function (value, element) {
    return this.optional(element) || /[0-9]+/.test(value);
}, "Please enter valid password");

$.validator.addMethod("atLeastOneSymbol", function (value, element) {
    return this.optional(element) || /[!@#$%^&*()_./]+/.test(value);
}, "Please enter valid password");

$.validator.addMethod("onlyNumericals", function(value, element) {
        return this.optional(element) || /[0-9]$/.test(value);
}, "This field contains only Numbers");

$.validator.addMethod("phoneNumber", function(value, element) {
        return this.optional(element) || /^[0][1-9]\d{9}$|^[1-9]\d{9}$/.test(value);
}, "Please enter valid 10 digit number");


$("#SignUpForm").validate({
  rules: {
      full_name: {
        required: {
          depends:function(){
            $(this).val($.trim($(this).val()));
            return true;
        }
        },
        onlyLetters:true
      },
      email: {
        required: {
          depends:function(){
            $(this).val($.trim($(this).val()));
            return true;
        }
        },
        emailRule:true,
      },
      mobile_number: {
        required: {
          depends:function(){
            $(this).val($.trim($(this).val()));
            return true;
        }
        },
        phoneNumber:true
      },

      messages: {
          full_name: {
            onlyLetters:"First Name contains only alphabets"
          },
      },
  }
});



$("#LoginForm").validate({
  rules: {
      login_username: {
        required: {
          depends:function(){
            $(this).val($.trim($(this).val()));
            return true;
        }
        },
        emailRule:true
      },
    }
  });


$("#ForgetForm").validate({
  rules: {
      forget_email: {
        required: {
          depends:function(){
            $(this).val($.trim($(this).val()));
            return true;
        }
        },
        emailRule:true,
      }
    }
});

  // confirm password
$("#resetpasswordForm").validate({
  rules: {
    reset_confirm_password: {
      equalTo : "#new_password"
    }

  },
  messages: {
      reset_confirm_password: {
      equalTo : "Password & confirm password does'nt match"
    }

  }
});

$("#user").validate({
        rules: {
            email: {
                required: {
                    depends: function() {
                        $(this).val($.trim($(this).val()));
                        return true;
                    }
                },
                emailRule: true,
            },

            full_name: {
            required: {
             depends:function(){
             $(this).val($.trim($(this).val()));
                return true;
                }
                },
                onlyLetters:true,
              },

            mobile_number: {
                onlyNumericals: true,
                minlength: 10,
                maxlength: 15,
            },

messages: {
      full_name: {
        onlyLetters:"Name contains only alphabets"
      },

      mobile_number: {
        onlyLetters:"mobile contains only number"
      },
    },
        }
    });


