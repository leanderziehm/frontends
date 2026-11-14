(function () {

  let ctx;

  function getCtx() {
    if (!ctx) {
      ctx = new (window.AudioContext || window.webkitAudioContext)();
    }
    return ctx;
  }

  function beep(freq, duration = 0.1, type = "square") {
    const c = getCtx();

    const osc = c.createOscillator();
    const gain = c.createGain();

    osc.type = type;
    osc.frequency.value = freq;

    gain.gain.value = 0.1;

    osc.connect(gain);
    gain.connect(c.destination);

    osc.start();

    gain.gain.exponentialRampToValueAtTime(0.0001, c.currentTime + duration);
    osc.stop(c.currentTime + duration);
  }

  function error() {
    beep(180, 0.12, "square");
  }

  function click() {
    beep(600, 0.05, "sine");
  }

  window.sfxEngine = {
    error,
    click
  };

})();