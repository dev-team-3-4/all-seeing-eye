window.onload = () => {
    function addChat(name, link, id, last_message='') {
        if(link == undefined) {
            link = "/static/img/camera_400.gif";
        }
        $("#chats_list").append(
        `<a href="/web/chat/${id}" style="text-decoration: none"><li class="chat_wrap">
            <img class="chat_image" src="${link}"/>
            <div class="chat_info">
                <h4 class="chat_name">${name}</h4>
                <div class="chat_last_message">${last_message}</div>
            </div>
        </li></a>`);
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

                if (last_message == undefined)
                    last_message = ""
                else
                    last_message = item["last_message"]["text"]
               addChat(item["name"], item["photo"], item["id"], );
            });
        },
        error: (answer) => {
            alert("error, check console!");
            console.error(answer);
        },
    });
}