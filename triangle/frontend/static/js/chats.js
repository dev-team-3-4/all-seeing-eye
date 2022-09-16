window.onload = () => {
    function addChat(name, link, id, last_message='', new_messages) {
        if(link == undefined) {
            link = "/static/img/camera_400.gif";
        }

        let text_color = new_messages ? "#00FF00":"white";

        //
        let chat_id = "link_chat_" + id
        $("#chats_list").append(
        `<div id="${chat_id}" style="text-decoration: none" class="chat_frame"><li class="chat_wrap">
            <img class="chat_image" src="${link}"/>
            <div class="chat_info">
                <h4 class="chat_name">${name}</h4>
                <div class="chat_last_message" style="color: ${text_color}">${last_message}</div>
            </div>
        </li></div>`);

        $(`#${chat_id}`).click((e) => {
           e.preventDefault();
           $.ajax({
               url: `/chat/read_message/${id}/`,
               method: "put",
               dataType: "json",
               success: (data) => {
                   location.replace(`/web/chat/${id}/`);
               },
                headers: {
                    "Authorization": "Token " + getCookie("token"),
                },
           })
        });
    }

    $.ajax({
        url: "/chat/",
        method: "get",
        data: {
            "page": 1,
            "page_size": 1e9
        },
        headers: {
            "Authorization": "Token " + getCookie("token"),
        },
        success: (answer) => {
            console.log(answer)

            answer["results"].forEach((item) => {
                let last_message = item["last_message"]
                console.log(item)

                if (last_message == undefined) {
                    last_message = ""
                } else {
                    last_message = item["last_message"]["text"]
                    if (last_message.length == 0) {
                        last_message = "(Вложение)"
                    }
                }
               addChat(item["name"], item["photo"], item["id"], last_message, item["new_messages"]);
            });
        },
        error: (answer) => {
            alert("error, check console!");
            console.error(answer);
        },
    });
}