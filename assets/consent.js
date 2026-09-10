/* Baner zgody na Google Analytics. Zero trackingu, dopóki ktoś nie kliknie
   "Akceptuję" — bez tego kliknięcia gtag.js nigdy się nie wczytuje. Decyzja
   trzyma się w localStorage i można ją cofnąć na /cookies.html. */
(() => {
  'use strict';
  const GA_ID = 'G-EF023N5VK3';
  const KEY = 'probatum-consent';

  const loadGA = () => {
    if (window.__gaLoaded) return;
    window.__gaLoaded = true;
    const s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', GA_ID);
  };

  const banner = document.querySelector('[data-consent-banner]');

  const hide = () => banner && (banner.hidden = true);
  const show = () => banner && (banner.hidden = false);

  const decide = (value) => {
    try { localStorage.setItem(KEY, value); } catch (e) {}
    hide();
    if (value === 'granted') loadGA();
  };

  let stored = null;
  try { stored = localStorage.getItem(KEY); } catch (e) {}

  if (stored === 'granted') loadGA();
  else if (stored !== 'denied') show();

  banner?.querySelector('[data-consent-accept]')?.addEventListener('click', () => decide('granted'));
  banner?.querySelector('[data-consent-reject]')?.addEventListener('click', () => decide('denied'));

  // Przycisk "Zmień zgodę" na /cookies.html — pokazuje baner ponownie.
  document.querySelector('[data-consent-manage]')?.addEventListener('click', (e) => {
    e.preventDefault();
    show();
    banner?.scrollIntoView({ behavior: 'smooth', block: 'end' });
  });
})();
