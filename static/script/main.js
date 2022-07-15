console.log('js on')
var ham = document.getElementById('ham');
let navlinks= document.getElementById('navlinks');

ham.onclick=function(){
    document.body.classList.toggle('ham')
    if(document.body.classList.contains('ham')) {
        navlinks.style.display='flex'
        ham.src=ham.getAttribute("data-original");
        ham.setAttribute("src", src)
     
    } 
    else{
        navlinks.style.display='none'
        ham.src=ham.getAttribute("data");
        ham.setAttribute("src", src)
      
    }
  }