function id_length_check() {
    let input_id = document.getElementById("user_id");
    let message = document.getElementById("loginMessage");
    if (input_id.value.length === 0) {
        message.innerText = "아이디를 입력해주세요.";
        message.style.color = "black";
    } else
    if (input_id.value.length < 5) {
        message.innerText = "아이디는 최소 5자 이상이어야 합니다.";
        message.style.color = "red";
    } else {
        message.innerText = "";
    }
}
