// Mobile nav drawer: open/close, Esc key, backdrop click, body scroll lock.
(function () {
  var toggle = document.querySelector('[data-nav-toggle]');
  var drawer = document.querySelector('[data-nav-drawer]');
  var backdrop = document.querySelector('[data-nav-backdrop]');
  if (!toggle || !drawer || !backdrop) return;

  function isOpen() {
    return !drawer.classList.contains('hidden');
  }

  function setOpen(open) {
    drawer.classList.toggle('hidden', !open);
    drawer.classList.toggle('flex', open);
    backdrop.classList.toggle('hidden', !open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    document.body.style.overflow = open ? 'hidden' : '';
  }

  toggle.addEventListener('click', function () {
    setOpen(!isOpen());
  });

  backdrop.addEventListener('click', function () {
    setOpen(false);
  });

  drawer.querySelectorAll('[data-nav-close]').forEach(function (el) {
    el.addEventListener('click', function () {
      setOpen(false);
    });
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && isOpen()) setOpen(false);
  });
})();
