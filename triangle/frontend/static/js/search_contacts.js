window.onload = () => {
    function addContactToList(username, photo_link) {
            let result = ``+
            `<li class="chat_wrap">\n` +
            `   <img class="chat_image" src="${photo_link}" alt="Profile photo"/>\n` +
            `   <div class="chat_info">\n` +
            `       <h4 class="chat_name"><a href="/web/user/${username}" class="username_link">${username}</a></h4>\n` +
            `       <p class="chat_last_message"></p>\n` +
            `   </div>\n` +
            `</li>`;

            $("#chats_list").append(result);
    }

    let users_page = 1;
    let scrolled_to_end = false;
    let search_string = null;

    function updateContent() {
        if (scrolled_to_end || search_string == null)
                return;
        $.ajax({
            url: "/user/",
            method: "GET",
            dataType: "json",
            data: {
                page: users_page,
                page_size: 10,
                username: search_string
            },
            success: (data) => {
                total_users = data["count"]
                console.log(data["results"])
                data["results"].forEach((item) => {
                    addContactToList(item["username"], item["profile_photo"] == null ? "/static/img/camera_400.gif" : item["profile_photo"]);
                });
                users_page += 1;
                scrolled_to_end = total_users < (10 * (users_page - 1));
                console.log("scrolled to end count " + scrolled_to_end)
                console.log("total_users " + total_users)
                scrollEvent();
                },
            headers: {
                "Authorization": "Token " + getCookie("token"),
            }
        });
    }

    function scrollEvent() {
        if (my_div.offsetHeight + my_div.scrollTop >= my_div.scrollHeight) {
            console.log("scrolled to end")
            updateContent();
        }
    }

    $("#username_input").on('input', (e) => {
        search_string = e.target.value;
        // if (search_string.length == 0) { // TODO: Fix?
        //     search_string = null;
        // }
        $("#chats_list").empty();
        users_page = 1;
        scrolled_to_end = false;
        updateContent();
    })


    let scroll_div = $("#contacts_scroll");

    let my_div = document.getElementById("contacts_scroll");

    scrollEvent();

    scroll_div.on('scroll', function() {
        scrollEvent();
    });
}