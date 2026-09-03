/* Al-banna Tutorials — portal behaviours: menu, progress tracking, feedback, year. */
(function(){
  'use strict';
  var cfgEl=document.getElementById('ab-config'); var cfg={};
  try{ cfg=JSON.parse(cfgEl?cfgEl.textContent:'{}')||{}; }catch(e){}
  var AR=(document.documentElement.lang||'').toLowerCase().indexOf('ar')===0;
  var T=AR?{complete:'وضع علامة مكتمل',done:'مكتمل ✓',of:'من',completed:'مكتملة',thanks:'شكراً لملاحظتك!',cert:'الشهادة'}
          :{complete:'Mark complete',done:'Completed ✓',of:'of',completed:'completed',thanks:'Thanks for your feedback!',cert:'Certificate'};
  var KEY='ab-progress';
  function load(){ try{ return JSON.parse(localStorage.getItem(KEY)||'{}')||{}; }catch(e){ return {}; } }
  function save(p){ try{ localStorage.setItem(KEY,JSON.stringify(p)); }catch(e){} }
  function norm(p){ return (p||'').replace(/\/ar\//,'/').replace(/_ar\.html$/,'.html').replace(/-ar\.html$/,'.html'); }
  function track(){ if(window.gtag){ try{ gtag.apply(null,arguments); }catch(e){} } }
  window.ABProgress={
    get:function(course){ var p=load(); return (p[course]||[]); },
    count:function(course){ return this.get(course).length; },
    isDone:function(course,path){ return this.get(course).indexOf(norm(path))>=0; },
    set:function(course,path,done){ var p=load(); var l=p[course]||[]; var n=norm(path); var i=l.indexOf(n);
      if(done&&i<0) l.push(n); if(!done&&i>=0) l.splice(i,1); p[course]=l; save(p);
      track('event',done?'module_complete':'module_uncomplete',{course_id:course,page_path:n}); },
    reset:function(course){ var p=load(); delete p[course]; save(p); }
  };
  // Pages with their own position:fixed top navbar: push it below the portal chrome while the chrome is in view.
  (function(){ var bar=document.querySelector('.ab-bar'); if(!bar) return; var crumbs=document.querySelector('.ab-crumbs');
    var fixed=[]; var cand=document.querySelectorAll('body *'); var n=Math.min(cand.length,600);
    for(var i=0;i<n;i++){ var el=cand[i]; if(bar.contains(el)||(crumbs&&crumbs.contains(el))||el.closest('.ab-footer')) continue;
      var cs=getComputedStyle(el); if((cs.position==='fixed'||cs.position==='sticky')&&parseInt(cs.top||'0',10)===0&&el.offsetHeight>0&&el.offsetHeight<220&&el.offsetWidth>=window.innerWidth*0.6){ if(cs.position==='fixed') fixed.push(el); } }
    if(!fixed.length) return;
    // Legacy pages reserve room for their fixed navbar with body{padding-top}; that padding also pushes
    // the portal chrome down. Pull the chrome back to the top and place the navbar under its real bottom.
    var pad=parseInt(getComputedStyle(document.body).paddingTop,10)||0;
    if(pad>0) bar.style.marginTop=(-pad)+'px';
    function place(){ var ref=crumbs||bar; var t=Math.max(0,ref.getBoundingClientRect().bottom); for(var i=0;i<fixed.length;i++) fixed[i].style.top=t+'px'; }
    place(); window.addEventListener('scroll',place,{passive:true}); window.addEventListener('resize',place);
    // keep in-page anchor targets from hiding under the shifted navbar
    var h=0; for(var i=0;i<fixed.length;i++) h=Math.max(h,fixed[i].offsetHeight); if(h) document.documentElement.style.scrollPaddingTop=(h+8)+'px';
  })();
  // Year
  var y=document.querySelectorAll('.ab-year'); for(var i=0;i<y.length;i++) y[i].textContent=new Date().getFullYear();
  // Mobile menu
  var bar=document.querySelector('.ab-bar'); var tg=document.querySelector('.ab-toggle');
  if(tg&&bar) tg.addEventListener('click',function(){ bar.classList.toggle('ab-open'); tg.setAttribute('aria-expanded',bar.classList.contains('ab-open')); });
  // Search form: keep query in the bar box on the search page
  var q=document.querySelector('.ab-search input'); if(q){ var m=location.search.match(/[?&]q=([^&]*)/); if(m&&location.pathname.indexOf('/search.html')>=0) q.value=decodeURIComponent(m[1].replace(/\+/g,' ')); }
  // Progress UI
  var slot=document.querySelector('.ab-slot');
  if(slot&&cfg.course&&cfg.course.modules&&cfg.course.modules.length){
    var c=cfg.course, total=c.modules.length;
    function render(){
      var n=Math.min(window.ABProgress.count(c.id),total); var pct=Math.round(100*n/total);
      var html='';
      if(cfg.page&&cfg.page.role==='module'){
        var done=window.ABProgress.isDone(c.id,cfg.page.path);
        html+='<button type="button" class="ab-btn'+(done?' ab-done':'')+'" data-ab-complete>'+(done?T.done:T.complete)+'</button>';
      }
      html+='<div class="ab-progress" title="'+n+' '+T.of+' '+total+' '+T.completed+'"><div class="ab-track"><div class="ab-fill" style="width:'+pct+'%"></div></div><span>'+n+'/'+total+'</span>'+
            (n>=total&&total>0?' <a class="ab-lang" href="/certificate.html?course='+encodeURIComponent(c.id)+'">'+T.cert+'</a>':'')+'</div>';
      slot.innerHTML=html;
      var b=slot.querySelector('[data-ab-complete]');
      if(b) b.addEventListener('click',function(){ window.ABProgress.set(c.id,cfg.page.path,!window.ABProgress.isDone(c.id,cfg.page.path)); render(); });
    }
    render();
  }
  // Course cards / lists that show progress (courses.html, course index)
  var els=document.querySelectorAll('[data-ab-course-progress]');
  for(var j=0;j<els.length;j++){ (function(el){ var id=el.getAttribute('data-ab-course-progress'); var total=parseInt(el.getAttribute('data-ab-total')||'0',10);
    if(!total) return; var n=Math.min(window.ABProgress.count(id),total); if(!n){ el.hidden=true; return; }
    el.hidden=false; var pct=Math.round(100*n/total);
    el.innerHTML='<div class="ab-track" style="height:6px;background:#e5e7eb;border-radius:3px;overflow:hidden"><div style="height:100%;width:'+pct+'%;background:#10b981"></div></div><small>'+n+'/'+total+' '+T.completed+'</small>'; })(els[j]); }
  // Feedback widget
  var fb=document.querySelector('.ab-feedback'); if(fb){ var bs=fb.querySelectorAll('button');
    for(var k=0;k<bs.length;k++){ bs[k].addEventListener('click',function(){ track('event','page_feedback',{helpful:this.getAttribute('data-v'),page_path:location.pathname}); fb.innerHTML='<span>'+T.thanks+'</span>'; }); } }
  // Mark active nav link
  var links=document.querySelectorAll('.ab-links a'); for(var l=0;l<links.length;l++){ var h=links[l].getAttribute('href'); if(h&&h!=='/'&&location.pathname.indexOf(h.replace(/index\.html$/,''))===0) links[l].classList.add('ab-active'); }
})();
