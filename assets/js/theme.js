// Theme toggle (parchment <-> night sky).
// The boot script in each page's <head> sets data-theme before first
// paint; this wires the header button and announces changes so pages
// with canvas charts (stats.html) can re-render.
document.querySelectorAll(".theme-toggle").forEach(function (btn) {
    btn.addEventListener("click", function () {
        var next = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
        document.documentElement.setAttribute("data-theme", next);
        localStorage.setItem("theme", next);
        window.dispatchEvent(new CustomEvent("themechange", { detail: { theme: next } }));
    });
});
