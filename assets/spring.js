/* Film na stronie głównej: ładowany dopiero po obrazie startowym. */
(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    var world = document.querySelector('.spring-world');
    var video = document.getElementById('spring-film');
    var controls = document.querySelector('.film-controls');
    var replay = document.getElementById('film-replay');
    var pause = document.getElementById('film-pause');
    var reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
    if (!world || !video) return;

    if (reduced.matches) {
      var reducedImage = document.querySelector('.spring-still img');
      var reducedSource = document.querySelector('.spring-still source');
      if (reducedImage && reducedImage.getAttribute('data-bloom')) reducedImage.src = reducedImage.getAttribute('data-bloom');
      if (reducedSource && reducedSource.getAttribute('data-bloom')) reducedSource.srcset = reducedSource.getAttribute('data-bloom');
      return;
    }

    var narrow = window.matchMedia('(max-width: 700px)').matches;
    var source = narrow ? video.getAttribute('data-mobile') : video.getAttribute('data-desktop');
    if (!source) return;

    function showControls() {
      if (controls) controls.hidden = false;
    }

    function play() {
      world.classList.add('is-playing');
      world.classList.remove('is-held');
      if (pause) {
        pause.hidden = false;
        pause.setAttribute('aria-pressed', 'false');
        pause.textContent = 'Zatrzymaj ruch';
      }
      var attempt = video.play();
      if (attempt && attempt.catch) {
        attempt.catch(function () {
          world.classList.remove('is-playing');
          if (replay) replay.innerHTML = '<span>↻</span> Odtwórz';
          showControls();
        });
      }
    }

    function loadFilm() {
      if (video.getAttribute('src')) return;
      video.src = source;
      video.load();
    }

    video.addEventListener('canplay', function () {
      showControls();
      play();
    }, { once: true });

    video.addEventListener('ended', function () {
      world.classList.remove('is-playing');
      world.classList.add('is-held');
      if (pause) pause.hidden = true;
      if (replay) replay.innerHTML = '<span>↻</span> Jeszcze raz';
      showControls();
    });

    video.addEventListener('error', function () {
      world.classList.remove('is-playing', 'is-held');
      if (controls) controls.hidden = true;
    });

    if (replay) replay.addEventListener('click', function () {
      video.currentTime = 0;
      play();
    });

    if (pause) pause.addEventListener('click', function () {
      if (video.paused) play();
      else {
        video.pause();
        pause.setAttribute('aria-pressed', 'true');
        pause.textContent = 'Wznów ruch';
      }
    });

    document.addEventListener('visibilitychange', function () {
      if (document.hidden && !video.paused && !video.ended) video.pause();
    });

    if ('IntersectionObserver' in window) {
      var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting && !video.paused && !video.ended) video.pause();
        });
      }, { threshold: 0.05 });
      observer.observe(world);
    }

    var still = document.querySelector('.spring-still img');
    if (still && !still.complete) still.addEventListener('load', loadFilm, { once: true });
    else window.requestAnimationFrame(loadFilm);
  });
})();
