const uploadBox = document.querySelector('.uploadBox');
const fileInput = document.querySelector('.fileInput');
const uploadText = document.querySelector('.uploadInner .textLimit')

uploadBox.addEventListener('click', ()=>{
    fileInput.click();
});

fileInput.addEventListener('change', (e)=>{
    const file = e.target.files[0];
    if(!file) return;
    uploadText.innerHTML = `${file.name}선택 완료`
})