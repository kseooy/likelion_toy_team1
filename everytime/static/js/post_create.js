// 파일
const uploadBox = document.querySelector('.uploadBox');
const fileInput = document.querySelector('.fileInput');
const uploadText = document.querySelector('.uploadInner .textLimit');
//이미지 사진 수
const imgCnt = document.querySelector('.imgCnt');

uploadBox.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener("change", (e) => {

    const files = Array.from(e.target.files);

    // 최대 5장
    if (files.length > 5) {
        alert("이미지는 최대 5장까지 업로드할 수 있습니다.");

        fileInput.value = "";

        uploadText.innerHTML = `
            이미지를 선택해주세요.<br>
            (최대5장, 10MB 미만)
        `;

        return;
    }

    // 10MB 검사
    const isOver10MB = files.some(file => {
        return file.size > 10 * 1024 * 1024;
    });

    if (isOver10MB) {

        alert("이미지는 1장당 10MB 미만만 업로드할 수 있습니다.");

        fileInput.value = "";

        uploadText.innerHTML = `
            이미지를 선택해주세요.<br>
            (최대5장, 10MB 미만)
        `;

        return;
    }

    uploadText.innerHTML = `${files.length}장 선택 완료`;
    imgCnt.innerHTML=`${files.length}/5`;

});

//교수 선택
const majorSelect = document.querySelectorAll(".articleSelect")[0];
const professorSelect = document.querySelectorAll(".articleSelect")[1];

professorSelect.disabled = true;

const professorByCollege = {
    "글로벌융합대학" : ["박현용", "백철우", "강여선", "김성은", "이황희", "주정은", "이경옥"],
    "과학기술대학" : ["유견아", "원대연", "배주화", "송유하", "이소영"],
    "약학대학" : ["정우현", "차옥경", "권희정"],
    "Art&Design 대학" : ["박영길", "차은영", "이주연"],
    "미래인재대학" : ["신현길", "강성민","문지훈", "박성우", "임양미"]
};

majorSelect.addEventListener("change", function(){

    professorSelect.disabled = false;
    
    const selectedOption = majorSelect.options[majorSelect.selectedIndex];
    const collegeName = selectedOption.parentElement.label;

    professorSelect.innerHTML = `
        <option value="" selected disabled hidden>
            교수명을 선택하세요
        </option>
    `;
    professorByCollege[collegeName].forEach(function (professor) {
        const option = document.createElement("option");
        option.value = professor;
        option.textContent = professor;
        professorSelect.appendChild(option);
    });
    
});

//별점
const starImg = document.querySelectorAll(".starImg");
const starCnt = document.querySelector(".starCnt");

let cnt = 0;
starImg.forEach((star, index)=>{
    star.addEventListener("click",()=>{
        cnt = index + 1;

        starCnt.textContent=cnt.toFixed(1);

        starImg.forEach((s, i)=>{
            if(i < cnt){
                s.src="../static/img/icon-star-red.svg";
            }else{
                s.src="../static/img/icon-star-gray.svg";
            }
        });
});
});

//익명버튼
const checkImg = document.querySelector(".checkImg");

let isChecked = false;
checkImg.addEventListener("click", ()=>{
    isChecked = !isChecked;
    if(isChecked){
        checkImg.src="../static/img/icon-check-red.png";
    }else{
        checkImg.src="../static/img/icon-check-gray.svg";
    }
});


//필수 항목 버튼
const titleInput = document.querySelector(".articleInput");
const contentInput = document.querySelector(".articleTextarea");
const submitBtn = document.querySelector(".submitBtn");
const requiredAlert = document.querySelector(".requiredAlert");
const confirmBtn = document.querySelector(".confirmBtn");
const backBlur = document.querySelector(".backBlur");

submitBtn.addEventListener("click", function(){

    if(
    !majorSelect.value || !professorSelect.value || !(cnt > 0)
    || !titleInput.value.trim() || !contentInput.value.trim()
    ){
        requiredAlert.style.display="flex";

        //배경 블러
        backBlur.style.display="block";
    }
});

confirmBtn.addEventListener("click", ()=>{
    requiredAlert.style.display="none";
    backBlur.style.display="none";
});


//제목 글자 수
const titleCnt = document.querySelector(".textLimit1");
const inputTitle = document.querySelector(".articleInput");

inputTitle.addEventListener("input", function(){
    titleCnt.innerHTML=`${inputTitle.value.length}/50`;
});

//본문 글자 수
const textareaCnt = document.querySelector(".textLimit2");
const textareaContent = document.querySelector(".articleTextarea");

textareaContent.addEventListener("input", function(){
    textareaCnt.innerHTML=`${textareaContent.value.length}/1000`;
});