function checkform(form_item, submit_id, failure_msg="資料輸入有誤") {
    var flag = [(form_item.checkValidity()).toString()]

    // check mandatory
    var required_list = form_item.getElementsByClassName("required_list")
    Array.prototype.forEach.call(required_list, function(el) {
        if (el.getElementsByClassName("select-items")[0] && el.getElementsByClassName("select-items")[0].children[0].value === "---") {
            flag.push("false")
        }
        else {
            flag.push("true")
        }
    });


    var required_mult = form_item.getElementsByClassName("required_mult")
    Array.prototype.forEach.call(required_mult, function(el) {
        var checkedValue = ""
        Array.prototype.forEach.call(el.getElementsByClassName("rad-label"), function(el_child) {
            if(el_child.children[0].checked){
                checkedValue = el_child.children[0].value;
            }
        });

        if (checkedValue === "") {
            flag.push("false")
        }
        else {
            flag.push("true")
        }
    });


    // password check
    var input_password = form_item.getElementsByClassName("inputPassword")
    Array.prototype.forEach.call(input_password, function(el) {
        var valid = el.getElementsByClassName("valid")
        if (valid.length !== 4) {
            flag.push("false")
        }
        else {
            flag.push("true")
        }
    });


    if (flag.includes("false")) {
        response_dict = {"jsAlert": true, "alert_type":"alert-danger", "alert_message":failure_msg, "alert_position":"prepend"}
        var token = document.head.querySelector("[name~=csrf-token][content]").content
        
        Sijax.request('famcy_submission_handler', [submit_id, response_dict], { data: { csrf_token: token } });
        return false
    }
    else{
        console.log("return true")
        return true
    }
}
