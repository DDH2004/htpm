$("#target-1-status").click(function()
{
	$("#target-1-contents").attr("hidden", false);
	$("#target-2-contents").attr("hidden", true);
	$("#target-3-contents").attr("hidden", true);
});

$("#target-2-status").click(function()
{
	$("#target-1-contents").attr("hidden", true);
	$("#target-2-contents").attr("hidden", false);
	$("#target-3-contents").attr("hidden", true);
});

$("#target-3-status").click(function()
{
	$("#target-1-contents").attr("hidden", true);
	$("#target-2-contents").attr("hidden", true);
	$("#target-3-contents").attr("hidden", false);
});

function update()
{
	$.getJSON("/api/info", function(d)
	{
		/* Update the logs. */
		let container = $("#logs").empty();
		for (let i = 0; i < d.Logs.length; i++)
		{
			let log = $("<p>"+d.Logs[i].time+"<br>"+d.Logs[i].content+"</p>")
			container.append(log);
		}

		/* Update the challenge completion state. */
		if ((d.Completion & 0b100) != 0)
		{
			$("#target-1-status").attr("class", "target-complete");
			$("#target-1-status").text("Complete");
		}
		if ((d.Completion & 0b010) != 0)
		{
			$("#target-2-status").attr("class", "target-complete");
			$("#target-2-status").text("Complete");
		}
		if ((d.Completion & 0b001) != 0)
		{
			$("#target-3-status").attr("class", "target-complete");
			$("#target-3-status").text("Complete");
		}
	});
}

function update_loop()
{
	update();
	setTimeout(update_loop, 5000);
}

$(document).ready(function()
{
	update_loop();
});
