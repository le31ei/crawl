function search(){
	var a_urls = document.getElementsByClassName("list_sx1");
	var result = new Array();
	for ( var i = 0; i <a_urls.length; i++){
			var title = a_urls[i].getElementsByTagName('li')[0].textContent.replace(/\s+/g,"");
			var ip = a_urls[i].getElementsByTagName('li')[1].textContent.replace(/\s+/g,"");
			var link = a_urls[i].parentElement.parentElement.parentElement.parentElement.firstElementChild.firstElementChild.href.replace(/\s+/g,"");
			console.log(title);
			console.log(ip);
			console.log(link);
			result[i] = [title,link,ip];
		}
	return result;
}

search();