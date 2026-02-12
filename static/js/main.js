window.SkillMart = (function () {
  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
    return "";
  }

  function csrfToken() {
    return getCookie("csrftoken");
  }

  function initThemeToggle() {
    const btn = document.getElementById("themeToggle");
    if (!btn) return;
    const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    const saved = localStorage.getItem("skillmart-theme");
    let theme = saved || (prefersDark ? "dark" : "light");
    document.documentElement.dataset.theme = theme;
    btn.textContent = theme === "dark" ? "🌙" : "☀";

    btn.addEventListener("click", () => {
      theme = theme === "dark" ? "light" : "dark";
      document.documentElement.dataset.theme = theme;
      localStorage.setItem("skillmart-theme", theme);
      btn.textContent = theme === "dark" ? "🌙" : "☀";
    });
  }

  document.addEventListener("DOMContentLoaded", () => {
    initThemeToggle();
  });

  return {
    csrfToken,
  };
})();

