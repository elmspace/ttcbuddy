/*
	This module will comminucate between front-end and the server.
	It uses AJAX to send data back to the server.
	It uses promises to send either the data sent back from server side, or
	on fail, it will return "fail"
*/
function AJAX_Post(input_EndPointName, input_JSONToSend){
	// Create a Deferred object
	var d_AJAX_Call = $.Deferred();
	// Make a AJAX call
	$.ajax({
		dataType : "json",
		contentType: 'application/json;charset=UTF-8',
		type: 'POST',
		url: input_EndPointName,
		data: input_JSONToSend
	}).done(function(ResultSentBack){
		d_AJAX_Call.resolve(ResultSentBack);
	}).fail(function(err){
		d_AJAX_Call.resolve("error");
	});
	return d_AJAX_Call.promise();
}

function AJAX_Get(input_EndPointName,input_JSONToSend){
	// Create a Deferred object
	var d_AJAX_Call = $.Deferred();
	// Make a AJAX call
	$.ajax({
		type: 'GET',
		url: input_EndPointName,
		data: input_JSONToSend
	}).done(function(ResultSentBack){
		d_AJAX_Call.resolve(ResultSentBack);
	}).fail(function(err){
		d_AJAX_Call.resolve("error");
	});
	return d_AJAX_Call.promise();
}