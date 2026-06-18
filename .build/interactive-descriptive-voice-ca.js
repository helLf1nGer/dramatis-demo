/* ===== voice-card tap/keyboard reveal (vc-) — defensive vanilla IIFE ===== */
(function(){
  var cards = [].slice.call(document.querySelectorAll('.vc-card'));
  if(!cards.length) return;

  function close(card){
    card.classList.remove('is-open');
    card.setAttribute('aria-expanded','false');
  }
  function open(card){
    cards.forEach(function(c){ if(c!==card) close(c); }); // one open at a time
    card.classList.add('is-open');
    card.setAttribute('aria-expanded','true');
  }
  function toggle(card){
    if(card.classList.contains('is-open')) close(card); else open(card);
  }

  cards.forEach(function(card){
    // pointer: tap/click toggles (also fine on desktop; :hover already reveals)
    card.addEventListener('click', function(e){
      e.preventDefault();
      toggle(card);
    });
    // keyboard: Enter/Space toggles, Esc closes
    card.addEventListener('keydown', function(e){
      var k = e.key;
      if(k === 'Enter' || k === ' ' || k === 'Spacebar'){
        e.preventDefault(); toggle(card);
      } else if(k === 'Escape' || k === 'Esc'){
        if(card.classList.contains('is-open')){ close(card); }
      }
    });
    // blur via keyboard navigation: collapse the tap-state so it doesn't linger
    card.addEventListener('blur', function(){
      // keep :focus-within behaviour to CSS; only clear the explicit tap flag
      close(card);
    });
  });

  // tap-away anywhere outside an open card closes it (touch + desktop)
  document.addEventListener('click', function(e){
    if(e.target && e.target.closest && e.target.closest('.vc-card')) return;
    cards.forEach(close);
  });
  // global Esc as a fallback
  document.addEventListener('keydown', function(e){
    if(e.key === 'Escape' || e.key === 'Esc'){ cards.forEach(close); }
  });
})();