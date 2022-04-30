
function getCookie(cName) {
      const name = cName + "=";
      const cDecoded = decodeURIComponent(document.cookie); //to be careful
      const cArr = cDecoded.split('; ');
      let res;
      cArr.forEach(val => {
        if (val.indexOf(name) === 0) res = val.substring(name.length);
      })
      return res;
    }

    function setCookie(name,value,days) {
        var expires = "";
        if (days) {
            var date = new Date();
            date.setTime(date.getTime() + (days*24*60*60*1000));
            expires = "; expires=" + date.toUTCString();
        }
        document.cookie = name + "=" + (value || "")  + expires + "; path=/";
    }


window.onload = function () {
    $("#username_bank_card_id_form").submit((e) => {
        e.preventDefault();
        $.ajax({
            url: "/user/" + username + "/",
            method: "put",
            dataType: "json",
            data: {
                "username": $("#input_username").val(),
                "bank_card_number": $("#bank_card_num").val(),
            },
            error: (data) => {
                alert("Error, check console");
                console.log(data);
            },
            success: (data) => {
                location.replace("/web/user/" + $("#input_username").val());
            },
            headers: {
                "Authorization": "Token " + getCookie("token"),
            }
        });
    });

    $("#change_password_form").submit((e) => {
       e.preventDefault();
       $.ajax({
            url: "/user/" + username + "/change/password/", // {{host}}user/{{username}}/change/password/
            method: "put",
            dataType: "json",
            data: {
                old_password: $("#old_password").val(),
                password: $("#new_password").val(),
            },
            error: (data) => {
                alert("Неправильный старый пароль / невалидный новый");
                console.log(data);
            },
            success: (data) => {
                let token = data.responseJSON["token"]
                setCookie("token", token);
                alert("Пароль успешно заменён!");

            },
            headers: {
                "Authorization": "Token " + getCookie("token"),
            }
        });
    });


    $("#change_email_send_key").submit((e) => {
        e.preventDefault();

        $.ajax({
            url: "/user/change/email/", // {{host}}user/{{username}}/change/password/
            method: "get",
            dataType: "json",
            body: {
                "email": $("#email_input").val(),
                username: username
            },
            error: (data) => {
                console.log(data);
                alert("Error, check console")
            },
            success: (data) => {
                alert("На почту отправлено письмо с кодом подтверждения!")
            }
        });

    });
}