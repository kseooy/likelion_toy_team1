function deleteKeyword(keyword, btnElement) {
    // 장고 CSRF 토큰 추출 함수
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // HTML에서 글로벌 변수로 정의한 DELETE_KEYWORD_URL을 사용해 API 호출
    fetch(DELETE_KEYWORD_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ 'keyword': keyword })
    })
    .then(response => response.json())
    .then(data => {
        if (data.result === 'success') {
            // 성공 시 화면에서 해당 검색어 태그(li) 삭제
            const liElement = btnElement.closest('li');
            if (liElement) liElement.remove();

            // 만약 모든 검색어가 삭제되었다면 '최근 검색어가 없습니다' 문구 동적 노출
            const ulElement = document.getElementById('recent-search-tags');
            if (ulElement && ulElement.children.length === 0) {
                ulElement.remove();
                
                const recentSection = document.querySelector('.recent-search-section');
                if (recentSection) {
                    const emptyMsg = document.createElement('p');
                    emptyMsg.className = 'empty-msg';
                    emptyMsg.id = 'recent-empty-msg';
                    emptyMsg.textContent = '최근 검색어가 없습니다';
                    recentSection.appendChild(emptyMsg);
                }

                // 상단 '전체 삭제' 버튼 숨기기
                const clearBtn = document.querySelector('.clear-all-btn');
                if (clearBtn) clearBtn.classList.add('hide');
            }
        } else {
            alert(data.message);
        }
    })
    .catch(error => console.error('Error:', error));
}
