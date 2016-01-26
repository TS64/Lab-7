var url = "ws://localhost:8080/wstest";

var ws = new WebSocket(url);
var player={};
player.x=1;
player.y=1;
var data = {};
data["type"] = "join";


ws.onopen = function()
{
	/*ws.send(JSON.stringify({
		"{"type:" "join"}"
	}));*/
	//ws.send(JSON.stringify(player.x));
	ws.send(data["type"]);
	//ws.send(data);
}

ws.onmessage = function(evt)
{
	alert(evt.data);
}

ws.addToConnectionList = function()
{
	ws.send("stuff");
	alert("Add to connection list.");
}