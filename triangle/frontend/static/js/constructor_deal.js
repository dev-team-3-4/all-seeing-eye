window.onload = () => {
    $("#form_constructor").submit((e) => {
        e.preventDefault()

        let send_data = {
                "first_user_funds": +$("#first_user_funds").val(),
                "second_user_funds": +$("#second_user_funds").val(),
                "moderator_funds": +$("#moderator_funds").val(),
                "close_contract": $("#deal_closing_checkbox").is(":checked")
            };
        const contract_id = +location.href.substring(location.href.lastIndexOf("/") + 1)
        $.ajax({
            url: `/contract/${contract_id}/withdrawal/`,
            method: "post",
            data: JSON.stringify(send_data),
            contentType: "application/json",
            success: (data) => {
                let user_id = data["id"];
                alert("Успешно")
            },
            error: (data) => {
                alert("There are moderator's funds, but the contract haven't a moderator")
            },
            headers: {
                "Authorization": "Token " + getCookie("token")
            }
        })
    })
}