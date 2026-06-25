const loginCheck = document.querySelector('.loginCheckImg');

loginCheck.addEventListener("click", ()=>{
    loginCheck.classList.toggle("checked");
    
    if (loginCheck.classList.contains("checked")){
        loginCheck.src="/static/img/icon-check-red.png";
    }else{
        loginCheck.src= "/static/img/icon-check-gray.svg";
    }
    
});


const username = document.querySelector('#username');
const ps = document.querySelector('#password');
const loginBtn = document.querySelector('.loginBtn');


function checkForm() {
    const isFilled =
        username.value.trim() !== "" &&
        ps.value.trim() !== "";

    loginBtn.disabled = !isFilled;
}

username.addEventListener("input", checkForm);
ps.addEventListener("input", checkForm);

checkForm();