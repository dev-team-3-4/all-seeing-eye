window.onload = () => {
    function validateLink(link) {
        if(link == undefined) {
            link = "/static/img/camera_400.gif";
        }
        return link
    }

    function addContract(info) {
        let first = info["first_user"]["username"]
        let second = info["second_user"]["username"]
        let moderator = info["moderator"]

        let moderator_name = moderator == null ? "(Отсутствует)" : moderator["username"];
        $("#chats_list").append(
        `<a href="/web/create_deal/${info['id']}" class="contract_link">
                <li class="deal_container">
                    <div class="user_detail">
                        <img src="/static/img/camera_400.gif" alt="" class="contract_user_photo">
                        <div class="contract_other_info">
                            <h4 class="contract_username">${first}</h4>
                            <h5>Инициатор</h5>
                        </div>
                    </div>
                    <div class="user_detail">
                        <img src="/static/img/camera_400.gif" alt="" class="contract_user_photo">
                        <div class="contract_other_info">
                            <h4 class="contract_username">${moderator_name}</h4>
                            <h5>Модератор</h5>
                        </div>
                    </div>
                    <div class="user_detail">
                        <img src="/static/img/camera_400.gif" alt="" class="contract_user_photo">
                        <div class="contract_other_info">
                            <h4 class="contract_username">${second}</h4>
                            <h5>Ответчик</h5>
                        </div>
                    </div>

                    <h4 class="contract_status">Средства в банке: ${info["bank"]}</h4>
                    <h4 class="contract_status">Закрыт: ${info["is_closed"]? "Да": "Нет"}</h4>
                    <hr class="deals_split_line">
                </li>
            </a>`
        );
    }

    $.ajax({
        url: "/contract/",
        method: "get",
        data: {
            "page": 1,
            "page_size": 1e9
        },
        headers: {
            "Authorization": "Token " + getCookie("token"),
        },
        success: (answer) => {
            answer["results"].forEach((item) => {
                addContract(item);
            });
        },
        error: (answer) => {
            alert("error, check console!");
            console.error(answer);
        },
    });
}