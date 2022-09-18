window.onload = () => {
    $("#form_constructor").submit((e) => {
        e.preventDefault()
        const contract_id = +location.href.substring(location.href.lastIndexOf("/") + 1)
        $.ajax({
            url: `/contract/${contract_id}/withdrawal/`,
            method: "post",
            data: {
                "first_user_funds": +$("#first_user_funds").val(),
                "second_user_funds": +$("#second_user_funds").val(),
                "moderator_funds": +$("#moderator_funds").val(),
                "close_contract": $("#deal_closing_checkbox").is(":checked")
            },
            success: (data) => {
                let user_id = data["id"];
                alert("Успешно")
            },
            error: (data) => {
                alert("Ошибка сервера!")
            },
            headers: {
                "Authorization": "Token " + getCookie("token")
            }
        })
    })
}