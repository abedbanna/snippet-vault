/* Shared behaviours for pages using /assets/theme.css: theme toggle, mobile menu, scroll-top, fade-up, copy buttons, TOC highlight, solution toggles. */
(function(){
  'use strict';
  var KEY=document.body.getAttribute('data-theme-key')||'ab-theme';
  function applyTheme(t){ document.body.classList.toggle('light-mode',t==='light'); var b=document.querySelectorAll('.theme-toggle i'); for(var i=0;i<b.length;i++) b[i].className=t==='light'?'fas fa-moon':'fas fa-sun'; }
  var saved=null; try{ saved=localStorage.getItem(KEY); }catch(e){}
  applyTheme(saved||'dark');
  var toggles=document.querySelectorAll('.theme-toggle');
  for(var i=0;i<toggles.length;i++) toggles[i].addEventListener('click',function(){ var light=!document.body.classList.contains('light-mode'); applyTheme(light?'light':'dark'); try{ localStorage.setItem(KEY,light?'light':'dark'); }catch(e){} });
  var hb=document.querySelector('.hamburger'), mm=document.querySelector('.mobile-menu');
  if(hb&&mm){ hb.addEventListener('click',function(){ mm.classList.toggle('open'); }); var ls=mm.querySelectorAll('a'); for(var j=0;j<ls.length;j++) ls[j].addEventListener('click',function(){ mm.classList.remove('open'); }); }
  var st=document.querySelector('.scroll-top'); if(st){ st.addEventListener('click',function(){ window.scrollTo({top:0,behavior:'smooth'}); }); }
  var toc=document.querySelector('.toc');
  function onScroll(){ var y=window.pageYOffset; if(st) st.classList.toggle('visible',y>400); if(toc) toc.classList.toggle('visible',y>300);
    if(toc){ var items=toc.querySelectorAll('.toc-item'); var cur=null; for(var k=0;k<items.length;k++){ var id=(items[k].getAttribute('href')||'').replace('#',''); var el=id&&document.getElementById(id); if(el&&el.getBoundingClientRect().top<=140) cur=items[k]; }
      for(var k2=0;k2<items.length;k2++) items[k2].classList.toggle('active',items[k2]===cur); } }
  window.addEventListener('scroll',onScroll,{passive:true}); onScroll();
  if('IntersectionObserver' in window){ var io=new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('visible'); io.unobserve(e.target); } }); },{threshold:0});
    var fu=document.querySelectorAll('.fade-up'); for(var f=0;f<fu.length;f++) io.observe(fu[f]); } else { var fu2=document.querySelectorAll('.fade-up'); for(var g=0;g<fu2.length;g++) fu2[g].classList.add('visible'); }
  var cbs=document.querySelectorAll('.copy-btn'); for(var c=0;c<cbs.length;c++) cbs[c].addEventListener('click',function(){ var btn=this; var block=btn.parentNode; var txt=block.innerText.replace(/^\s*Copy\s*/,'').replace(/\s*Copy\s*$/,''); var done=function(){ btn.textContent='Copied!'; setTimeout(function(){ btn.textContent='Copy'; },1500); };
    if(navigator.clipboard) navigator.clipboard.writeText(txt).then(done); else { var ta=document.createElement('textarea'); ta.value=txt; document.body.appendChild(ta); ta.select(); try{ document.execCommand('copy'); }catch(e){} document.body.removeChild(ta); done(); } });
  var sts=document.querySelectorAll('.solution-toggle'); for(var s=0;s<sts.length;s++) sts[s].addEventListener('click',function(){ this.classList.toggle('open'); var n=this.nextElementSibling; if(n&&n.classList.contains('solution-content')) n.classList.toggle('show'); });
})();
