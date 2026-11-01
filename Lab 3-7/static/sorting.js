// Sorting page: replays the steps recorded by sorting.py as an animation.
// Loaded only on the sorting page, and only after a list has been sorted.
const steps = JSON.parse(document.getElementById("sort-steps").textContent);
const barsBox = document.getElementById("bars");
const note = document.getElementById("sort-note");
const stepText = document.getElementById("step-text");
const cmpCount = document.getElementById("cmp-count");
const movCount = document.getElementById("mov-count");
const btnRestart = document.getElementById("btn-restart");
const btnPrev = document.getElementById("btn-prev");
const btnPlay = document.getElementById("btn-play");
const btnNext = document.getElementById("btn-next");
const speed = document.getElementById("speed");

const DELAYS = [900, 500, 250, 110, 40];   // milliseconds per step for speed 1 to 5
const last = steps.length - 1;
let index = 0;
let playing = false;
let timer = null;

// Running totals, so stepping back and forth keeps the counters right.
const comparisons = [];
const moves = [];
let c = 0, m = 0;
steps.forEach((s, i) => {
  if (s.kind === "compare") c++;
  if (s.kind === "swap" || s.kind === "write") m++;
  comparisons[i] = c;
  moves[i] = m;
});

// Bar heights run from 18% (smallest value) to 100% (biggest value).
const start = steps[0].array;
const low = Math.min(...start);
const high = Math.max(...start);
function heightOf(value) {
  return high === low ? 100 : 18 + 82 * (value - low) / (high - low);
}

// One bar per item in the list.
const bars = start.map(() => {
  const bar = document.createElement("div");
  bar.className = "sort-bar";
  bar.appendChild(document.createElement("span"));
  barsBox.appendChild(bar);
  return bar;
});
if (start.length > 12) barsBox.classList.add("dense");

function delay() {
  return DELAYS[speed.value - 1];
}

function show(i) {
  index = i;
  const s = steps[i];
  const moving = s.kind === "swap" || s.kind === "write";
  bars.forEach((bar, k) => {
    bar.style.height = heightOf(s.array[k]) + "%";
    bar.firstChild.textContent = s.array[k];
    let state = "";
    if (s.active.includes(k)) state = moving ? " active lift" : " active";
    else if (s.pivot === k) state = " pivot";
    else if (s.sorted.includes(k)) state = " sorted";
    const outside = s.bounds && (k < s.bounds[0] || k > s.bounds[1]);
    bar.className = "sort-bar" + state + (outside ? " dim" : "");
  });
  note.textContent = s.note;
  stepText.textContent = `Step ${i} of ${last}`;
  cmpCount.textContent = comparisons[i];
  movCount.textContent = moves[i];
  updateControls();
}

function updateControls() {
  btnPlay.textContent = playing ? "Pause" : index >= last ? "Replay" : "Play";
  btnPrev.disabled = index === 0;
  btnNext.disabled = index >= last;
  // Do not read every step aloud while it plays; announce each one when paused.
  note.setAttribute("aria-live", playing ? "off" : "polite");
}

function tick() {
  show(index + 1);
  if (index >= last) stop();
  else timer = setTimeout(tick, delay());
}

function play() {
  if (index >= last) show(0);
  playing = true;
  updateControls();
  timer = setTimeout(tick, delay());
}

function stop() {
  playing = false;
  clearTimeout(timer);
  updateControls();
}

function setSpeed() {
  barsBox.style.setProperty("--t", Math.min(300, delay() * 0.8) + "ms");
}

btnPlay.addEventListener("click", () => (playing ? stop() : play()));
btnNext.addEventListener("click", () => { stop(); if (index < last) show(index + 1); });
btnPrev.addEventListener("click", () => { stop(); if (index > 0) show(index - 1); });
btnRestart.addEventListener("click", () => { stop(); show(0); });
speed.addEventListener("input", setSpeed);

setSpeed();
show(0);
// Start playing by itself, unless the visitor asked their device for less motion.
if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) play();
