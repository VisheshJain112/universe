// Animation
        window.setTimeout(function(){
            document.querySelector('#login-img').style.width = '325px'
            document.querySelector('#login-img').style.height = '300px'
            document.querySelector('#login-img').style.transform = 'rotate(1440deg)'
            document.querySelector("#login-img").style.boxShadow = "0 10px 10px grey"
        }, 750);

        window.setTimeout(function(){
            document.querySelector(".login-input").style.opacity="1";
            document.querySelector(".login-password").style.opacity = "1";
            document.querySelector(".login-btn").style.opacity="1";
            document.querySelector(".login-input").style.marginTop="0";
            document.querySelector(".login-password").style.marginTop="3%";
            document.querySelector(".login-btn").style.marginTop="0";
        },3100);