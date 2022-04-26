window.onload =
function ()
{
    function changeDisplay(object, vis = "none") {
        return () => {
            $(object).css(
                "display", vis
            );
        };
    }

    $("#register_button").click(function (){
        changeDisplay("#choose_auth_type", "none")();
        changeDisplay("#register_container", "block")();
    }
    );

    $("#auth_button").click(function (){
        changeDisplay("#choose_auth_type", "none")();
        changeDisplay("#login_form_container", "block")();
    });

    $("#back_button").click(function (){
        changeDisplay("#choose_auth_type", "block")();
        changeDisplay("#login_form_container", "none")();
    });

    $("#login_form").submit((e) => {
        e.preventDefault();
        sessionStorage.clear();
        let reg_password = $("#reg_password").val();

        if (reg_password !== $("#reg_password_confirm").val()) {
            alert("Пароли дожны совпадать!");
            return;
        } else if (reg_password.length < 8) {
            alert("Пароль слишком короткий!");
            return;
        }

        sessionStorage.setItem("login", $("#reg_login").val());
        sessionStorage.setItem("email", $("#reg_email").val());
        sessionStorage.setItem("password", reg_password);

        changeDisplay("#confirm_email_window", "block")();
        changeDisplay("#register_container", "none")();
    });

    $("#back_button_register").click(function () {
        changeDisplay("#choose_auth_type", "block")();
        changeDisplay("#register_container", "none")();
        console.log("Clicked bak register")
    });

    $("#accept_code").submit((e) => {
        e.preventDefault();

    });

}

window.onclose = () => {
    sessionStorage.clear();
}