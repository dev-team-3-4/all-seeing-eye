window.onload = () => {
    function addContactToList(username, photo_link) {
            let result = ``+
            `<li class="chat_wrap">\n` +
            `   <img class="chat_image" src="${photo_link}" alt="Profile photo"/>\n` +
            `   <div class="chat_info">\n` +
            `       <h4 class="chat_name">${username}</h4>\n` +
            `       <p class="chat_last_message"></p>\n` +
            `   </div>\n` +
            `</li>`;

            $(".chats_list").append(result);
    }

    let users_page = 1;
    let scrolled_to_end = false;

    function scrolledToBottom() {
        if (my_div.offsetHeight + my_div.scrollTop >= my_div.scrollHeight) {
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
                        addContactToList(item["username"], item["profile_photo"] == null ? "/static/img/camera_400.gif" : item["profile_photo"]);
                    });
                    users_page += 1;
                    scrolled_to_end = total_users < (10 * users_page);
                },
                headers: {
                    "Authorization": "Token " + getCookie("token"),
                }
            });
        }
    }


    let scroll_div = $("#contacts_scroll");

    let my_div = document.getElementById("contacts_scroll");

    scrolledToBottom();

    scroll_div.on('scroll', function() {
        scrolledToBottom();
    });
}