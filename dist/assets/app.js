
document.documentElement.classList.add('js');
addEventListener('DOMContentLoaded',function(){
  var h=document.querySelector('.header');
  var onScroll=function(){h.classList.toggle('scrolled',scrollY>8)};
  addEventListener('scroll',onScroll,{passive:true});onScroll();
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){
      es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}});
    },{threshold:.1,rootMargin:'0px 0px -40px 0px'});
    document.querySelectorAll('.reveal').forEach(function(el){io.observe(el)});
  }else{
    document.querySelectorAll('.reveal').forEach(function(el){el.classList.add('in')});
  }
});
