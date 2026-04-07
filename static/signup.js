function id_length_check() {
    let input_id = document.getElementById("user_id");
    let hint = document.querySelector(".hint");
    if (input_id.value.length === 0) {
        hint.innerText = "아이디를 입력해주세요.";
        hint.style.color = "black";
    } else
    if (input_id.value.length < 5) {
        hint.innerText = "아이디는 최소 5자 이상이어야 합니다.";
        hint.style.color = "red";
    } else {
        hint.innerText = "";
    }
}
function check_info() {
    let input_id = document.getElementById("user_id");
    if (input_id.value.length === 0) {
        document.getElementById("signupMessage").innerText = "아이디를 입력해주세요.";
        document.getElementById("signupMessage").style.color = "red";
        return false;
    }
    if (input_id.value.length < 5) {
        document.getElementById("signupMessage").innerText = "아이디는 최소 5자 이상이어야 합니다.";
        document.getElementById("signupMessage").style.color = "red";
        return false;
    }
    let pw = document.getElementById("passwd").value;
    let pw_check = document.getElementById("passwd_check").value;
    if (pw.length < 4) {
        document.getElementById("signupMessage").innerText = "비밀번호는 최소 4자 이상이어야 합니다.";
        document.getElementById("signupMessage").style.color = "red";
        return false;
    }
    if (pw !== pw_check) {
        document.getElementById("signupMessage").innerText = "비밀번호가 일치하지 않습니다.";
        document.getElementById("signupMessage").style.color = "red";
        return false;
    }
    return true;

}