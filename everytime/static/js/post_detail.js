// 북마크 버튼
const bookmarkBtn = document.getElementById('bookmarkBtn');
const bookmarkImg = document.getElementById('bookmarkImg');

bookmarkBtn.addEventListener('click', function() {
    
    if (bookmarkImg.src.includes('Bookmark.svg')) {
        
        bookmarkImg.src = '../static/img/Bookmark_active.svg';
        bookmarkImg.alt = '북마크 취소';
    } else {
        bookmarkImg.src = '../static/img/Bookmark.svg';
        bookmarkImg.alt = '북마크 하기';
        
    }
});

// 좋아요 버튼
// 게시글 좋아요
const mainLikeBtn = document.getElementById('likeBtn');
const mainLikeBtnImg = document.getElementById('likeBtnImg');
const mainLikeCount = document.getElementById('likeCount');

if (mainLikeBtn && mainLikeBtnImg && mainLikeCount) {
    mainLikeBtn.addEventListener('click', function() {
        let currentCount = parseInt(mainLikeCount.innerText);
        
        if (mainLikeBtnImg.src.includes('LikeBtn.svg')) {
            mainLikeBtnImg.src = '../static/img/LikeBtn_active.svg';
            mainLikeBtnImg.alt = '좋아요 취소';
            mainLikeCount.innerText = currentCount + 1;
        } else {
            mainLikeBtnImg.src = '../static/img/LikeBtn.svg';
            mainLikeBtnImg.alt = '좋아요';
            mainLikeCount.innerText = currentCount - 1;
        }
    });
}

// 댓글 & 대댓글 좋아요
const commentLikeBtns = document.querySelectorAll('.comment-like-btn');

commentLikeBtns.forEach(function(btn) {
    btn.addEventListener('click', function() {
        const img = btn.querySelector('.comment-like-img');
        const countSpan = btn.querySelector('.comment-like-count');
        
        if (img && countSpan) {
            let currentCount = parseInt(countSpan.innerText);
            
            if (img.src.includes('LikeBtn.svg')) {
                img.src = '../static/img/LikeBtn_active.svg';
                img.alt = '좋아요 취소';
                countSpan.innerText = currentCount + 1;
            } else {
                img.src = '../static/img/LikeBtn.svg';
                img.alt = '좋아요';
                countSpan.innerText = currentCount - 1;
            }
        }
    });
});

// 익명 체크박스
const anonToggleBtn = document.getElementById('anonToggleBtn');
const anonCheckImg = document.getElementById('anonCheckImg');

if (anonToggleBtn && anonCheckImg) {
    anonToggleBtn.addEventListener('click', function() {
        
        if (anonCheckImg.src.includes('Checkbox.svg')) {
            anonCheckImg.src = '../static/img/Checkbox_active.svg'; // 비어있는 체크박스 이미지명으로 변경하세요!
            anonCheckImg.alt = '체크박스 해제';
        } else {
            anonCheckImg.src = '../static/img/Checkbox.svg';
            anonCheckImg.alt = '체크박스';
        }
    });
}

// 댓글 입력창 텍스트 감지
const commentInput = document.getElementById('commentInput');
const submitBtn = document.getElementById('submitBtn');
const submitBtnImg = document.getElementById('submitBtnImg');

if (commentInput && submitBtn && submitBtnImg) {
    commentInput.addEventListener('input', function() {

        if (commentInput.value.trim().length > 0) {
            submitBtn.classList.add('active');
            submitBtnImg.src = '../static/img/Submitbtn_active.svg'; 
        } else {
            submitBtn.classList.remove('active');
            submitBtnImg.src = '../static/img/Submitbtn.svg';
        }
    });
}

// 댓글 더보기 점 세 개 버튼
const dotsBtns = document.querySelectorAll('.dots-btn');

dotsBtns.forEach(function(btn) {
    btn.addEventListener('click', function(event) {
        event.stopPropagation();
        
        const container = btn.parentElement;
        
        const menu = container.querySelector('.dots-menu');
        
        document.querySelectorAll('.dots-menu').forEach(function(openMenu) {
            if (openMenu !== menu) {
                openMenu.classList.remove('show');
            }
        });
        
        menu.classList.toggle('show');
    });
});

document.addEventListener('click', function() {
    document.querySelectorAll('.dots-menu').forEach(function(menu) {
        menu.classList.remove('show');
    });
});

// 게시글 삭제 버튼
const deleteModal = document.getElementById('deleteModal');
const modalConfirmBtn = document.getElementById('modalConfirmBtn');

const postDeleteTrigger = document.querySelector('.post-actions span:first-child'); 

// [삭제] 글씨를 클릭했을 때
if (postDeleteTrigger && deleteModal) {
    postDeleteTrigger.addEventListener('click', function() {
        deleteModal.classList.add('show');
    });
}

// 모달창 내부의 [확인] 버튼을 클릭했을 때
if (modalConfirmBtn && deleteModal) {
    modalConfirmBtn.addEventListener('click', function() {
        deleteModal.classList.remove('show');
    });
}

// 댓글 정렬 버튼 토글 (최신순 ↔ 인기순)
const sortBtns = document.querySelectorAll('.comment-actions .sort-btn');

sortBtns.forEach(function(btn) {
    btn.addEventListener('click', function() {

        if (this.classList.contains('active')) {
            return;
        }
        
        document.querySelectorAll('.comment-actions .sort-btn').forEach(function(otherBtn) {
            otherBtn.classList.remove('active');
        });
        
        this.classList.add('active');
    });
});