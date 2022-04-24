window.onload =
function ()
{
    function changeDisplay(object, vis = "none") {
        return function () {
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

    $("#login_form").submit(function (e) {
        e.preventDefault();
       alert("wqe");
    });

    $("#back_button_register").click(function () {
        changeDisplay("#choose_auth_type", "block")();
        changeDisplay("#register_container", "none")();
        console.log("Clicked bak register")
    });

}