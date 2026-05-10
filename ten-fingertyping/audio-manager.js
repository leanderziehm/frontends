(function () {

  const STORAGE_KEY = "audioMuted";

  const state = {
    muted: localStorage.getItem(STORAGE_KEY) === "true"
  };

  function save() {
    localStorage.setItem(STORAGE_KEY, state.muted);
  }

  function setMuted(v) {
    state.muted = v;
    save();
    window.dispatchEvent(new Event("audio-mute-change"));
  }

  function toggleMute() {
    setMuted(!state.muted);
  }

  function isMuted() {
    return state.muted;
  }

  // ---- PUBLIC API ----

  function speak(text) {
    console.log("speak",text,"state",state.muted)
    if (state.muted) return;
    window.ttsEngine?.speak(text);
  }

  function error() {
    if (state.muted) return;
    window.sfxEngine?.error();
  }

  function click() {
    if (state.muted) return;
    window.sfxEngine?.click();
  }

  window.audioManager = {
    speak,
    error,
    click,
    toggleMute,
    setMuted,
    isMuted
  };

})();