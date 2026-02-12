const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");
const sign_in_btn2 = document.querySelector("#sign-in-btn2");
const sign_up_btn2 = document.querySelector("#sign-up-btn2");

// Add reCAPTCHA validation
function validateCaptcha(form) {
    const response = grecaptcha.getResponse();
    if (response.length === 0) {
        alert("Please complete the captcha verification");
        return false;
    }
    return true;
}

// Add form submission handlers
document.querySelector('.sign-in-form').addEventListener('submit', function(e) {
    if (!validateCaptcha(this)) {
        e.preventDefault();
    }
});

document.querySelector('.sign-up-form').addEventListener('submit', function(e) {
    if (!validateCaptcha(this)) {
        e.preventDefault();
    }
});

sign_up_btn.addEventListener("click", () => {
    container.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener("click", () => {
    container.classList.remove("sign-up-mode");
});

sign_up_btn2.addEventListener("click", () => {
    container.classList.add("sign-up-mode2");
});

sign_in_btn2.addEventListener("click", () => {
    container.classList.remove("sign-up-mode2");
});