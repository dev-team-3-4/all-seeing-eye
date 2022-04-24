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

    $("#register_button").click(changeDisplay("#choose_auth_type", "none"));

    $("#auth_button").click(function (){
        changeDisplay("#choose_auth_type", "none")()
        changeDisplay("#login_form_container", "block")()
    });

    $("#back_button").click(function (){
        changeDisplay("#choose_auth_type", "block")()
        changeDisplay("#login_form_container", "none")()
    });

    $("#login_form").submit(function (e) {
        e.preventDefault();
       alert("wqe");
    });
}