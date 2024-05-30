// For the data table
$(document).ready(function () {
  $("#profilesTable").DataTable();
});


// Download ChartJS button functionality
document.getElementById("downloadPieChart").addEventListener("click", function() {
  var a = document.createElement('a');
  a.href = myPieChart.toBase64Image();
  a.download = 'pie_chart.png';
  a.click();
});


// For notifications through channels and signals
var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
var ws_path = ws_scheme + '://' + window.location.host + "/ws/notifications/";
var socket = new WebSocket(ws_path);

socket.onmessage = function(e) {
  var data = JSON.parse(e.data);
  var message = data['message'];
  var notificationsDiv = document.getElementById('notifications');
  notificationsDiv.textContent = message;
  notificationsDiv.style.display = 'block';

  // Hide the notification after 3 seconds
  setTimeout(function() {
    notificationsDiv.style.display = 'none';
  }, 3000);
};

socket.onopen = function() {
  console.log("WebSocket connection opened.");
};

socket.onclose = function() {
  console.log("WebSocket connection closed.");
};