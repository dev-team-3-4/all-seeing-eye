
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

    $.ajax({
        url: "/user/" + location.href.substring(location.href.lastIndexOf("/") + 1, location.href.length),
        method: "get",
        success: (data) => {
            if(location.href.substring(location.href.lastIndexOf("/") + 1, location.href.length) === getCookie("username")) {
                $("#self_page_part").css("display", "block");
                $("#email_input").val(data["email"]);
                $("#input_username").val(data["username"]);
                $("#bank_card_num").val(data["bank_card_number"]);
            }
            else {
                $("#other_container").css("display", "block");
                $("#username_h1").text(data["username"])
                $("#username_input").val(data["username"]);

                if(data["in_contacts"])
                    $("#delete_from_contacts").css("display", "block");
                else
                    $("#add_to_friends_button").css("display", "block");

                console.log(data)
            }

            let photo_link = "/static/img/camera_400.gif"
            if (data["profile_photo"] != null)
                photo_link = data["profile_photo"]

            $(".status_online").text(data["is_online"] ? "Online" : "Offline")
            $(".profile_photo").attr("src", photo_link)
            $("#title").text(data["username"])
        },
        error: (data) => {
            alert("Пользователя с таким именем нет!")
        },
        headers: {
            "Authorization": "Token " + getCookie("token"),
        }
    })

















    $("#username_bank_card_id_form").submit((e) => {
        e.preventDefault();
        $.ajax({
            url: "/user/me/",
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
                setCookie("username", $("#input_username").val())
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
                let token = data["token"]
                setCookie("token", token);
                alert("Пароль успешно заменён!");
                location.reload();

            },
            headers: {
                "Authorization": "Token " + getCookie("token"),
            }
        });
    });


    $("#change_email_send_key").submit((e) => {
        e.preventDefault();

        $.ajax({
            url: "/user/change/email/",
            method: "put",
            data: {
                "email": $("#email_input").val(),
                "username": "" + username
            },
            headers: {
                "Authorization": "Token " + getCookie("token"),
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

    $("#form_key").submit((e) => {
        e.preventDefault();

        $.ajax({
            url: "/user/change/email/",
            method: "post",
            data: {
                "email": $("#email_input").val(),
                "key": $("#email_key_input").val()
            },
            error: (data) => {
                console.log(data);
                alert("Неправильный код!")
            },
            success: (data) => {
                location.reload();
            }
        });
    });

    $("#delete_profile_button").click((e) => {
        if(confirm("Вы точно хотите удалить профиль?")) {
            $.ajax({
                url: "/user/" + username + "/",
                method: "delete",
                headers: {
                    "Authorization": "Token " + getCookie("token"),
                },
                error: (data) => {
                    console.log(data);
                    alert("Неправильный код!")
                },
                success: (data) => {
                    location.replace("/web");
                    setCookie("token", "")
                }
            });
        }
    })

    $("#upload_image_input").change((e) => {
        let form_data = new FormData();
        form_data.append('profile_photo', $("#upload_image_input")[0].files[0]);
        form_data.append('username', $("#input_username").val());

        $.ajax({
            method: 'put',
            enctype: 'multipart/form-data',
            url: '/user/me/',
            data: form_data,
            processData: false,
            contentType: false,
            cache: false,
            success: (answer) => {
                window.location.reload();
            },
            error: (answer) => {
                alert("error, check console!")
                console.error(answer);
            },
            timeout: 600000,
            headers: {
                "Authorization": "Token " + getCookie("token"),
            }
        });
    })

    $("#add_to_friends_button").click((e) => {
        $.ajax({
            url: "/user/" + $("#username_input").val() + "/contact/",
            method: "post",
            headers: {
                "Authorization": "Token " + getCookie("token"),
            },
            error: (data) => {
                alert("Error, check console")
                console.log(data)
            },
            success: (data) => {
                alert("Пользователь успешно добавлен в ваши контакты!")
                location.reload()
            }
        });
    });

    $("#delete_from_contacts").click((e) => {
        $.ajax({
            url: "/user/" + $("#username_input").val() + "/contact/",
            method: "delete",
            headers: {
                "Authorization": "Token " + getCookie("token"),
            },
            error: (data) => {
                alert("Error, check console")
                console.log(data)
            },
            success: (data) => {
                alert("Пользователь успешно удалён из ваших контактов!")
                location.reload()
            }
        });
    });


    $("#open_chat_button").click((e) => {
        $.ajax({
            url: "/chat/private/" + $("#username_input").val() + "/",
            method: "post",
            headers: {
                "Authorization": "Token " + getCookie("token"),
            },
            error: (data) => {
                alert("Error, check console")
                console.log(data)
            },
            success: (data) => {
                location.href = "/web/chat/" + data["id"];
            }
        });
    });

}