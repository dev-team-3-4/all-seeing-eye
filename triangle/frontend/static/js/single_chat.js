window.onload = function () {
    function add_message(image_link, content, time, username) {
        let message_template =
        `<div class="message_container">
            <div class="message_info">
                <img class="message_image" src="${image_link}">
                <div class="info_message_container">
                    <div class="message_time_username">
                        <h5 class="message_username">${username}</h5>
                        <h5 class="message_time">${time}</h5>
                    </div>
                    
                    <div class="message_content">
                        ${content}
                    </div>
                </div>
            </div>
        </div>`

        $("#messages_container").append(message_template)
    }

    function add_user(image_link, chat_username) {
        $("#users_list").append(`<div class="user_info">
             <img class="user_image" src="${image_link}">
                <div class="user_details">
                    <h4 class="username">${chat_username}</h4>
                    <h5 class="role">Модератор</h5>
            </div>
            <button class="button deal_button">Сделка!</button>
        </div>`);
    }

    const message_input = $("#message_input")



    const chat_id =  $("#chat_id").val();
    $.ajax({
        url: "/chat/" + chat_id + "/",
        method: "get",
        headers: {
            "Authorization": "Token " + getCookie("token"),
        },
        success: (data) => {
            console.log(data);

            let link = data["photo"];

            if(link == undefined) {
                link = "/static/img/camera_400.gif";
            }

            $("#chat_image").attr("src", link);
            $("#chat_name").text(data["name"]);
            if(!data["are_private"]) {
                data["member_objects"].forEach((item) => {
                    add_user(item["user"]["profile_photo"], item["user"]["username"])
                });
                $("#users_list").css("visibility", "visible");
            }


        },
    });

    $.ajax({
        url: "/chat/" + chat_id + "/message/",
        method: "get",
        headers: {
            "Authorization": "Token " + getCookie("token"),
        },
        data: {
            "page_size": 1e9,
            "page": 1
        },
        success: (data) => {
            var options = { year: 'numeric', month: 'long', day: 'numeric', hour: "numeric", minute: "2-digit" };
            console.log(data)
            data["results"].forEach((item) => {
                add_message(item["author"]["profile_photo"], item["text"], new Date(item["send_time"]).toLocaleDateString("ru-RU", options), item["author"]["username"])
            });
        }
    });

    $("#send_message_button").on("click", (e) => {
        let message = message_input.val()
        if(message.length !== 0) {
            $.ajax({
                url: "/chat/" + chat_id + "/message/",
                method: "post",
                headers: {
                    "Authorization": "Token " + getCookie("token"),
                },
                data: {
                    "text": message
                },
                success: (data) => {
                    add_message("qwe", message, "", "Sender")
                }
            });
        }
    })
}