function MQTTConnect() {

// Create a client instance
client = new Paho.MQTT.Client("kotok.asuscomm.com", Number(1884), "/wss");
client.startTrace();
// set callback handlers
client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;

    console.log("attempting to connect...")
//document.getElementById("messages").innerHTML += '<span> attempting to connect... </span><br/>';
    var options = {timeout:10, 
        onSuccess: client.connect};
        client.subscribe("inTopic");

}

function onConnect_1() {

client.publish("inTopic", "1", 1, false)
document.getElementById("messages").innerHTML += '<span> Switched ON </span><br/>';


}

function onConnect_0() {

  message = new Paho.MQTT.Message("0");
  message.destinationName = "inTopic";
  client.publish("inTopic", "0", 1, false)
  client.publish(message)

  topicMessage = new Paho.MQTT.Message("0");
  topicMessage.topic = "inTopic";
  client.publish(topicMessage)
  // Print output for the user in the messages div
    document.getElementById("messages").innerHTML += '<span> Topic message: ' + topicMessage.topic + '</span><br/>';
client.connect({onSuccess:onConnect_0,
                useSSL: false});

}

// called when the client loses its connection
function onConnectionLost(responseObject) {
  if (responseObject.errorCode !== 0) {
    console.log("onConnectionLost:"+responseObject.errorMessage);
  }
}

// called when a message arrives
function onMessageArrived(message) {
  console.log("onMessageArrived:"+message.payloadString);
}