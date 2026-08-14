(function () {
  function moveTocAfterMenu() {
    document.querySelectorAll('.md-nav--secondary').forEach((toc) => {
      const tocItem = toc.closest('.md-nav__item');
      if (!tocItem || tocItem.classList.contains('md-nav__item--toc')) return;

      const list = tocItem.parentElement;
      if (!list || !list.classList.contains('md-nav__list')) return;

      const wrapper = document.createElement('li');
      wrapper.className = 'md-nav__item md-nav__item--toc';
      wrapper.appendChild(toc);
      list.appendChild(wrapper);
    });
  }

  function init() {
    moveTocAfterMenu();

    const observer = new MutationObserver(() => {
      moveTocAfterMenu();
    });

    observer.observe(document.body, {
      childList: true,
      subtree: true,
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }
})();
