window.onload = () => {


    const contract_id =  1;
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
            }

            $("#initiator_username").text(data["first_user"]["username"])
            $("#responder_username").text(data["second_user"]["username"])


        },
        headers: {
            "Authorization": "Token " + getCookie("token"),
        },
    })
}