function load_logs()
{
	let container = $("#logs").empty();

	$.getJSON("/api/info", function (d)
	{
		for (let i = 0; i < d.Results.length; i++)
		{
			let log = $("<p>"+d.Results[i].time+"<br>"+d.Results[i].content+"</p>")
			container.append(log);
		}
	});
}

function load_logs_loop()
{
	load_logs();
	setTimeout(load_logs_loop, 5000);
}

$(document).ready(function()
{
	load_logs_loop();
});
