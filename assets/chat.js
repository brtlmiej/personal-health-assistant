const msgerForm = get(".msger-inputarea");
const msgerInput = get(".msger-input");
const msgerChat = get(".msger-chat");
const firstTimeSlot = get("#first-time-slot");
let msgCounter = 0;
let userName;
let messages = [];

firstTimeSlot.innerHTML = new Date().toLocaleTimeString('PL', {
    hour: '2-digit',
    minute: '2-digit',
});

const BOT_MSGS = [
"Before I will response to your question I need some information from you. What is your name?",
"What is your gender?",
"What is your age?",
"How much do you weigh?",
"How tall are you?",
"Do you have some heart disease?",
"Are you married or have you been married before?",
"Ok thank you! Now I need to think for a while. I'll be right back"
];


// Icons made by Freepik from www.flaticon.com
const BOT_IMG = "ha-icon.png";
const PERSON_IMG = "user-icon.png";
const BOT_NAME = "Personal Health Assistant";
const PERSON_NAME = "User";

msgerForm.addEventListener("submit", event => {
  event.preventDefault();

  const msgText = msgerInput.value;
  if (!msgText) return;

  appendMessage(PERSON_NAME, PERSON_IMG, "right", msgText);
  msgerInput.value = "";

  botResponse();
  if (msgCounter == BOT_MSGS.length) {
    predictDiseases();
  }
});

function predictDiseases() {
  let data = {variables: formatMessages()};
  fetch("/api/predict", {
    method: "POST",
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data)
  })
  .then((response) => response.json())
  .then((data) => {
    console.log('Data: ', data);
    prepareSummary(data);
  })
  msgCounter = 0;
  messages = [];
}

function formatMessages() {
  messages.shift();
  userName = messages.shift();
  const formattedMessages = [];
  for (const message of messages) {
    if (message.toLowerCase() == 'man') {
      formattedMessages.push(0);
    }
    else if (message.toLowerCase() == 'woman') {
      formattedMessages.push(1);
    }
    else if (message.toLowerCase() == 'other') {
      formattedMessages.push(0.5);
    }
    else if (message.toLowerCase() == 'yes') {
      formattedMessages.push(1);
    }
    else if (message.toLowerCase() == 'no') {
      formattedMessages.push(0);
    }
    else if (!isNaN(parseFloat(message))){
      formattedMessages.push(parseFloat(message) / 100.0);
    }
    else {
      formattedMessages.push(0);
    }
  }
  return formattedMessages;
}

function prepareSummary(data) {
  const getChanceString = (chance, disease) => {
    if (chance <= 25) {
      return `There are very low chances that you will have ${disease}.`
    } else if (chance > 25 && chance <= 40) {
      return `You're unlikely to have ${disease}.`
    } else if (chance > 40 && chance <= 70) {
      return `There are chances that you will have ${disease}. You should contact with your doctor.`
    } else if (chance > 70) {
      return `There is a high probability that you will have ${disease}. You should contact with doctor immediately.`
    }
  }
  const diesases = ['diabetes', 'heart-attack', 'stroke'];
  const summaryMessaegs = []
  summaryMessaegs.push(`Ok, I'm back ${userName}. Here are the results. `)
  diesases.forEach((d) => {
    summaryMessaegs.push(getChanceString(data[d] * 100, d.split('_').join(' ')));
  })
  let delay = 300;
  summaryMessaegs.forEach((m) => {
    botResponse(m, delay);
    delay += 100;
  });
  botResponse(`I've hope I was helpful enough. Have a great day!`, delay + 600);
}

function appendMessage(name, img, side, text) {
  //   Simple solution for small apps
  const msgHTML = `
    <div class="msg ${side}-msg">
      <div class="msg-img" style="background-image: url(${img})"></div>

      <div class="msg-bubble">
        <div class="msg-info">
          <div class="msg-info-name">${name}</div>
          <div class="msg-info-time">${formatDate(new Date())}</div>
        </div>

        <div class="msg-text">${text}</div>
      </div>
    </div>
  `;

  msgerChat.insertAdjacentHTML("beforeend", msgHTML);
  msgerChat.scrollTop += 500;
  if (side == 'right') {
    messages.push(text);
  }
}

function botResponse(message = null, delayMultiply = 100) {
  const msgText = message ?? BOT_MSGS[msgCounter];
  if (!message) {
    msgCounter++;
  }
  const delay = msgText.split(" ").length * delayMultiply;

  setTimeout(() => {
    appendMessage(BOT_NAME, BOT_IMG, "left", msgText);
  }, delay);
}

// Utils
function get(selector, root = document) {
  return root.querySelector(selector);
}

function formatDate(date) {
  const h = "0" + date.getHours();
  const m = "0" + date.getMinutes();

  return `${h.slice(-2)}:${m.slice(-2)}`;
}

function random(min, max) {
  return Math.floor(Math.random() * (max - min) + min);
}