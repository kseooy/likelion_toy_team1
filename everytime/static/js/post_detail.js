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
// 대댓글 작성 폼 열기 (이름 전달받음)
function prepareReply(commentId, targetName) {
    const parentInput = document.getElementById('parentCommentId');
    const commentInput = document.getElementById('commentInput');
    const replyIndicator = document.getElementById('replyIndicator');
    const replyTargetName = document.getElementById('replyTargetName');
    
    if (parentInput && commentInput && replyIndicator && replyTargetName) {
        parentInput.value = commentId;
        replyTargetName.innerText = targetName; // 클릭한 사람 이름으로 변경
        replyIndicator.classList.add('show');   // 배너 나타나기
        commentInput.placeholder = '대댓글을 입력해주세요.';
        commentInput.focus(); // 입력창으로 커서 자동 이동
    }
}

// X 버튼 누르면 대댓글 모드 취소
document.addEventListener('DOMContentLoaded', function() {
    const cancelReplyBtn = document.getElementById('cancelReplyBtn');
    const replyIndicator = document.getElementById('replyIndicator');
    const parentInput = document.getElementById('parentCommentId');
    const commentInput = document.getElementById('commentInput');

    if (cancelReplyBtn) {
        cancelReplyBtn.addEventListener('click', function() {
            replyIndicator.classList.remove('show'); // 배너 숨김
            if (parentInput) parentInput.value = ''; // 타겟 초기화
            if (commentInput) commentInput.placeholder = '댓글을 입력해주세요.';
        });
    }
});

// 2. 게시글 메인 로직 영역
document.addEventListener('DOMContentLoaded', function() {
    // 삭제 확인
    const deleteModal = document.getElementById('deleteModal');
    const deleteTriggerBtn = document.getElementById('deleteTriggerBtn'); 

    // 익명 체크박스 토글 관련 요소
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
    const cancelDeleteBtn = document.getElementById('cancelDeleteBtn');
    if (cancelDeleteBtn && deleteModal) {
        cancelDeleteBtn.addEventListener('click', function() {
            deleteModal.classList.remove('show');
        });
    }
});

// 공유하기 버튼 및 토스트 알림 요소
const exportBtn = document.querySelector('.export-btn'); 
const copyToast = document.getElementById('copyToast');
const toastCloseBtn = document.getElementById('toastCloseBtn');
let toastTimeout; // 알림창 타이머

if (exportBtn && copyToast) {
    exportBtn.addEventListener('click', function(e) {
        e.preventDefault();
        
        // 클립보드에 현재 URL 복사
        navigator.clipboard.writeText(window.location.href).then(function() {
            // 복사 성공 시 토스트 알림창 표시
            copyToast.classList.add('show');
            
            // 만약 기존에 세팅된 타이머가 있다면 초기화
            clearTimeout(toastTimeout);
            
            // 3초뒤에 알아서 사라지도록 설정
            toastTimeout = setTimeout(function() {
                copyToast.classList.remove('show');
            }, 3000);
            
        }).catch(function(err) {
            console.error('링크 복사 실패:', err);
        });
    });
}

// X 버튼을 누르면 즉시 알림창 닫기
if (toastCloseBtn) {
    toastCloseBtn.addEventListener('click', function() {
        copyToast.classList.remove('show');
        clearTimeout(toastTimeout); // 닫은 후 타이머 꼬이지 않게 초기화
    });
}

// 전체화면 이미지 뷰어 로직
document.addEventListener('DOMContentLoaded', function() {
    const imageViewer = document.getElementById('imageViewer');
    const viewerMainImg = document.getElementById('viewerMainImg');
    const viewerCounter = document.getElementById('viewerCounter');
    const viewerCloseBtn = document.getElementById('viewerCloseBtn');
    const viewerPrevBtn = document.getElementById('viewerPrevBtn');
    const viewerNextBtn = document.getElementById('viewerNextBtn');
    
    // 본문 이미지들과 하단 썸네일들 가져오기
    const postImages = document.querySelectorAll('.post-img');
    const thumbImages = document.querySelectorAll('.viewer-thumb');
    
    let currentImageIndex = 0;
    const totalImages = postImages.length;

    if (imageViewer && totalImages > 0) {
        
        // 뷰어 화면을 특정 사진에 맞게 업데이트하는 함수
        function updateViewer(index) {
            currentImageIndex = index;
            
            // 메인 이미지 주소 바꾸기
            viewerMainImg.src = postImages[index].src;
            
            // 상단 숫자 바꾸기
            viewerCounter.innerText = `${index + 1}/${totalImages}`;
            
            // 썸네일 하얀 테두리 효과
            thumbImages.forEach(function(thumb, idx) {
                if (idx === index) {
                    thumb.classList.add('active');
                } else {
                    thumb.classList.remove('active');
                }
            });
            
            // 4. 맨 처음이거나 맨 마지막일 때 화살표 숨기기
            viewerPrevBtn.style.display = index === 0 ? 'none' : 'flex';
            viewerNextBtn.style.display = index === totalImages - 1 ? 'none' : 'flex';
        }

        // 게시글 본문 사진 클릭 시 뷰어 띄우기
        postImages.forEach(function(img, idx) {
            img.addEventListener('click', function() {
                updateViewer(idx); // 누른 사진의 인덱스로 업데이트
                imageViewer.classList.add('show');
            });
        });

        // 좌상단 뒤로가기(닫기) 버튼
        viewerCloseBtn.addEventListener('click', function() {
            imageViewer.classList.remove('show');
        });

        // 이전(〈) 버튼
        viewerPrevBtn.addEventListener('click', function() {
            if (currentImageIndex > 0) updateViewer(currentImageIndex - 1);
        });

        // 다음(〉) 버튼
        viewerNextBtn.addEventListener('click', function() {
            if (currentImageIndex < totalImages - 1) updateViewer(currentImageIndex + 1);
        });

        // 하단 썸네일 클릭 시 해당 사진으로 이동
        thumbImages.forEach(function(thumb, idx) {
            thumb.addEventListener('click', function() {
                updateViewer(idx);
            });
        });
    }
});