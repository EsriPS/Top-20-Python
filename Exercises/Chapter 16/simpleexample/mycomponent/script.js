// ----------------------------------------------------
// Just copy/paste these functions as-is:

function sendMessageToStreamlitClient(type, data) {
  var outData = Object.assign(
    {
      isStreamlitMessage: true,
      type: type,
    },
    data
  );
  window.parent.postMessage(outData, "*");
}

function init() {
  sendMessageToStreamlitClient("streamlit:componentReady", { apiVersion: 1 });
}

function setFrameHeight(height) {
  sendMessageToStreamlitClient("streamlit:setFrameHeight", { height: height });
}

// The `data` argument can be any JSON-serializable value.
function sendDataToPython(data) {
  sendMessageToStreamlitClient("streamlit:setComponentValue", data);
}

// ----------------------------------------------------
// Now modify this part of the code to fit your needs:

var myInput = document.getElementById("myinput");

// data is any JSON-serializable value you sent from Python,
// and it's already deserialized for you.
function onDataFromPython(event) {
  if (event.data.type !== "streamlit:render") return;
  myInput.value = event.data.args.input_url; // Access values sent from Python here!
}

myInput.addEventListener("change", function () {
  sendDataToPython({
    value: myInput.value,
    dataType: "json",
  });
});

// Hook things up!
window.addEventListener("message", onDataFromPython);
init();

// Hack to autoset the iframe height.
window.addEventListener("load", function () {
  window.setTimeout(function () {
    setFrameHeight(document.documentElement.clientHeight);
  }, 0);
});

// Optionally, if the automatic height computation fails you, give this component a height manually
// by commenting out below:
//setFrameHeight(200);
