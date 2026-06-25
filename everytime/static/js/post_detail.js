// 북마크 버튼
const bookmarkBtn = document.getElementById('bookmarkBtn');
const bookmarkImg = document.getElementById('bookmarkImg');

if (bookmarkBtn && bookmarkImg) {
    bookmarkBtn.addEventListener('click', function() {
        if (bookmarkImg.src.includes('Bookmark_active.svg')) {
            // 이미 활성화된 상태라면 -> 비활성화(기본) 이미지로 변경
            bookmarkImg.src = bookmarkImg.dataset.inactive;
            bookmarkImg.alt = '북마크 하기';
        } else {
            // 기본 상태라면 -> 활성화 이미지로 변경
            bookmarkImg.src = bookmarkImg.dataset.active;
            bookmarkImg.alt = '북마크 취소';
        }
    });
}

// 좋아요 버튼
// 게시글 좋아요 버튼 로직
// const mainLikeBtn = document.getElementById('likeBtn');
// const mainLikeBtnImg = document.getElementById('likeBtnImg');
// const mainLikeCount = document.getElementById('likeCount');

// if (mainLikeBtn && mainLikeBtnImg && mainLikeCount) {
//     mainLikeBtn.addEventListener('click', function(e) {
//         //새로고침(깜빡임) 강제로 막음
//         e.preventDefault(); 

//         let currentCount = parseInt(mainLikeCount.innerText);
//         if (mainLikeBtnImg.src.includes('LikeBtn_active.svg')) {
//             mainLikeBtnImg.src = mainLikeBtnImg.dataset.inactive;
//             mainLikeBtnImg.alt = '좋아요';
//             mainLikeCount.innerText = currentCount - 1;
//         } else {
//             mainLikeBtnImg.src = mainLikeBtnImg.dataset.active;
//             mainLikeBtnImg.alt = '좋아요 취소';
//             mainLikeCount.innerText = currentCount + 1;
//         }
//     });
// }

/* 댓글 & 대댓글 좋아요 - 대댓글 좋아요 무한히 눌리는 오류 해결 위해 주석 처리해 뒀습니다!
const commentLikeBtns = document.querySelectorAll('.comment-like-btn');

commentLikeBtns.forEach(function(btn) {
    btn.addEventListener('click', function(e) {
        e.preventDefault();

        const img = btn.querySelector('.comment-like-img');
        const countSpan = btn.querySelector('.comment-like-count');
        
        if (img && countSpan) {
            let currentCount = parseInt(countSpan.innerText);
            
            if (img.src.includes('LikeBtn_active.svg')) {
                img.src = img.dataset.inactive;
                img.alt = '좋아요';
                countSpan.innerText = currentCount - 1;
            } else {
                img.src = img.dataset.active;
                img.alt = '좋아요 취소';
                countSpan.innerText = currentCount + 1;
            }
        }
    });
}); */

// 익명 체크박스
const anonToggleBtn = document.getElementById('anonToggleBtn');
const anonCheckImg = document.getElementById('anonCheckImg');
const anonCheckbox = document.getElementById('anonCheckbox');

if (anonToggleBtn && anonCheckImg) {
    anonToggleBtn.addEventListener('click', function() {
        
        if (anonCheckImg.src.includes('Checkbox_active.svg')) {
            // 체크 해제 상태로 변경
            anonCheckImg.src = anonCheckImg.dataset.inactive;
            anonCheckImg.alt = '체크박스';
        } else {
            // 체크 상태로 변경
            anonCheckImg.src = anonCheckImg.dataset.active;
            anonCheckImg.alt = '체크박스 해제';
        }
    });
}

// 댓글 입력창 텍스트 감지, 전송 버튼 활성화
const commentInput = document.getElementById('commentInput');
const submitBtn = document.getElementById('submitBtn');
const submitBtnImg = document.getElementById('submitBtnImg');

if (commentInput && submitBtn && submitBtnImg) {
    commentInput.addEventListener('input', function() {
        
        if (commentInput.value.trim().length > 0) {
            submitBtn.classList.add('active');
            submitBtnImg.src = submitBtnImg.dataset.active;
        } else {
            // 텍스트가 다 지워지면 다시 비활성화 상태로 복구
            submitBtn.classList.remove('active');
            submitBtnImg.src = submitBtnImg.dataset.inactive;
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

// 1. 대댓글(답글) 작성 폼 열고 닫기 토글 함수
function prepareReply(commentId) {
    const parentInput = document.getElementById('parentCommentId');
    const commentInput = document.getElementById('commentInput');
    
    if (parentInput && commentInput) {
        parentInput.value = commentId;
        commentInput.placeholder = '대댓글을 입력하세요.';
        commentInput.focus();
    }
}

// 2. 게시글 메인 로직 영역
document.addEventListener('DOMContentLoaded', function() {
    // [A] 삭제 확인 커스텀 모달창 관련 요소
    const deleteModal = document.getElementById('deleteModal');
    const deleteTriggerBtn = document.getElementById('deleteTriggerBtn'); 

    // [B] 익명 체크박스 토글 관련 요소
    const anonToggleBtn = document.getElementById('anonToggleBtn');
    const anonCheckbox = document.getElementById('anonCheckbox');
    const anonCheckImg = document.getElementById('anonCheckImg');

    // 모달창 띄우기 실행
    if (deleteTriggerBtn && deleteModal) {
        deleteTriggerBtn.addEventListener('click', function(e) {
            e.preventDefault(); 
            deleteModal.classList.add('show');
        });

        window.addEventListener('click', function(e) {
            if (e.target === deleteModal) {
                deleteModal.classList.remove('show');
            }
        });
    }

    if (anonToggleBtn && anonCheckbox && anonCheckImg) {
        anonToggleBtn.addEventListener('click', function() {
            // 라벨 클릭 시 체크박스의 checked 상태가 바뀐 직후 실행됩니다.
            if (anonCheckbox.checked) {
                anonCheckImg.src = anonCheckImg.dataset.active;
            } else {
                anonCheckImg.src = anonCheckImg.dataset.inactive;
            }
        });
    }
});