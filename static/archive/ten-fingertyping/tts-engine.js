(function () {

  let voice = null;

  function initVoices() {
    const voices = speechSynthesis.getVoices();
    voice = voices.find(v => v.lang.includes("en")) || voices[0];
  }

  if (speechSynthesis.onvoiceschanged !== undefined) {
    speechSynthesis.onvoiceschanged = initVoices;
  }

  initVoices();

  function speak(text) {

    if (!window.speechSynthesis) return;

    window.speechSynthesis.cancel();

    const u = new SpeechSynthesisUtterance(text);

    if (voice) u.voice = voice;

    u.rate = 1;
    u.pitch = 1;
    u.volume = 1;

    window.speechSynthesis.speak(u);
  }

  window.ttsEngine = {
    speak
  };

})();