window.onload = function (){
    $("#create_chat_form").on("submit", (e) => {
        e.preventDefault();
        let file = $("#upload_image_input")[0].files[0];

        let form_data = new FormData();

        if(file != undefined)
            form_data.append('photo', file);


        form_data.append('name', $("#chat_name_input").val());

        $.ajax({
            method: 'post',
            enctype: 'multipart/form-data',
            url: '/chat/',
            data: form_data,
            processData: false,
            contentType: false,
            cache: false,
            success: (answer) => {
                location.href = "/web/chat/" + answer["id"];
            },
            error: (answer) => {
                alert("error, check console!")
                console.error(answer);
            },
            timeout: 600000,
            headers: {
                "Authorization": "Token " + getCookie("token"),
            }
        });
    });

}