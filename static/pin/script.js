// oh man so much spaghetti code don't read it pls

const pinWrapper = document.querySelector('.pin-wrapper'),
      input = pinWrapper.querySelector('.focus'),
      digits = Array.from(pinWrapper.querySelectorAll('.digit')),
      caret = pinWrapper.querySelector('.caret'),
      button = pinWrapper.querySelector('.submit'),
      mainEl = document.querySelector('main'),
      resultEl = pinWrapper.querySelector('.result'),
      reset = resultEl.querySelector('.reset');
let currentIndex = 0;
let prevLeft = 0;
let prevX = 0;
let inputLock = false;

function moveCaret(newWidth, newLeft) {
  anime({
    targets: caret,
    width: newWidth,
    left: newLeft,
    easing: 'easeInOutQuad',
    duration: 450,
    begin: () => {
      caret.classList.remove('blink')
    },
    complete: () => {
      caret.classList.add('blink')
    }
  });
}

input.oninput = e => {
  this.value = "";
  let digit = parseInt(e.data);

  if (!isNaN(digit) && !inputLock && currentIndex <= digits.length-1) {
    inputLock = true;
    let left, x, newWidth, newLeft;

    if (currentIndex < digits.length-1) {
      x = digits[currentIndex + 1].offsetLeft;
      left = x + (digits[currentIndex + 1].offsetWidth - 4) / 2;

      newWidth = [
        {value: x-prevX+5},
        {value: 4}
      ];
      newLeft = [
        {value: prevLeft},
        {value: left}
      ];
    }

    else if (currentIndex === digits.length-1) {
      x = 100;
      left = pinWrapper.offsetWidth;
      newWidth = [
        {value: x},
        {value: 70}
      ];
      newLeft = [
        {value: prevLeft},
        {value: left}
      ];
      x = pinWrapper.offsetWidth;
    }

    moveCaret(newWidth, newLeft);

    prevLeft = left;
    prevX = x;

    digits[currentIndex].dataset.digit = digit;
    digits[currentIndex].classList.add('shown');
    currentIndex++;
    setTimeout(() => {
      inputLock = false;

      if (currentIndex === digits.length) {
        mainEl.classList.add('show-button');
      }
    }, 450);

  }
};
input.onkeydown = e => {
  if (e.key === "Backspace" && !inputLock && currentIndex !== 0) {
    inputLock = true;
    currentIndex--;

    let x = digits[currentIndex].offsetLeft;
    let left = x+(digits[currentIndex].offsetWidth-4)/2;

    let newWidth = [
      {value: prevX-x+5},
      {value: 4}
    ],
        newLeft = [
          {value: left},
          {value: left}
        ];
    moveCaret(newWidth, newLeft);

    prevLeft = left;
    prevX = x;

    digits[currentIndex].classList.remove('shown');
    setTimeout(() => {
      digits[currentIndex].dataset.digit = "";
      inputLock = false;
      mainEl.classList.remove('show-button');
    }, 450);
  }

  if (e.key === "Enter" && !inputLock && currentIndex === 4) {
    submit();
  }
};
input.onfocus = e => {
  if (!currentIndex) {
    inputLock = true;
    let x = digits[0].offsetLeft;
    let left = x+(digits[currentIndex].offsetWidth-4)/2;

    let newWidth = [
      {value: left+5},
      {value: 4}
    ],
        newLeft = [
          {value: 0},
          {value: left}
        ];
    moveCaret(newWidth, newLeft);

    prevLeft = left;
    prevX = x;
    setTimeout(() => {inputLock = false;}, 450)
  }
};
input.onblur = e => {
  if (!currentIndex) {
    let q = digits[0].offsetLeft;
    let left = q+(digits[currentIndex].offsetWidth-4)/2;

    let newWidth = [
      {value: left+5},
      {value: 0}
    ],
        newLeft = [
          {value: 0},
          {value: 0}
        ];
    moveCaret(newWidth, newLeft);
  }
};

function submit() {
  inputLock = true;
  mainEl.classList.remove('show-button');
  resultEl.querySelector('.result-pin').innerText = digits.map(el => {
    return el.dataset.digit
  }).join('');
  resultEl.classList.add('shown');
}

button.onclick = submit;

reset.onclick = () => {
  caret.style.width = '0px';
  caret.style.left = '0px';
  digits.forEach(el => {
    el.dataset.digit = "";
    el.classList.remove('shown');
  });
  resultEl.classList.remove('shown');
  inputLock = false;
  currentIndex = 0;
  prevLeft = 0;
  prevX = 0;
}


var ml4 = {};
ml4.opacityIn = [0,1];
ml4.scaleIn = [0.2, 1];
ml4.scaleOut = 3;
ml4.durationIn = 800;
ml4.durationOut = 600;
ml4.delay = 500;
// Wrap every letter in a span
var textWrapper = document.querySelector('.ml12');
textWrapper.innerHTML = textWrapper.textContent.replace(/\S/g, "<span class='letter'>$&</span>");

anime.timeline({loop: false})
.add({
  targets: '.ml12 .letter',
  translateX: [1,0],
  translateZ: 0,
  opacity: [0,1],
  easing: "easeOutExpo",
  duration: 1200,
  delay: (el, i) => 500 + 30 * i
})
