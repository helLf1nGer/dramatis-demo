(function(){
  var r = document.getElementById('replay'); if(!r) return;
  var body = document.getElementById('rbBody'); if(!body) return;
  var btn = document.getElementById('rbPlay');
  var phase = document.getElementById('rpPhase');
  var railFill = document.getElementById('rpRailFill');
  var evs = [].slice.call(body.querySelectorAll('.ev[data-step]'));
  if(!evs.length) return;

  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  r.classList.add('armed'); // hide steps only when JS is present

  // phase label per step index (the real pipeline stages)
  var phases = ['brief','brief','analyze','cast','cast','cast','cast','synth','review',
                'review','review','review','review','review','mix','mix','mix','resume','mix','export'];
  // per-step dwell (ms) before advancing; the fan stage holds long
  var dwell = function(el){
    if(el.classList.contains('rp-fan')) return 6200;
    if(el.classList.contains('rp-prod')) return 1700;
    if(el.classList.contains('rp-resume')) return 2400;
    if(el.classList.contains('think')) return 1500;
    return 1250;
  };

  var timers = [], playing = false;
  function clearAll(){ timers.forEach(function(t){ clearTimeout(t); }); timers = []; }
  function reset(){
    clearAll();
    evs.forEach(function(e){
      e.classList.remove('show','cur','active');
      var feed = e.querySelectorAll('.rp-lane-feed li'); [].forEach.call(feed,function(li){li.classList.remove('in');});
      var lanes = e.querySelectorAll('.rp-lane'); [].forEach.call(lanes,function(l){l.classList.remove('lit');});
      var foot = e.querySelector('.rp-fan-foot'); if(foot) foot.classList.remove('show');
    });
    if(railFill) railFill.style.right = '100%';
    if(phase){ phase.textContent=''; phase.classList.remove('on'); }
  }

  // animate the held parallel stage: lanes light, then findings stream in, then converge
  function runFan(el, done){
    el.classList.add('active');
    var lanes = [].slice.call(el.querySelectorAll('.rp-lane'));
    var foot = el.querySelector('.rp-fan-foot');
    if(reduce){
      lanes.forEach(function(l){ l.classList.add('lit'); });
      [].forEach.call(el.querySelectorAll('.rp-lane-feed li'),function(li){li.classList.add('in');});
      if(foot) foot.classList.add('show');
      timers.push(setTimeout(done, 900));
      return;
    }
    // 1) all three lanes light at once (the "running in parallel" beat)
    timers.push(setTimeout(function(){ lanes.forEach(function(l){ l.classList.add('lit'); }); }, 120));
    // 2) findings stream concurrently across lanes, row by row (max 3 rows)
    var feeds = lanes.map(function(l){ return [].slice.call(l.querySelectorAll('.rp-lane-feed li')); });
    var maxRows = 3, rowGap = 1100, startAt = 500;
    for(var row=0; row<maxRows; row++){
      (function(row){
        timers.push(setTimeout(function(){
          feeds.forEach(function(f){ if(f[row]) f[row].classList.add('in'); });
        }, startAt + row*rowGap));
      })(row);
    }
    // 3) converge
    timers.push(setTimeout(function(){ if(foot) foot.classList.add('show'); el.classList.remove('active'); }, startAt + maxRows*rowGap + 250));
    timers.push(setTimeout(done, startAt + maxRows*rowGap + 900));
  }

  function play(){
    if(playing) return;
    playing = true; reset();
    if(reduce){
      // show everything, expand the fan, no per-step timing fuss
      evs.forEach(function(e){ e.classList.add('show'); });
      var fan = body.querySelector('.rp-fan'); if(fan) runFan(fan, function(){});
      if(railFill) railFill.style.right='0%';
      if(phase){ phase.textContent='done'; phase.classList.add('on'); }
      playing = false;
      return;
    }
    var i = 0;
    function step(){
      if(i >= evs.length){ playing = false; return; }
      var el = evs[i];
      evs.forEach(function(x){ x.classList.remove('cur'); });
      el.classList.add('show');
      if(railFill) railFill.style.right = (100 - Math.round(((i+1)/evs.length)*100)) + '%';
      if(phase){ phase.textContent = phases[i] || ''; phase.classList.add('on'); }
      var advance = function(){ i++; step(); };
      if(el.classList.contains('rp-fan')){
        runFan(el, advance);
      } else {
        if(el.classList.contains('think')) el.classList.add('cur');
        timers.push(setTimeout(advance, dwell(el)));
      }
    }
    step();
  }

  if(btn) btn.addEventListener('click', function(){ if(playing){ reset(); playing=false; } play(); });

  if('IntersectionObserver' in window){
    var seen = false;
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(x){ if(x.isIntersecting && !seen){ seen = true; play(); io.disconnect(); } });
    }, { threshold: 0.25 });
    io.observe(r);
  } else {
    play();
  }
})();