// Mobile menu
const nav = document.querySelector('.nav');
document.querySelector('.burger')?.addEventListener('click', () => {
  const open = nav.classList.toggle('open');
  document.querySelector('.burger').setAttribute('aria-expanded', open);
});

// Reveal on scroll
const io = new IntersectionObserver((entries) => {
  entries.forEach((e) => {
    if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
  });
}, { rootMargin: '0px 0px -8% 0px' });
document.querySelectorAll('.reveal').forEach((el) => io.observe(el));

// Gallery filter (supports ?kategori=… in the URL)
const filterBtns = document.querySelectorAll('.filters button');
const applyFilter = (f) => {
  filterBtns.forEach((b) => b.classList.toggle('active', b.dataset.filter === f));
  document.querySelectorAll('[data-cat]').forEach((el) => {
    el.classList.toggle('hide', f !== 'alla' && !el.dataset.cat.split(' ').includes(f));
  });
};
filterBtns.forEach((btn) => btn.addEventListener('click', () => {
  applyFilter(btn.dataset.filter);
  history.replaceState(null, '', btn.dataset.filter === 'alla' ? location.pathname : `?kategori=${btn.dataset.filter}`);
}));
const startCat = new URLSearchParams(location.search).get('kategori');
if (startCat && document.querySelector(`.filters [data-filter="${startCat}"]`)) applyFilter(startCat);

// Lightbox with prev/next across the visible images
const lb = document.querySelector('.lb');
if (lb) {
  const lbImg = lb.querySelector('img');
  const cap = lb.querySelector('.cap');
  let list = [], idx = 0;
  const show = (i) => {
    idx = (i + list.length) % list.length;
    const a = list[idx];
    lbImg.src = a.getAttribute('href');
    lbImg.alt = a.querySelector('img')?.alt || '';
    cap.textContent = `${lbImg.alt ? lbImg.alt + ' · ' : ''}${idx + 1} / ${list.length}`;
  };
  document.querySelectorAll('[data-lb]').forEach((a) => {
    a.addEventListener('click', (e) => {
      e.preventDefault();
      const group = a.closest('[data-lb-group]') || document;
      list = [...group.querySelectorAll('[data-lb]')].filter((x) => !x.classList.contains('hide'));
      show(list.indexOf(a));
      lb.classList.add('open');
    });
  });
  const close = () => lb.classList.remove('open');
  lb.querySelector('.prev').addEventListener('click', (e) => { e.stopPropagation(); show(idx - 1); });
  lb.querySelector('.next').addEventListener('click', (e) => { e.stopPropagation(); show(idx + 1); });
  lb.addEventListener('click', (e) => { if (e.target === lb || e.target.classList.contains('close')) close(); });
  document.addEventListener('keydown', (e) => {
    if (!lb.classList.contains('open')) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowLeft') show(idx - 1);
    if (e.key === 'ArrowRight') show(idx + 1);
  });
}

// Quote form: opens the visitor's mail client with the request prefilled
document.querySelector('#forfragan')?.addEventListener('submit', (e) => {
  e.preventDefault();
  const d = new FormData(e.target);
  const body = [
    `Namn: ${d.get('namn')}`,
    `E-post: ${d.get('epost')}`,
    `Telefon: ${d.get('telefon') || '-'}`,
    `Ort: ${d.get('ort') || '-'}`,
    `Produkter: ${d.getAll('typ').join(', ') || '-'}`,
    `Glas: ${d.get('glas') || '-'}`,
    `Leverans/montering: ${d.getAll('tjanst').join(', ') || '-'}`,
    '',
    d.get('beskrivning'),
  ].join('\n');
  location.href = `mailto:info@fvab.se?subject=${encodeURIComponent('Offertförfrågan – ' + d.get('namn'))}&body=${encodeURIComponent(body)}`;
});
