window.onloadqweqwe = () => {
    function validateLink(link) {
        if(link == undefined) {
            link = "/static/img/camera_400.gif";
        }
        return link
    }

    function addContract(info) {
        let first_user_link = info["first_user"]["username"]
        let second_link = info["second_user"]["username"]
        let moderator_link = info["moderator"]["username"]
        $("#chats_list").append(
        `<a href="" class="contract_link">
                <li class="deal_container">
                    <div class="user_detail">
                        <img src="/static/img/camera_400.gif" alt="" class="contract_user_photo">
                        <div class="contract_other_info">
                            <h4 class="contract_username">Петр Геннадич</h4>
                            <h5>Первый юзер</h5>
                        </div>
                    </div>
                    <div class="user_detail">
                        <img src="/static/img/camera_400.gif" alt="" class="contract_user_photo">
                        <div class="contract_other_info">
                            <h4 class="contract_username">Петр Геннадич</h4>
                            <h5>Модератор</h5>
                        </div>
                    </div>
                    <div class="user_detail">
                        <img src="/static/img/camera_400.gif" alt="" class="contract_user_photo">
                        <div class="contract_other_info">
                            <h4 class="contract_username">Петр Геннадич</h4>
                            <h5>Второй юзер</h5>
                        </div>
                    </div>

                    <h4 class="contract_status">Средства в банке</h4>
                    <h4 class="contract_status">Статус</h4>
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
            console.log(answer)

            answer["results"].forEach((item) => {
               addContract(item[""]);
            });
        },
        error: (answer) => {
            alert("error, check console!");
            console.error(answer);
        },
    });
}