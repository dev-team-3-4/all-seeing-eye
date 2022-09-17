window.onload = () => {
    $("#button_append").click(() => {
        let price = +$("#input_deal_sum").val()
        if (price == undefined || price <= 0) {
            alert("Введите валидное число!")
            return;
        }
        console.log(typeof price)
        const contract_id = +location.href.substring(location.href.lastIndexOf("/") + 1)
        $.ajax({
            url: `/contract/${contract_id}/input/`,
            method: "post",
            dataType: "json",
            data: {
                "input_coins": price
            },
            headers: {
                "Authorization": "Token " + getCookie("token"),
            },
            success: (data) => {
                location.href = "/web/create_deal/" + contract_id
            },
            error: (data) => {
                console.log(data)
                alert("Error")
            }
        })
    })
}