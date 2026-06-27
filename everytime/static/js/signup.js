document.addEventListener("DOMContentLoaded", () => {
  const usernameInput = document.getElementById("check_username");
  const passwordInput = document.getElementById("password");
  const confirmInput = document.getElementById("check_password");
  const submitBtn = document.getElementById("submit-btn");

  const DEFAULT_CHECK = "/static/img/Check.svg";
  const ACTIVE_CHECK = "/static/img/Check-on.svg";

  const statusTracker = {
    idLen: false,
    idEng: false,
    idNum: false,
    idCheck: false,
    pwLen: false,
    pwEng: false,
    pwNum: false,
    pwSpecial: false,
    pwMatch: false,
  };

  const updateStatusUI = (elementId, isValid) => {
    const el = document.getElementById(elementId);
    if (el) {
      const img = el.querySelector("img");

      if (isValid) {
        el.classList.add("active");
        if (img) img.src = ACTIVE_CHECK;
      } else {
        el.classList.remove("active");
        if (img) img.src = DEFAULT_CHECK;
      }
    }
  };

  const toggleSubmitButton = () => {
    const allConditionsMet = Object.values(statusTracker).every(
      (status) => status === true,
    );
    if (submitBtn) submitBtn.disabled = !allConditionsMet;
  };

  // ==========================================
  // 실시간 입력 감지 - 아이디 검사
  // ==========================================
  if (usernameInput) {
    usernameInput.addEventListener("input", (e) => {
      const val = e.target.value;
      
      statusTracker.idLen = val.length >= 4 && val.length <= 12;
      updateStatusUI("id-len", statusTracker.idLen);

      statusTracker.idEng = /[a-zA-Z]/.test(val);
      updateStatusUI("id-eng", statusTracker.idEng);

      statusTracker.idNum = /[0-9]/.test(val);
      updateStatusUI("id-num", statusTracker.idNum);

      const hasKorean = /[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]/.test(val);
      statusTracker.idCheck = val.length > 0 && !hasKorean && val !== "admin";
      updateStatusUI("id-check", statusTracker.idCheck);

      if (hasKorean) {
        statusTracker.idEng = false;
        statusTracker.idNum = false;
        updateStatusUI("id-eng", false);
        updateStatusUI("id-num", false);
      }
      toggleSubmitButton();
    });
  }

  // ==========================================
  // 실시간 입력 감지 - 비밀번호 검사
  // ==========================================
  if (passwordInput) {
    passwordInput.addEventListener("input", (e) => {
      const val = e.target.value;
      
      statusTracker.pwLen = val.length >= 8 && val.length <= 20;
      updateStatusUI("pw-len", statusTracker.pwLen);

      statusTracker.pwEng = /[a-zA-Z]/.test(val);
      updateStatusUI("pw-eng", statusTracker.pwEng); // 🌟 오타 라인 1줄 제거 완료

      statusTracker.pwNum = /[0-9]/.test(val);
      updateStatusUI("pw-num", statusTracker.pwNum);

      statusTracker.pwSpecial = /[{}[\]/?.,;:|)*~`!^\-_+<>@###$%&='"\\]/.test(val);
      updateStatusUI("pw-special", statusTracker.pwSpecial);

      if (confirmInput) {
        statusTracker.pwMatch = val.length > 0 && val === confirmInput.value;
        updateStatusUI("pw-match", statusTracker.pwMatch);
      }
      toggleSubmitButton();
    });
  }

  // ==========================================
  // 실시간 입력 감지 - 비밀번호 확인 검사
  // ==========================================
  if (confirmInput) {
    confirmInput.addEventListener("input", (e) => {
      const val = e.target.value;
      if (passwordInput) {
        statusTracker.pwMatch = val.length > 0 && val === passwordInput.value;
        updateStatusUI("pw-match", statusTracker.pwMatch);
      }
      toggleSubmitButton();
    });
  }

  // ==========================================
  // 비밀번호 보이기 / 숨기기 토글 기능 (괄호 안으로 안전하게 진입 🌟)
  // ==========================================
  const inputContainers = document.querySelectorAll(".input-container");
  inputContainers.forEach((container) => {
    const pInput = container.querySelector('input[type="password"], input[type="text"]');
    const toggleBtn = container.querySelector(".password-toggle-btn");

    if (pInput && toggleBtn) {
      const toggleImg = toggleBtn.querySelector("img");
      toggleBtn.addEventListener("click", () => {
        if (pInput.type === "password") {
          pInput.type = "text";
          if (toggleImg) toggleImg.src = "/static/img/icon-eye-off.svg";
        } else {
          pInput.type = "password";
          if (toggleImg) toggleImg.src = "/static/img/icon-eye.svg";
        }
      });
    }
  });

});