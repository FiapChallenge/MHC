const checkbox = document.getElementById("menu-toggle");
const nav = document.getElementById("navbar");
const menu = document.getElementById("menu");
const navLinks = document.querySelectorAll(".nav-link");

document.body.addEventListener("click", (event) => {
  if (!nav.contains(event.target) && checkbox.checked) {
    checkbox.checked = false;
  }
  if (event.target.classList.contains("nav-link")) {
    checkbox.checked = false;
  }
});

// Back to top button
const mybutton = document.getElementById("btn-back-to-top");

const scrollFunction = () => {
  if (
    document.body.scrollTop > 200 ||
    document.documentElement.scrollTop > 200
  ) {
    mybutton.classList.remove("opacity-0");
    mybutton.classList.remove("invisible");
  } else {
    mybutton.classList.add("opacity-0");
    mybutton.classList.add("invisible");
  }
};
const backToTop = () => {
  window.scrollTo({ top: 0, behavior: "smooth" });
};

mybutton.addEventListener("click", backToTop);

window.addEventListener("scroll", scrollFunction, { passive: true });
