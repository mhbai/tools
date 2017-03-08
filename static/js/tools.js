function trim(str)
{
	return str.replace(/^[\s,]+|[\s,]+$/gm,'');
}

function split(str)
{
	if(!str){
		return [];
	}else{
		return str.split(/[\s,]+/);
	}
}

function trim_and_split(str)
{
	return split(trim(str));
}

function collect_wordlist()
{
	var data={}
	data.wordlist=trim_and_split($('#wordlist').val());
    return data;

}

function request_wordinfo()
{
	
	$('#wordinfo').val('');

	var data=collect_wordlist();
	if(data.wordlist.length==0){
		return;
	}

	var data_str=JSON.stringify(data);
	$('#wordinfo').html("詞表統計中...");
	var obj={
		contentType:"application/json",
		type: "POST",
		url: "wordlist/",
		dataType: 'json',
		data:data_str ,
		//timeout:3000,
		error: function(xhr){
			$('#wordinfo').html("計算過程發生錯誤！");
			$('#wordinfo').html(xhr.responseText);
		},
		success: function(response){
			$('#wordinfo').html("計算完成！<br><a href='"+response.filename+"' download>詞表下載</a>");
		}
	};
	$.ajax(obj);
}
