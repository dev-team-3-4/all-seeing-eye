window.onload = function () {
    function add_message(image_link, content, time, username, role) {
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

    function add_user(image_link, chat_username, role_id) {
        $("#users_list").append(`<div class="user_info">
             <img class="user_image" src="${image_link}">
                <div class="user_details">
                    <h4 class="username">${chat_username}</h4>
                    <h5 class="role">Роль: ${role_id}</h5>
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
                    add_user(item["user"]["profile_photo"], item["user"]["username"], item["role"])
                });
                $("#users_list").css("visibility", "visible");
                $("#admin_buttons_wrapper").css("visibility", "visible");
            }
        },
    });

    function loadMessages() {
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
                $("#messages_container").html("")
                var options = { year: 'numeric', month: 'long', day: 'numeric', hour: "numeric", minute: "2-digit" };
                console.log(data)
                data["results"].forEach((item) => {
                    add_message(item["author"]["profile_photo"], item["text"], new Date(item["send_time"]).toLocaleDateString("ru-RU", options), item["author"]["username"])
                });
            }
        });
    }

    loadMessages();

    setInterval(loadMessages, 3000);


    $("#send_message_button").on("click", (e) => {
        let message = message_input.val()
        if(message.length !== 0) {
            message_input.val("")
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
                    add_message("", message, "", "")
                }
            });
        }
    });


    $("#invite_user_button").on("click", ()=>{
        $("#chat_container").css("display", "none");
        $("#search_contacts_to_add").css("display", "flex");
    })

    // Тут логика поиска и добавления юзера в чат

    function addContactToList(username, photo_link, contact_id) {
        let result = ``+
            `<li class="chat_wrap" onclick="add_to_chat(${contact_id})">\n` +
            `   <img class="chat_image_searched" src="${photo_link}" alt="Profile photo"/>\n` +
            `   <h4 class="user_name_search">${username}</h4>\n` +
            `</li>`;

        $("#chats_list").append(result);
    }

    let users_page = 1;
    let scrolled_to_end = false;

    function scrolledToBottom() {
        if (scrolled_to_end)
            return;
        $.ajax({
            url: "/user/contacts/",
            method: "GET",
            dataType: "json",
            data: {
                page: users_page,
                page_size: 10
            },
            success: (data) => {
                total_users = data["count"]
                data["results"].forEach((item) => {
                    addContactToList(item["username"], item["profile_photo"] == null ? "/static/img/camera_400.gif" : item["profile_photo"], item["id"]);
                });
                users_page += 1;
                scrolled_to_end = total_users < (10 * (users_page - 1));
                scrollEvent()
            },
            headers: {
                "Authorization": "Token " + getCookie("token"),
            }
        });

    }

    function scrollEvent() {
        if (my_div.offsetHeight + my_div.scrollTop >= my_div.scrollHeight) {
            console.log("scrolled to end")
            scrolledToBottom();
        }
    }


    let scroll_div = $("#contacts_scroll");

    let my_div = document.getElementById("contacts_scroll");

    scrollEvent();

    scroll_div.on('scroll', function() {
        scrollEvent();
    });
}

    function add_to_chat(contact_id) {
        $.ajax({
            url: "/chat/" + $("#chat_id").val() + "/member/" + contact_id + "/",
            method: "post",
            success: (data) => {
                location.reload()
            },
            error: (data) => {
                alert("Невозможно добавить этого пользователя в чат!");
                console.log(data)
            },
            headers: {
                "Authorization": "Token " + getCookie("token"),
            }
        })
    }