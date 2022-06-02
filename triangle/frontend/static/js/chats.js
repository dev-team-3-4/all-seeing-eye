window.onload = () => {
    function addChat(name, link, id) {
        if(link == undefined) {
            link = "/static/img/camera_400.gif";
        }
        $("#chats_list").append(
        `<a href="/web/chat/${id}" style="text-decoration: none"><li class="chat_wrap">
            <img class="chat_image" src="${link}"/>
            <div class="chat_info">
                <h4 class="chat_name">${name}</h4>
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
               addChat(item["name"], item["photo"], item["id"]);
            });
        },
        error: (answer) => {
            alert("error, check console!");
            console.error(answer);
        },
    });
}