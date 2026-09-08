/* Research, strategy, plan and build: one chapter at a time. */
(() => {
  'use strict';
  document.querySelectorAll('[data-foundation]').forEach(section => {
    const tabs = [...section.querySelectorAll('[data-foundation-tab]')];
    const panels = [...section.querySelectorAll('[data-foundation-panel]')];
    const show = (index, focus = false) => {
      tabs.forEach((tab, i) => {
        tab.setAttribute('aria-selected', String(i === index));
        tab.tabIndex = i === index ? 0 : -1;
      });
      panels.forEach((panel, i) => { panel.hidden = i !== index; });
      section.dataset.foundationStage = String(index);
      if (focus) tabs[index].focus();
    };
    tabs.forEach((tab, index) => {
      tab.addEventListener('click', () => show(index));
      tab.addEventListener('keydown', event => {
        let next = index;
        if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
        else if (event.key === 'ArrowLeft') next = (index - 1 + tabs.length) % tabs.length;
        else if (event.key === 'Home') next = 0;
        else if (event.key === 'End') next = tabs.length - 1;
        else return;
        event.preventDefault();
        show(next, true);
      });
    });
    show(0);
    section.querySelector('[role="tablist"]').hidden = false;
    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver(entries => {
        if (entries.some(entry => entry.isIntersecting)) {
          section.classList.add('is-ready');
          observer.disconnect();
        }
      }, {threshold: .12});
      observer.observe(section);
    } else section.classList.add('is-ready');
  });
})();
