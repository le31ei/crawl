()=>{
	var a_urls = document.getElementsByClassName("b_algo")
	var result = new Array();
	for ( var i = 0; i <a_urls.length; i++){
			var link = a_urls[i].getElementsByTagName("a")[0].href;
			var title = a_urls[i].getElementsByTagName("a")[0].text;
			var domain = a_urls[i].getElementsByTagName('cite')[0].textContent;

			console.log(link);
			result[i] = [title,link,domain];
		}
	return result;	
}
