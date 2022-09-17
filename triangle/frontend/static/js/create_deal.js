window.onload = () => {
    function image_link_check(link) {
        if (link == null)
            return  "/static/img/camera_400.gif"
        return link
    }

    const contract_id = +location.href.substring(location.href.lastIndexOf("/") + 1)
    var moderator_invited = true;
    $.ajax({
        url: `/contract/${contract_id}/`,
        method: "get",
        success: (data) => {
            console.log(data)
            moderator_invited = data["moderator"] != undefined;
            if (moderator_invited) {
                $("#moderator_filed").text(data["moderator"]["username"]);
                $("#moderator_profile_picture").src(data["moderator"]["profile_photo"]);
                $("#invite_button").hide();
            } else {
                $("#moderator_filed").text("(Не приглашён)");
            }

            $("#initiator_username").text(data["first_user"]["username"])
            $("#responder_username").text(data["second_user"]["username"])

            $("#initiator_profile_picture").attr("src", image_link_check(data["first_user"]["profile_photo"]))
            $("#responder_profile_picture").attr("src", image_link_check(data["second_user"]["profile_photo"]))

            $("#money_in_bank").text("Средства в банке: " + data["bank"])

            $("#append_money_button").click((e) => {
                location.href = `/web/input_deal/${contract_id}`
            })

            $("#button_chat_deal").click(() => {
                location.href = `/web/chat/` + data["chat_id"];
            })

            $("#invite_button").click(() => {
                location.href = `/web/invite_moderator/` + data["id"];
            })
        },
        headers: {
            "Authorization": "Token " + getCookie("token")
        },
    });
}