window.onload = function () {
    document.addEventListener(
        'keydown', (event) => {
            let name = event.key;
            let code = event.code;
            // Alert the key name and key code on keydown
            if (code == "Escape" && editableMessageId != undefined) {
                attachments = undefined;
                editableMessageId = undefined;
                message_input.val("");
            }
        }, false);


    const chat_id =  $("#chat_id").val();
    var users_list_dict = {}
    var editableMessageId = undefined;
    const roles_list = [
        "", // "юзер"
        "Модератор",
        "Администратор",
        "Владелец чата"
    ]

    function deleteMessageClosure(message_id) {
        return function () {
            $.ajax({
                url: "/chat/" + chat_id + "/message/" + message_id + "/",
                method: "delete",
                headers: {
                    "Authorization": "Token " + getCookie("token"),
                },
                success: (data) => {
                    alert("Сообщение успешно удалено!")
                },
            });
        }
    }

    function editMessageClosure (message_id) {
        return function () {
            editableMessageId = message_id;
            message_input.val($(`#message_${message_id}_content`).text());
        }
    }

    function image_link_check(link) {
        if (link == null)
            return  "/static/img/camera_400.gif"
        return link
    }

    function add_message(
        image_link, content, time, username, message_id, add_edit_tab = false, add_remove_tab = false,
        attachments = [], whole_data
    ) {
        let deleteMessageFunction = deleteMessageClosure(message_id);
        let editMessageFunction = editMessageClosure(message_id)

        let deleteMessageTab = "";
        let editMessageTab = "";



        if (add_remove_tab) {
            deleteMessageTab = `<button class="button edit_message_button edit_message_button_red" id="delete_message_${message_id}_button">Удалить</button>`;
        }

        if (add_edit_tab) {
            editMessageTab = `<button class="button edit_message_button" id="edit_message_${message_id}_button">Ред.</button>`;
        }

        let attachments_html = '';

        attachments.forEach((image_url, index) => {
            let file_name = image_url.substring(image_url.lastIndexOf('/')+1)

            attachments_html +=
                `<a href="${image_url}" target="_blank">
                    <div class="message_attachments">
                        <img src="/static/img/file_sign.png" class="file_sign_image">
                        <div class="attachments_name">${file_name}</div>
                    </div>
                </a>`
        });

        let invite_moderator_request ='';
        if (whole_data["moderator_invite"] != undefined) {
            let moderator_photo_link = image_link_check(whole_data['moderator_invite']['moderator']['profile_photo'])
            let moderator_name = whole_data['moderator_invite']['moderator']['username']
            invite_moderator_request =
            `<div class="message_content">
                <h4>Хочет пригласить модератора:</h4>
                <div class="moderator_info">
                    <img class="message_image" src="${moderator_photo_link}">
                    <div>${moderator_name}</div>
            </div>
            <div class="moderator_info" style="max-width: 200px">
                <button class="button edit_message_button edit_message_button_red" id="decline_moderator_${whole_data['id']}">Отклонить</button>
                <button class="button edit_message_button" id="accept_moderator_${whole_data['id']}">Принять</button>
            </div>
            </div>`;
        }

        let withdrawal_request = '';
        if (whole_data["withdrawal_request"] != undefined) {
            withdrawal_request =
            `<div class="message_content">
                <h4>Выдвинуто предложение</h4>
                <h5>Заказчик получает: ${whole_data["withdrawal_request"]["first_user_funds"]}</h5>
                <h5>Ответчик получает: ${whole_data["withdrawal_request"]["second_user_funds"]}</h5>
                <h5>Модератор получает: ${whole_data["withdrawal_request"]["moderator_funds"]}</h5>
                <h5>Сделка ${whole_data["withdrawal_request"]["close_contract"] ? "":"не"} будет закрыта</h5>
            <div class="moderator_info" style="max-width: 200px">
                <button class="button edit_message_button edit_message_button_red" id="decline_moderator_${whole_data['id']}">Отклонить</button>
                <button class="button edit_message_button" id="accept_moderator_${whole_data['id']}">Принять</button>
            </div>
            </div>`;
        }


        if (content == undefined)
            content = ''
        let message_template =
        `<div class="message_container">
            <div class="message_info">
                <img class="message_image" src="${image_link}">
                <div class="info_message_container">
                    <div class="message_time_username">
                        <a style="text-decoration: none" href="/web/user/${username}"><h5 class="message_username">${username}</h5></a>
                        <h5 class="message_time">${time}</h5>
                    </div>
                    
                    <div class="message_content">
                        <div id="message_${message_id}_content">${content}</div>
                        ${attachments_html}
                        ${invite_moderator_request}
                        ${withdrawal_request}
                    </div>
                </div>
                <div class="edit_message">
                    ${editMessageTab}
                    ${deleteMessageTab}
                </div>
            </div>
        </div>`

        $("#messages_container").append(message_template)
        $(`#delete_message_${message_id}_button`).on('click', (e) => {deleteMessageFunction()});
        $(`#edit_message_${message_id}_button`).on('click', (e) => {editMessageFunction()})

        $(`#decline_moderator_${whole_data['id']}`).click(() => {
            $.ajax({
                url: `/contract/message/${whole_data['id']}/`,
                method: "delete",
                success: (data) => {
                    alert("Успешно")
                },
                headers: {
                    "Authorization": "Token " + getCookie("token"),
                },
            })
        })

        $(`#accept_moderator_${whole_data['id']}`).click(() => {
            $.ajax({
                url: `/contract/message/${whole_data['id']}/`,
                method: "put",
                success: (data) => {
                    alert("Успешно")
                },
                headers: {
                    "Authorization": "Token " + getCookie("token"),
                },
            })
        })

        $(`#decline_withdrawal${whole_data['id']}`).click(() => {

        })
    }

    function startDealButtonClosure(user_id) {
        return function () {
            $.ajax({
                url: "/contract/",
                method: "post",
                data: {
                    "second_user_id": user_id
                },
                headers: {
                    "Authorization": "Token " + getCookie("token"),
                },
                success: (data) => {
                    console.log(data)
                    location.href = "/web/create_deal/" + data["id"]
                },
                error: (data) => {
                    alert("Unable to kick this user!");
                }
            })
        }
    }

    function add_user(image_link, chat_username, role_id, user_id) {
        let kick_button = "";

        if (role_id < users_list_dict[getCookie("username")]["role"] - 1)
            kick_button = `<h5 class="kick_user_button" onclick="" id="kick_user_${user_id}_button">Выгнать!</h5>`

        let button_html = '';
        if (chat_username != username) {
            button_html = `<button class="button deal_button" id="deal_button_${user_id}">Сделка!</button>`
        }

        $("#users_list").append(`<div class="user_info">
             <img class="user_image" src="${image_link}">
                <div class="user_details">
                    <h4 class="username">${chat_username}</h4>
                    <h5 class="role">${roles_list[role_id]}</h5>
                    ${kick_button}
            </div>
            ${button_html}
        </div>`);


        if (button_html != '') {
            let deal_closure = startDealButtonClosure(user_id);
            $(`#deal_button_${user_id}`).click(() => {deal_closure()});
        }

        $(`#kick_user_${user_id}_button`).on('click', (e) => {
            $.ajax({
                url: "/chat/" + chat_id + "/member/" + user_id + "/",
                method: "delete",
                headers: {
                    "Authorization": "Token " + getCookie("token"),
                },
                success: (data) => {
                    location.reload();
                },
                error: (data) => {
                    alert("Unable to kick this user!");
                }
            });
        });
    }

    $("#leave_chat_button").on('click', (e) => {
        console.log(users_list_dict)
        console.log(users_list_dict[getCookie("username")]["id"])
        $.ajax({
            url: "/chat/" + chat_id + "/member/" + users_list_dict[getCookie("username")]["id"] + "/",
            method: "delete",
            headers: {
                "Authorization": "Token " + getCookie("token"),
            },
            success: (data) => {
                location.reload();
            },
            error: (data) => {
                alert("Невозможно выйти из чата!")
            }
        })
    });

    const message_input = $("#message_input")



    $.ajax({
        url: "/chat/" + chat_id + "/",
        method: "get",
        headers: {
            "Authorization": "Token " + getCookie("token"),
        },
        success: (data) => {
            users_list_dict = {};
            console.log("READING INFO ABOUT CHAT")
            console.log(data);

            let link = data["photo"];

            if(link == undefined) {
                link = "/static/img/camera_400.gif";
            }

            $("#chat_image").attr("src", link);
            $("#chat_name").text(data["name"]);

            if(!data["are_private"]) {
                data["member_objects"].forEach((item) => {
                    if (item["user"]["username"] == getCookie("username")) {
                        users_list_dict[item["user"]["username"]] = {};
                        users_list_dict[item["user"]["username"]]["role"] = item["role"];
                    }
                });

                data["member_objects"].forEach((item) => {
                    let profile_photo_link = item["user"]["profile_photo"];
                    if (profile_photo_link == null)
                        profile_photo_link = "/static/img/camera_400.gif"
                    add_user(profile_photo_link, item["user"]["username"], item["role"], item["user"]["id"]);

                    users_list_dict[item["user"]["username"]] = {};
                    users_list_dict[item["user"]["username"]]["role"] = item["role"];
                    users_list_dict[item["user"]["username"]]["id"] = item["user"]["id"];

                });

                $("#users_list").css("visibility", "visible");
                $("#admin_buttons_wrapper").css("visibility", "visible");
            }
        },
        error: (data) => {
            location.replace("/web/chats");
        }
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
                let options = { year: 'numeric', month: 'long', day: 'numeric', hour: "numeric", minute: "2-digit" };
                console.log(data)
                data["results"].forEach((item) => {
                    let profile_photo_link = item["author"]["profile_photo"];
                    if (profile_photo_link == null)
                        profile_photo_link = "/static/img/camera_400.gif";

                    add_message(
                        profile_photo_link,
                        item["text"],
                        new Date(item["send_time"]).toLocaleDateString("ru-RU", options),
                        item["author"]["username"],
                        item["id"],
                        item["author"]["username"] === getCookie("username"),
                        item["author"]["username"] === getCookie("username"),
                        item["attachments"],
                        //(users_list_dict[item["author"]["username"]]["role"] <= users_list_dict[getCookie("username")]["role"]) || (item["author"]["username"] === getCookie("username"))
                        item
                    )
                });
            },
            error: (data) => {
                location.replace("/web/chats");
            }
        });
    }

    loadMessages();

    setInterval(loadMessages, 3000);


    var attachments = undefined;
    $("#attachments_input").change((e) => {
        attachments = $("#attachments_input")[0].files;
        console.log(attachments);
    });

    $("#send_message_button").on("click", (e) => {
        let message = message_input.val()

        let form_data = new FormData();
        jQuery.each(attachments, function(i, file) {
            form_data.append('attachments', file);
            console.log('attachments_'+i, file);
        });

        form_data.append("text", message);

        if(message.length !== 0 || attachments.length != 0) {
            message_input.val("")
            if (editableMessageId != undefined) {
                $.ajax({
                    url: "/chat/" + chat_id + "/message/" + editableMessageId + "/",
                    enctype: 'multipart/form-data',
                    method: "put",
                    processData: false,
                    contentType: false,
                    cache: false,
                    headers: {
                        "Authorization": "Token " + getCookie("token"),
                    },
                    data: form_data,
                    success: (data) => {
                        // add_message("", message, "", "", data["id"])
                        attachments = undefined;
                        editableMessageId = undefined;
                    }
                });
            } else {
                $.ajax({
                    url: "/chat/" + chat_id + "/message/",
                    enctype: 'multipart/form-data',
                    method: "post",
                    processData: false,
                    contentType: false,
                    cache: false,
                    headers: {
                        "Authorization": "Token " + getCookie("token"),
                    },
                    data: form_data,
                    success: (data) => {
                        // add_message("", message, "", "", data["id"])
                        attachments = undefined;
                        editableMessageId = undefined;
                    }
                });
            }
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
                let total_users = data["count"]
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