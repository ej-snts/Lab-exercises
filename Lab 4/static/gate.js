// Entry popup: shown once per browser session.
const gate = document.getElementById("gate");
const yes = document.getElementById("gate-yes");
const no = document.getElementById("gate-no");

function enter() {
  gate.hidden = true;
  document.body.classList.remove("locked");
}

if (sessionStorage.getItem("cpe") === "yes") {
  enter();
} else {
  gate.hidden = false;
  yes.focus();
}

yes.addEventListener("click", () => {
  sessionStorage.setItem("cpe", "yes");
  enter();
});

no.addEventListener("click", () => {
  window.close();                  // works only if the browser allows it
  location.replace("about:blank"); // otherwise leave to a blank page
});
