document.addEventListener("DOMContentLoaded", () => {
  const fileInput = document.getElementById("profile-file-input");
  const avatarImg = document.querySelector(".p-avatar-img");
  const nicknameInput = document.getElementById("profile_nickname");
  const submitBtn = document.getElementById("profile-submit-btn");
  const profileForm = document.getElementById("profile-form");
  
  // HTML에 숨겨둔 Django CSRF 토큰 가져오기
  const csrfToken = document.getElementById("csrf-token")?.value || "";

  // 이미지 경로 설정
  const DEFAULT_CHECK = "/static/img/Check.svg";
  const ACTIVE_CHECK = "/static/img/Check-on.svg";

  // 상태 관리 객체
  const status = { len: false, check: false };
  let debounceTimeout = null; // 타이핑 멈출 때까지 기다리는 타이머

  // UI 변경 함수 (체크 불 켜기/끄기)
  const updateUI = (elementId, isValid) => {
    const el = document.getElementById(elementId);
    if (el) {
      const img = el.querySelector("img");
      if (isValid) {
        el.classList.add("active");
        if (img) img.src = ACTIVE_CHECK; // 빨간 체크로 변경
      } else {
        el.classList.remove("active");
        if (img) img.src = DEFAULT_CHECK; // 회색 체크로 변경
      }
    }
  };

  // 완료 버튼 활성화/비활성화 제어
  const toggleSubmitBtn = () => {
    if (status.len && status.check) {
      submitBtn.disabled = false; // 버튼 활성화 (CSS에 의해 빨간색으로 변함)
    } else {
      submitBtn.disabled = true;  // 버튼 비활성화 (연분홍색)
    }
  };

  // 백엔드 중복 확인 API 통신 함수
  const validateNickname = async (value) => {
    const trimmedValue = value.trim();

    // 1단계: 글자 수 검증
    status.len = trimmedValue.length >= 2 && trimmedValue.length <= 12;
    updateUI("nick-len", status.len);

    // 글자 수 안 맞으면 중복 체크 요청도 안 보냄
    if (!status.len) {
      status.check = false;
      updateUI("nick-check", false);
      toggleSubmitBtn();
      return;
    }

    // 2단계: 백엔드 서버에 중복 확인 요청
    try {
      const response = await fetch("/accounts/check-nickname/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken, // CSRF 필수 토큰 첨부
        },
        body: JSON.stringify({ nickname: trimmedValue }),
      });

      const data = await response.json();

      if (response.ok && data.result === "success") {
        status.check = true; // 사용 가능한 닉네임
      } else {
        status.check = false; // 중복되었거나 사용 불가
      }
    } catch (error) {
      console.error("중복 확인 통신 에러:", error);
      status.check = false;
    }

    updateUI("nick-check", status.check);
    toggleSubmitBtn();
  };

  // 디바운스: 사용자가 타이핑을 멈추고 0.4초 뒤에 서버로 요청을 보냄 (서버 과부하 방지)
  const handleNicknameInput = (value) => {
    nicknameInput.classList.remove("is-default");
    
    if (debounceTimeout) {
      clearTimeout(debounceTimeout);
    }

    debounceTimeout = setTimeout(() => {
      validateNickname(value);
    }, 400); 
  };

  // 초기값 및 입력 이벤트 바인딩
  if (nicknameInput && submitBtn) {
    // 처음 로드되었을 때 기존 닉네임이 있으면 즉시 검증 실행
    if (nicknameInput.value.trim().length > 0) {
      nicknameInput.classList.remove("is-default");
      validateNickname(nicknameInput.value);
    }

    // 유저가 글자를 입력할 때마다 실행
    nicknameInput.addEventListener("input", (e) => {
      handleNicknameInput(e.target.value);
    });
  }

  // 프로필 사진 변경 시 미리보기 기능
  if (fileInput && avatarImg) {
    fileInput.addEventListener("change", (e) => {
      const file = e.target.files[0];
      if (file && file.type.startsWith("image/")) {
        const imageUrl = URL.createObjectURL(file);
        avatarImg.src = imageUrl; // 고른 사진으로 즉시 교체됨
      }
    });
  }

  // 폼 제출 (완료 버튼 클릭 시) -> FormData를 사용하여 텍스트와 이미지 동시 전송
  if (profileForm) {
    profileForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const formData = new FormData();
      formData.append("nickname", nicknameInput.value.trim());
      
      // 유저가 사진을 선택했다면 파일도 추가
      if (fileInput.files[0]) {
        formData.append("profile_image", fileInput.files[0]);
      }

      try {
        const response = await fetch("/accounts/profile/update/", {
          method: "POST",
          headers: {
            "X-CSRFToken": csrfToken, // CSRF 토큰 필수
          },
          body: formData, // FormData 형식으로 전송
        });

        const data = await response.json();

        if (response.ok && data.result === "success") {
          alert("프로필 설정이 완료되었습니다!");
          window.location.href = "/posts/"; // 성공 시 이동할 주소
        } else {
          alert(data.message || "오류가 발생했습니다.");
        }
      } catch (error) {
        console.error("프로필 저장 통신 에러:", error);
      }
    });
  }
});