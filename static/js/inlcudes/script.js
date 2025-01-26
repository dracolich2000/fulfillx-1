// for setting sidebar links active
document.addEventListener("DOMContentLoaded", () => {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll(".nav-link");
    navLinks.forEach(link => {
        const linkPath = link.getAttribute("href");
        if (currentPath === linkPath) {
            link.classList.add("active");
        } else {
            link.classList.remove("active");
        }
    });
});
