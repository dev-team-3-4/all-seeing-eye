window.onload = () => {
    function addContactToList(username, photo_link) {
            let result = ``+
            `<li class="chat_wrap">\n` +
            `   <img class="chat_image" src="${photo_link}" alt="Profile photo"/>\n` +
            `   <div class="chat_info">\n` +
            `       <h4 class="chat_name">${username}</h4>\n` +
            `       <p class="chat_last_message">Последнее сообщение</p>\n` +
            `   </div>\n` +
            `</li>`;

            $(".chats_list").append(result);
    }

    function scrolledToBottom() {
        $.ajax({
            url: "/user/contacts/",
            method: "GET",
            dataType: "application/json",
            data: {
                page: 1,
                page_size: 10
            },
            success: (data) => {
                alert(data);
            },
            headers: {
                "Authorization": "Token " + getCookie("token"),
            }
        })
        if (my_div.offsetHeight + my_div.scrollTop >= my_div.scrollHeight) {
            for (let i = 0; i < 100; i ++) {
                addContactToList("Valerka - i", "http://localhost:8000/media/accounts_photos/GlisteningGreatKusimanse-size_restricted_RP6bk5C.gif");
            }
        }
    }


    let scroll_div = $("#contacts_scroll");

    let my_div = document.getElementById("contacts_scroll");

    scrolledToBottom();

    scroll_div.on('scroll', function() {
        scrolledToBottom();
    });
}