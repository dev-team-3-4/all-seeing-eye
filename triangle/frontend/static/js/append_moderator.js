window.onload = () => {
    $("#button_append").click(() => {
        const contract_id = +location.href.substring(location.href.lastIndexOf("/") + 1)
        $.ajax({
            url: "/user/" + $("#input_moderator_name").val(),
            method: "get",
            success: (data) => {
                let user_id = data["id"];

                $.ajax({
                    url: `/contract/${contract_id}/invite/${user_id}/`,
                    method: "post",
                    success: (data) => {
                        location.href = "/web/create_deal/" + contract_id
                    },
                    error: (data) => {
                        alert("Невозможно пригласить этого пользователя!")
                        console.log(data)
                    },
                    headers: {
                        "Authorization": "Token " + getCookie("token"),
                    },
                })
            },
            error: (data) => {
                alert("Пользователя с таким ником нет!")
            },
            headers: {
                "Authorization": "Token " + getCookie("token")
            }
        })
    })
}