function startConnect() {
    // Generate a random client ID
    clientID = "clientID-" + parseInt(Math.random() * 100);

    host = "kotok.asuscomm.com";
    port = "1884";

    // Print output for the user in the messages div
  // document.getElementById("messages").innerHTML = '<span>Connecting to: ' + host + ' on port: ' + port + '</span><br/>';
  // document.getElementById("messages").innerHTML = '<span>Using the following client value: ' + clientID + '</span><br/>';

    // Initialize new Paho client connection
    client = new Paho.MQTT.Client(host, Number(port), clientID);

    // Set callback handlers
    client.onConnectionLost = onConnectionLost;
    client.onMessageArrived = onMessageArrived;

    // Connect the client, if successful, call onConnect function
    client.connect({onSuccess:onConnect,
                useSSL: false,
                keepAliveInterval: 100});
console.log("attempting to connect...");

//  my_chart_1 = [['time', 'Distance', 'Speed']];

}

// Called when the client connects
function onConnect() {

    topic = "home/electro/all";
    client.subscribe(topic);
	
    $("#seven-seg-array").sevenSeg({ digits: 5, value: 00000, decimalPoint: true, colorOff: "grey", colorOn: "#AD1D12",colorBackground:"grey"});
    $("#seven-seg-array_v").sevenSeg({ digits: 4, value: 0000, decimalPoint: true, colorBackground:"grey" ,colorOff: "grey",colorOn: "#AD1D12",});
	$("#seven-seg-array_p").sevenSeg({ digits: 6, value: 000000, decimalPoint: true , colorBackground:"grey",colorOff: "grey",colorOn: "#AD1D12",});
    $("#seven-seg-array_e").sevenSeg({ digits: 6, value: 000000, decimalPoint: true , colorBackground:"grey",colorOff: "grey",colorOn: "#AD1D12",});
	$("#seven-seg-array_f").sevenSeg({ digits: 4, value: 0000,decimalPoint: true, colorBackground:"grey",colorOff: "grey",colorOn: "#AD1D12",});
    $("#seven-seg-array_h").sevenSeg({ digits: 4, value: 0000, decimalPoint: true, colorBackground:"grey",colorOff: "grey",colorOn: "#AD1D12",});

}

// Called when the client loses its connection
function onConnectionLost(responseObject) {
    document.getElementById("messages").innerHTML += '<span>ERROR: Connection lost</span><br/>';
    if (responseObject.errorCode !== 0) {
        document.getElementById("messages").innerHTML += '<span>ERROR: ' + + responseObject.errorMessage + '</span><br/>';
    }
}

// Called when a message arrives
function onMessageArrived(message) {
let payload = message.payloadString.split("|");
var now = new Date();
    document.getElementById("messages").innerHTML += now.getHours()+':'+ now.getMinutes()+'<span>' + 'Topic: ' + message.destinationName + '  '+ message.payloadString +'| '  + '</span><br/>';

	$("#seven-seg-array").sevenSeg({ digits: 5, value: payload[1] });
	$("#seven-seg-array_v").sevenSeg({ digits: 4, value: payload[5], decimalPoint: true });
	$("#seven-seg-array_p").sevenSeg({ digits: 6, value: payload[0] });
	$("#seven-seg-array_e").sevenSeg({ digits: 6, value: payload[2], decimalPoint: true });
	$("#seven-seg-array_f").sevenSeg({ digits: 4, value: payload[3], decimalPoint: true });
	$("#seven-seg-array_h").sevenSeg({ digits: 4, value: payload[4], decimalPoint: true });

    document.getElementById('messages').scrollTop = 9999999;

  };


// Called when the disconnection button is pressed
function startDisconnect() {
    client.disconnect();
    document.getElementById("messages").innerHTML += '<span>Disconnected</span><br/>';
}
//	setInterval('show()',1000);


