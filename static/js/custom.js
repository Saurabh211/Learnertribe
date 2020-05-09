//scroll add and remove class js
$(window).scroll(function () {
    var scroll = $(window).scrollTop();
    if (scroll >= 10) {
        $("body").addClass("scrolled");
    } else {
        $("body").removeClass("scrolled");
    }
});


//nav bar icon toggle
$("#hamburger").click(function () {
    $(this).toggleClass('open');
    $('.navigation').toggleClass('open');
})


//login signup show hide
$(".show-login").click(function () {
    $(".login-error-container").addClass('d-none');
    $(".login-error-container").text('');
    $(".tab-login").hide()
    $("#login").show();
    $('input.from-input').val('');
    $('label.error').text('');
    $('#attached_document').val('');
    $("#myForm").trigger("reset");

    $('#SignUpForm').trigger("reset");
    $('#LoginForm').trigger("reset");
    $('#user_passcode').trigger("reset");
    $('#ForgetPassword').trigger("reset");

});

$(".show-signup").click(function () {
    $(".tab-login").hide()
    $("#sign_up").show();
    $('#SignUpForm').trigger("reset");
    $('#bChecksignup').text("Upload Document");
    $('#LoginForm').trigger("reset");
    $('#user_passcode').trigger("reset");
    $('#ForgetPassword').trigger("reset");
    $("#code").val(instituteCode);
});

$(".show-forgot").click(function () {
    $(".tab-login").hide()
    $("#forgot").show();
});

$(".show-otp").click(function () {
    $(".tab-login").hide()
    $("#otp").show();
});

//categories js
$("#left-cat").click(function () {
    $(this).addClass('active')
    $("#right-cat").removeClass('active');
    $(".t-detail").show();
    $(".v-detail").hide();
});

$("#right-cat").click(function () {
    $(this).addClass('active')
    $("#left-cat").removeClass('active');
    $(".v-detail").show();
    $(".t-detail").hide();
});


//tab js
$(".login-tab").click(function () {
    $(".login-tab").removeClass('active')
    $(this).addClass('active');
})

//tab js
$(".tab").click(function () {
    $(".tab-detail").hide();
    var data = $(this).attr('data');
    $('#' + data).show();
    $(".tab").removeClass('active');
    $(this).addClass('active');
})

//modal-open js
$(".modal-open").click(function () {
    $(".modal").hide();
    $('body').removeClass('modal-open');
    var data = $(this).attr('data');
    $('#' + data).addClass('show');
    $('#' + data).show();
    $('body').addClass('modal-open');
})

//modal-close js
$(".modal-close").click(function () {
    $(".modal").hide();
    $(".modal").removeClass('show');
    $('body').removeClass('modal-open');
})


//click dropdown js
$(".dropdown").click(function () {
    var data = $(this).attr('drop');
    $('#' + data).toggleClass('active');
})

// signup page file name change js
$("#attached_document").change(function (e) {
    var filename = e.target.files[0].name;
    $('#bChecksignup').text('');
    $('#bChecksignup').text(filename);
});

//file name change js
$('.value-id').click(function () {
    var data = $(this).attr('data');
    $("#file1" + data).change(function (e) {
        var filename = e.target.files[0].name;
        $('#bCheck' + data).text('');
        $('#bCheck' + data).text(filename);
        $('#bCheck' + data).addClass('upload');
    });
});


//password show hide function
function passwordSHOW() {
    var x = document.getElementById("password");
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }
}

function passwordSHOWs() {
    var x = document.getElementById("login_password");
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }
}

//js for active nav
jQuery(function ($) {
    var path = window.location.href;
    $('.nav-toggle-active').each(function () {
        if (this.href === path) {
            $(this).addClass('active');
        }
    });
});


//modal open and close js
$(".modal-open").click(function () {
    $(".modal-container").hide();
    var modal = $(this).attr('modal');
    $('#' + modal).show();
})
$(".modal-close").click(function () {
    $(".modal-container").hide();
    $('.modal-input').val('');
    //    $('.modal-input').text('');
})



//    count one add js+
//$(document).on("click", ".valadd-1", function () {
//    var midall = $(this).attr('data');
//    var value = parseInt(document.getElementById(midall).value);
//    value += 1;
//    document.getElementById(midall).value = value;
//    if (value == 1) {
//        $('#minus' + midall).removeClass('valremove-1');
//        $('#minus' + midall).addClass('disabled');
//    } else {
//        $('#minus' + midall).addClass('valremove-1');
//        $('#minus' + midall).removeClass('disabled');
//    }
//})

$(document).on("click", ".valadd-1", function () {
    var midall = $(this).attr('data');
    var max = $(this).attr('data-max');
    var value = parseInt(document.getElementById(midall).value);
    if (value == max){
        $('#plus' + midall).removeClass('valadd-1');
        $('#plus' + midall).addClass('disabled');
    }else{
        $('#plus' + midall).addClass('valadd-1');
        $('#plus' + midall).removeClass('disabled');

        value += 1;
        document.getElementById(midall).value = value;
        if (value == 1) {
            $('#minus' + midall).removeClass('valremove-1');
            $('#minus' + midall).addClass('disabled');
        } else {
            $('#minus' + midall).addClass('valremove-1');
            $('#minus' + midall).removeClass('disabled');
        }
        }
})

//    count one remove js+
$(document).on("click", ".valremove-1", function () {
    var midall = $(this).attr('data');
    var value = parseInt(document.getElementById(midall).value);
   // document.getElementById(midall).value = value;
    if (value == 1) {
        $('#minus' + midall).removeClass('valremove-1');
        $('#minus' + midall).addClass('disabled');
    } else {
        value -= 1;
        document.getElementById(midall).value = value;
        $('#minus' + midall).addClass('valremove-1');
        $('#minus' + midall).removeClass('disabled');
        $('#plus' + midall).addClass('valadd-1');
        $('#plus' + midall).removeClass('disabled');


    }
})
