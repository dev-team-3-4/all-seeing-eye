window.onload =
function ()
{
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
    if (getCookie("token") != undefined) {
        // alert("cookie already there!");
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

    function getAuthToken(l, p) {
        $.ajax({
            url: "/user/token/",
            method: "post",
            dataType: "json",
            data: {
                "username": l,
                "password": p
            },
            error: function(data) {
                alert("error: " + data);
            },
            success: function (data) {
                console.log(data);
                setCookie("token", data["token"], 10);
                window.location.replace("/user/" + l);
            }
        });
    }
    function changeDisplay(object, vis = "none") {
        return () => {
            $(object).css(
                "display", vis
            );
        };
    }

    $("#register_button").click(function (){
        changeDisplay("#choose_auth_type", "none")();
        changeDisplay("#register_container", "block")();
    });

    $("#auth_button").click(function (){
        changeDisplay("#choose_auth_type", "none")();
        changeDisplay("#login_form_container", "block")();
    });

    $("#back_button").click(function (){
        changeDisplay("#choose_auth_type", "block")();
        changeDisplay("#login_form_container", "none")();
    });

    $("#login_form").submit((e) => {
        e.preventDefault();
        sessionStorage.clear();

        let reg_password = $("#reg_password").val();
        let reg_login = $("#reg_login").val();
        let reg_email = $("#reg_email").val();

        if (reg_password !== $("#reg_password_confirm").val()) {
            alert("Пароли дожны совпадать!");
            return;
        } else if (reg_password.length < 8) {
            alert("Пароль слишком короткий!");
            return;
        }

        sessionStorage.setItem("login", reg_login);
        sessionStorage.setItem("email", reg_email);
        sessionStorage.setItem("password", reg_password);

        $.ajax({
            url: "/user/",
            method: "post",
            dataType: "json",
            data: {
                username: reg_login,
                email: reg_email,
                password: reg_password
            },
            error: function (data) {
                console.log(data);
            },
            success: function (data) {
                changeDisplay("#confirm_email_window", "block")();
                changeDisplay("#register_container", "none")();
            }
        });
    });

    $("#back_button_register").click(function () {
        changeDisplay("#choose_auth_type", "block")();
        changeDisplay("#register_container", "none")();
        console.log("Clicked bak register")
    });

    $("#accept_code").submit((e) => {
        e.preventDefault();
        $.ajax({
            url: "/user/change/email/",
            method: "post",
            dataType: "json",
            data: {
                email: sessionStorage.getItem("email"),
                key: $("#reg_code").val()
            },
            error: function (data) {
                alert(data.responseJSON["non_field_errors"][0]["message"]);
            },
            success: function (data) {
                console.log(data);

                getAuthToken(sessionStorage.getItem("login"), sessionStorage.getItem("password"));
                sessionStorage.clear();
            }
        });
    });

    $("#auth_form").submit((e) => {
        e.preventDefault();
        getAuthToken($("#auth_login").val(), $("#auth_password").val());
    });

    $("#forgot_password_button").click((e) => {
        $.ajax({
            url: "/user/" + $("#auth_login").val() + "/reset",
            method: "get",
            dataType: "json",
            data: {},
            error: function(data) {
                console.log(data);
                alert("Введённый логин неправильный! / Другая ошибка (дебаг)");
            },
            success: function (data) {
                console.log(data);
                alert("Мы отправили вам сообщение на почту с инструкцией по восстановалению пароля!");
            }
        });
    });
}

window.onclose = () => {
    sessionStorage.clear();
}