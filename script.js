// ---------- Add after your renderSites() function ----------

// Map + audio setup
let currentSpeech = null;

function playAudioDescription(siteId, lang = "en") {
  stopAudio();
  const site = heritageSites.find(s => s.id == siteId);
  if (!site) return;

  const text = site.description?.[lang] || site.description || "";
  const msg = new SpeechSynthesisUtterance(`This is ${site.name}. ${text} ${site.importance}`);
  msg.lang = lang === "te" ? "te-IN" : lang === "hi" ? "hi-IN" : "en-US";
  window.speechSynthesis.speak(msg);
  currentSpeech = window.speechSynthesis;
}

function stopAudio() {
  if (currentSpeech) currentSpeech.cancel();
}

// Add GPS + Stop buttons dynamically
function addExtraButtons() {
  document.querySelectorAll(".site-card").forEach((card, index) => {
    const site = heritageSites[index];
    const actions = card.querySelector(".card-actions");
    if (!actions.querySelector(".map-btn")) {
      const mapBtn = document.createElement("button");
      mapBtn.className = "btn map-btn";
      mapBtn.innerHTML = '<i class="fas fa-map"></i> GPS';
      mapBtn.onclick = () => window.open(site.map, "_blank");
      actions.prepend(mapBtn);
    }
    if (!actions.querySelector(".stop-btn")) {
      const stopBtn = document.createElement("button");
      stopBtn.className = "btn stop-btn";
      stopBtn.innerHTML = '<i class="fas fa-volume-mute"></i>';
      stopBtn.onclick = stopAudio;
      actions.appendChild(stopBtn);
    }
  });
}

// Language dropdown (optional)
const langSelect = document.createElement("select");
langSelect.id = "language";
langSelect.innerHTML = `
  <option value="en">English</option>
  <option value="te">Telugu</option>
  <option value="hi">Hindi</option>
`;
document.querySelector(".filters")?.appendChild(langSelect);

langSelect.addEventListener("change", e => {
  const lang = e.target.value;
  document.querySelectorAll(".desc").forEach((p, i) => {
    p.textContent = heritageSites[i].description?.[lang] || heritageSites[i].description;
  });
  stopAudio();
});

// Run after renderSites
const originalRender = renderSites;
renderSites = function(sites) {
  originalRender(sites);
  addExtraButtons();
};
