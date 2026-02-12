const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");
const sign_in_btn2 = document.querySelector("#sign-in-btn2");
const sign_up_btn2 = document.querySelector("#sign-up-btn2");

// Check if we're on the register page and initialize sign-up mode
window.addEventListener('DOMContentLoaded', function() {
    const currentPath = window.location.pathname;
    if (currentPath.includes('/register/')) {
        if (container) {
            container.classList.add("sign-up-mode");
        }
    }
});

if (sign_up_btn) {
    sign_up_btn.addEventListener("click", () => {
        container.classList.add("sign-up-mode");
    });
}

if (sign_in_btn) {
    sign_in_btn.addEventListener("click", () => {
        container.classList.remove("sign-up-mode");
    });
}

if (sign_up_btn2) {
    sign_up_btn2.addEventListener("click", () => {
        container.classList.add("sign-up-mode2");
    });
}

if (sign_in_btn2) {
    sign_in_btn2.addEventListener("click", () => {
        container.classList.remove("sign-up-mode2");
    });
}
