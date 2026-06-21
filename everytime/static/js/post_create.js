// 전공 / 교수 선택
const majorSelect = document.getElementById("majorSelect");
const professorSelect = document.getElementById("professorSelect");

// 파일
const uploadBox = document.querySelector(".uploadBox");
const fileInput = document.querySelector(".fileInput");
const uploadText = document.querySelector(".uploadInner .textLimit");
const imgCnt = document.querySelector(".imgCnt");

uploadBox.addEventListener("click", () => {
    fileInput.click();
});

fileInput.addEventListener("change", (e) => {
    const files = Array.from(e.target.files);

    if (files.length > 5) {
        alert("이미지는 최대 5장까지 업로드할 수 있습니다.");
        fileInput.value = "";
        uploadText.innerHTML = `
            이미지를 선택해주세요.<br>
            (최대5장, 10MB 미만)
        `;
        imgCnt.innerHTML = "0/5";
        return;
    }

    const isOver10MB = files.some(file => file.size > 10 * 1024 * 1024);

    if (isOver10MB) {
        alert("이미지는 1장당 10MB 미만만 업로드할 수 있습니다.");
        fileInput.value = "";
        uploadText.innerHTML = `
            이미지를 선택해주세요.<br>
            (최대5장, 10MB 미만)
        `;
        imgCnt.innerHTML = "0/5";
        return;
    }

    uploadText.innerHTML = `${files.length}장 선택 완료`;
    imgCnt.innerHTML = `${files.length}/5`;
});

// 별점
const starImg = document.querySelectorAll(".starImg");
const starCnt = document.querySelector(".starCnt");
const ratingInput = document.getElementById("ratingInput");

let cnt = Number(ratingInput.value) || 0;

function updateStars() {
    starCnt.textContent = cnt.toFixed(1);
    ratingInput.value = cnt;

    starImg.forEach((star, index) => {
        if (index < cnt) {
            star.src = "/static/img/icon-star-red.svg";
        } else {
            star.src = "/static/img/icon-star-gray.svg";
        }
    });
}

updateStars();

starImg.forEach((star, index) => {
    star.addEventListener("click", () => {
        cnt = index + 1;
        updateStars();
    });
});

// 익명 버튼
const anonCheckbox = document.getElementById("anon");
const checkImg = document.getElementById("checkImg");

function updateCheckImg() {
    if (anonCheckbox.checked) {
        checkImg.src = "/static/img/icon-check-red.png";
    } else {
        checkImg.src = "/static/img/icon-check-gray.svg";
    }
}

updateCheckImg();

checkImg.addEventListener("click", () => {
    anonCheckbox.checked = !anonCheckbox.checked;
    updateCheckImg();
});

// 필수 항목 버튼
const titleInput = document.querySelector(".articleInput");
const contentInput = document.querySelector(".articleTextarea");
const submitBtn = document.querySelector(".submitBtn");
const requiredAlert = document.querySelector(".requiredAlert");
const confirmBtn = document.querySelector(".confirmBtn");
const backBlur = document.querySelector(".backBlur");

submitBtn.addEventListener("click", function (e) {
    if (
        !majorSelect.value ||
        !professorSelect.value ||
        !(cnt > 0) ||
        !titleInput.value.trim() ||
        !contentInput.value.trim()
    ) {
        e.preventDefault();

        requiredAlert.style.display = "flex";
        backBlur.style.display = "block";
    }
});

confirmBtn.addEventListener("click", () => {
    requiredAlert.style.display = "none";
    backBlur.style.display = "none";
});

// 제목 글자 수
const titleCnt = document.querySelector(".textLimit1");
const inputTitle = document.querySelector(".articleInput");

function updateTitleCnt() {
    titleCnt.innerHTML = `${inputTitle.value.length}/50`;
}

inputTitle.addEventListener("input", updateTitleCnt);
updateTitleCnt();

// 본문 글자 수
const textareaCnt = document.querySelector(".textLimit2");
const textareaContent = document.querySelector(".articleTextarea");

function updateTextareaCnt() {
    textareaCnt.innerHTML = `${textareaContent.value.length}/1000`;
}

textareaContent.addEventListener("input", updateTextareaCnt);
updateTextareaCnt();