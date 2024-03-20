function setBackgroundImage() {
    const currentScroll = window.pageYOffset || document.documentElement.scrollTop;
    const threshold = 300; // Adjust this value to change when the transition happens
    const backgroundImage1 = 'url("https://images.pexels.com/photos/323780/pexels-photo-323780.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1")';
    const backgroundImage2 = 'url("https://images.unsplash.com/photo-1515263487990-61b07816b324?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")';
  
    if (currentScroll >= threshold) {
      requestAnimationFrame(() => {
        document.body.style.backgroundImage = backgroundImage1;
      });
    } else {
      requestAnimationFrame(() => {
        document.body.style.backgroundImage = backgroundImage2;
      });
    }
  }
  
  window.addEventListener('scroll', setBackgroundImage);
  
  // Call the function initially to set the background image based on the initial scroll position
  setBackgroundImage();