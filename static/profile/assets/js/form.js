function startTimer() {
    var timeLabel = document.getElementById("timeLabel");
    var minutes = parseInt(timeLabel.innerText.split(":")[0]);
    var seconds = parseInt(timeLabel.innerText.split(":")[1]);
    
    var interval = setInterval(function() {
      if (seconds === 0) {
        if (minutes === 0) {
          clearInterval(interval);
          document.getElementById("test").submit();
        } else {
          minutes--;
          seconds = 59;
        }
      } else {
        seconds--;
      }
      
      timeLabel.innerText = formatTime(minutes) + ":" + formatTime(seconds);
    }, 1000);
  }
  
function formatTime(time) {
    return time < 10 ? "0" + time : time;
}




const cards = document.querySelectorAll('.question');
const bullets = document.querySelectorAll('.bullet');

function showCard(index) {
  cards.forEach((card, i) => {
    if (i === index) {
      card.style.display = 'block';
      bullets[i].classList.add('bullet-active');
    } else {
      card.style.display = 'none';
      bullets[i].classList.remove('bullet-active');
    }
  });
}



