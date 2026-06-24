const sort = params.get("sort");

const latestBtn = document.querySelector(".likedPages");
const popularBtn = document.querySelector(".bookmarkPages");

if(sort === "popular"){
    popularBtn.classList.add("activeSort");
}else{
    latestBtn.classList.add("activeSort");
}