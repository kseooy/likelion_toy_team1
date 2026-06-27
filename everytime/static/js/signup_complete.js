document.addEventListener('DOMContentLoaded', () => {
  const fileInput = document.getElementById('profile-file-input');
  const avatarImg = document.querySelector('.p-avatar-img');
  const nicknameInput = document.getElementById('profile_nickname');
  const submitBtn = document.getElementById('profile-submit-btn');

  const DEFAULT_CHECK = "../static/img/Check.svg";
  const ACTIVE_CHECK = "../static/img/Check-on.svg";

  const status = { len: false, check: false };

  const updateUI = (elementId, isValid) => {
    const el = document.getElementById(elementId);
    if (el) {
      const img = el.querySelector('img');
      if (isValid) {
        el.classList.add('active');
        if (img) img.src = ACTIVE_CHECK;
      } else {
        el.classList.remove('active');
        if (img) img.src = DEFAULT_CHECK;
      }
    }
  };

  const validateNickname = (value) => {
    status.len = value.length >= 2 && value.length <= 12;
    updateUI('nick-len', status.len);

    status.check = value.length > 0 && value !== 'admin';
    updateUI('nick-check', status.check);

    if (status.len && status.check) {
      submitBtn.disabled = false;
      submitBtn.classList.add('active');
    } else {
      submitBtn.disabled = true;
      submitBtn.classList.remove('active');
    }
  };

  // 실행부 체킹
  if (nicknameInput && submitBtn) {
    
    // 1. 처음 들어왔을 때 값이 있으면 바로 검증 돌리기
    if (nicknameInput.value.length > 0) {
      // 닉네임이 기본으로 채워져 있다면 초기 회색 스타일(.is-default)을 강제로 지워줍니다!
      nicknameInput.classList.remove('is-default');
      validateNickname(nicknameInput.value);
    }

    // 2. 사용자가 타이핑할 때마다 실시간 검사
    nicknameInput.addEventListener('input', (e) => {
      nicknameInput.classList.remove('is-default');
      validateNickname(e.target.value);
    });
  }

  // 프로필 이미지 미리보기 (유지)
  if (fileInput && avatarImg) {
    fileInput.addEventListener('change', (e) => {
      const file = e.target.files[0];
      if (file && file.type.startsWith('image/')) {
        const imageUrl = URL.createObjectURL(file);
        avatarImg.src = imageUrl;
      }
    });
  }
});