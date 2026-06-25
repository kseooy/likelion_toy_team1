const majorCategoryMap = {
    //글로벌융합대학
    "국어국문학전공" : "globalCollege",
    "일어일문학전공" : "globalCollege",
    "중어중문학전공" : "globalCollege",
    "미술사학전공" : "globalCollege",
    "경영학전공" : "globalCollege",
    "의상디자인전공" : "globalCollege",
    "유아교육과" : "globalCollege",
    //과학기술대학
    "디지털소프트웨어공학부" : "scienceCollege",
    "컴퓨터공학전공" : "scienceCollege",
    "사이버보안전공" : "scienceCollege",
    "수학전공" : "scienceCollege",
    "정보통계학전공" : "scienceCollege",
    "화학전공" : "scienceCollege",
    "식품영양학전공" : "scienceCollege",
    //약학대학
    "약학과" : "pharmacyCollege",
    //Art&Design대학
    "동양화전공" : "artCollege",
    "서양화전공" : "artCollege",
    "실내디자인전공" : "artCollege",
    "시각디자인전공" : "artCollege",
    "텍스타일디자인전공" : "artCollege",
    "생활체육학전공" : "artCollege",
    //미래인재대학
    "자유전공학부" : "futureCollege",
    "가상현실융합학과" : "futureCollege",
    "데이터사이언스학과" : "futureCollege",
    "AI신약학과" : "futureCollege",
    "한국학전공" : "futureCollege"
};

document.querySelectorAll(".majorBadge").forEach((major) =>{
    const majorName = major.textContent.trim();
    const majorClass = majorCategoryMap[majorName];
    if (majorClass){
        major.classList.add(majorClass);
    }

});
const params = new URLSearchParams(window.location.search);
const sort = params.get("sort");

const latestBtn = document.querySelector(".latesBtn");
const popularBtn = document.querySelector(".popularBtn");

if(sort === "popular"){
    popularBtn.classList.add("activeSort");
}else{
    latestBtn.classList.add("activeSort");
}

//프로필 박스
const profileBtn = document.querySelector(".backIcon");
const profileBox = document.querySelector(".profileBox");

profileBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    profileBox.classList.toggle("active");
});

profileBox.addEventListener("click", (e) => {
    e.stopPropagation();
});

document.addEventListener("click", () => {
    profileBox.classList.remove("active");
});