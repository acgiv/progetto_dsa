 function read_text_password(id) {
            const element = document.getElementById(id);
            if (element.type === "text") {
                return element.value;
            } else {
                element.type = "text";
                const val_password = element.value;
                element.type = "password";
                return val_password;
            }

        }

function control_security_password(password) {
    let cont = 0;
    const len_password = password.length;
    if (len_password !== 0) {
        if (len_password > 8) {
            cont += 16.0;
        } else {
            cont += len_password * 2;
        }
        if (password.search(/^(?=.*[A-Z]).*$/) === 0) {
            cont += 16.0;
        }
        if (password.search(/^(?=.*[a-z]).*$/) === 0) {
            cont += 16.0;
        }
        if (password.search(/^(?=.*[~`!@#$%^&*()--+={}\[\]|\\:;"'<>,.?/_₹]).*$/) === 0) {
            cont += 16.0;
        }
        if (password.search(/^.{10,100}$/) === 0) {
            cont += 16.0;
        }
        if (password.search(/^(?=.*[0-9]).*$/) === 0) {
            cont += 16.0;

        }
    }
    if (cont === 96) {
        cont = 100;
    }
    return cont;
}

jQuery.validator.addMethod("validate_email", function(value) {
    return /^([a-zA-Z0-9_.\-])+@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/.test(value);
}, "L'email deve essere nel formato example@mail.com");



jQuery.validator.addMethod("validate_username", function(value) {
    return /^([a-zA-Z0-9_.\-])+$/.test(value);
    }, "Errore nel formato.");


 function control_email() {
     $(document).ready(function () {
         $('#form_control').validate({
             rules: {
                 user_name: {
                     required: true,
                     validate_username: true,
                     minlength: 3,
                     maxlength: 10
                 },
                 email: {
                     required: true,
                     email: true,
                     validate_email: true
                 },
                 password: {
                     required: true,
                     minlength: 6
                 },
                 confirm_password: {
                     required: true,
                     minlength: 6
                 },
                 inlineRadioOptions: {
                     required: true
                 },
                 date_birth: {
                     required: true,
                     date: true
                 }
             },
             messages: {
                 user_name: {
                     required: "Il campo email è obbligatorio.",
                     minlength: "Per favore, inserisci almeno 3 caratteri.",
                     maxlength: "Per favore, inserisci meno di 10 caratteri."
                 },
                 email: {
                     required: "Il campo email è obbligatorio.",
                     email: "Inserisci un indirizzo email valido."
                 },
                 confirm_password: {
                     required: "Il campo conferma password è obbligatorio.",
                     minlength: "Per favore, inserisci almeno 6 caratteri."
                 },
                 password: {
                     required: "Il campo conferma password è obbligatorio.",
                     minlength: "Per favore, inserisci almeno 6 caratteri."
                 },
                 inlineRadioOptions: {
                     required: "Il campo genere è obbligatorio!."
                 },
                 date_birth: {
                     required: "Il campo genere è obbligatorio!."
                 }

             },
             errorPlacement: function (error, element) {
                 if (element.attr("name") === "user_name") {
                     error.appendTo('#user_email_validation_error');
                     if (document.getElementById("content_error_user_name").classList.contains("d-none")) {
                         document.getElementById("content_error_user_name").classList.remove("d-none");
                     }
                     document.getElementById("user_email_validation_error").classList.remove("d-none");
                 }
                 if (element.attr("name") === "email") {
                      error.appendTo("#email_validation_error");
                     if (document.getElementById("content_error_email").classList.contains("d-none")) {
                         document.getElementById("content_error_email").classList.remove("d-none");
                         document.getElementById("email_validation_error").classList.remove("d-none");
                     }
                 }
                 if (element.attr("name") === "password") {
                     error.appendTo("#error_password");
                     document.getElementById("content_err_password").classList.remove("d-none");
                     document.getElementById("password-error").classList.add("px-2");
                 }

                 if (element.attr("name") === "confirm_password") {
                     error.appendTo("#error_conf_password");
                     document.getElementById("content_err_conf_password").classList.remove("d-none");
                     document.getElementById("confirm-password-error").classList.add("px-2");
                 }
                 if (element.attr("name") === "inlineRadioOptions") {
                     error.appendTo("#error_genere");
                     document.getElementById("content_err_genere").classList.remove("d-none");
                     document.getElementById("inlineRadioOptions-error").classList.add("px-2");
                 }
                 if (element.attr("name") === "date_birth") {
                     error.appendTo("#error_date");
                     document.getElementById("all_message_date").classList.remove("d-none");
                     document.getElementById("date_birth").classList.remove("mb-5");
                     document.getElementById("all_message_date").classList.add("mb-5");
                     document.getElementById("date_birth-error").classList.add("px-2");
                 }

             },/* success: function (label, element) {
                 if (element.name === "user_name") {
                     if (document.getElementById("user_email_error_message").classList.contains("d-none")) {
                         document.getElementById("content_error_user_name").classList.add("d-none");
                     }
                     document.getElementById("user_email_validation_error").classList.add("d-none");
                 }
                 if (element.name === "email") {
                     document.getElementById("content_error_email").classList.add("d-none");
                     document.getElementById("email_validation_error").classList.add("d-none");
                 }
                 if (element.name === "password") {
                     document.getElementById("content_err_password").classList.add("d-none");
                 }

             },*/
             invalidHandler: function (event, validator) {
                 const firstErrorElement = validator.errorList[0].element;
                 $(firstErrorElement).focus();
             }
         });
     });
 }


$(document).ready(function () {
    $(document.getElementById("form_register")).on('input', function () {
        $.ajax({
            url: '/verifier',
            type: 'POST',
            data: {
                "user_name": document.getElementById("user_name").value,
                "email": document.getElementById("email").value,
                "password": read_text_password("password"),
                "confirm-password": read_text_password("confirm-password")
            }, success: function (data) {
                control_email();
                if (data.user_name !== false) {
                    document.getElementById("content_error_user_name").classList.remove("d-none");
                    document.getElementById("crea_account").disabled = true;
                    document.getElementById("message_user").innerHTML = data.user_name;
                    document.getElementById("user_email_error_message").classList.remove("d-none");
                } else {
                    document.getElementById("crea_account").disabled = false;
                    document.getElementById("message_user").innerHTML = "";
                    document.getElementById("user_email_error_message").classList.add("d-none");
                }

                if (data.email !== false) {
                    document.getElementById("content_error_email").classList.remove("d-none");
                    document.getElementById("crea_account").disabled = true;
                    document.getElementById("email_error_message").classList.remove("d-none");
                    document.getElementById("message_email_exist").innerHTML = data.email;

                } else {
                    document.getElementById("crea_account").disabled = false;
                    document.getElementById("email_error_message").classList.add("d-none");
                }
                if (data.password !== false) {
                    document.getElementById("message_password").innerHTML = data.password;
                    document.getElementById("message_password").classList.remove("d-none");
                } else {
                    document.getElementById("message_password").classList.add("d-none");
                }
                const password = read_text_password("password");
                if (read_text_password("password").length === 0) {
                    document.getElementById("password").classList.add("mb-0", "mb-2");
                    document.getElementById("security_password").classList.add("d-none");
                } else {
                    document.getElementById("err_conf_message_pass").classList.remove("d-none");
                    document.getElementById("security_password").classList.remove("d-none");
                    document.getElementById("password").classList.replace("mb-2", "mb-0");
                    const cont = control_security_password(password);
                    document.getElementById("bar_percent").style.width = cont.toString() + "%";
                    if (cont <= 16) {
                        document.getElementById("bar_percent").style.backgroundColor = "#FF0000";
                    } else if (cont <= 32) {
                        document.getElementById("bar_percent").style.backgroundColor = "#ff6666";
                    } else if (cont <= 48) {
                        document.getElementById("bar_percent").style.backgroundColor = "#FFA500";
                    } else if (cont <= 64) {
                        document.getElementById("bar_percent").style.backgroundColor = "#8FCE00";
                    } else if (cont >= 84) {
                        document.getElementById("bar_percent").style.backgroundColor = "#476700";
                    }
                }
            }
        });
    });
});

function password_show_hide(id_element, show_eye, hide_eye) {
    const id = id_element;
    const s_eye = show_eye;
    const h_eye = hide_eye;
    const password = document.getElementById(id);
    const show_password = document.getElementById(s_eye);
    const hide_password = document.getElementById(h_eye);
    hide_password.classList.remove("d-none");
    if (password.type === "password") {
        password.type = "text";
        show_password.style.display = "none";
        hide_password.style.display = "block";
    } else {
        password.type = "password";
        show_password.style.display = "block";
        hide_password.style.display = "none";
    }
}


$(document).ready(function () {
    $(document.getElementById("login_register")).on('input', function () {
        console.log(document.getElementById("error_login").classList.contains("d-none"));
        if(!document.getElementById("error_login").classList.contains("d-none")){
             document.getElementById("error_login").classList.add("d-none");
        }
    });
});
