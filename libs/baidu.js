() => {
	var a_urls = document.getElementsByClassName("c-tools");
	var b_urls = document.getElementsByClassName("c-abstract");
	var result = new Array();
	for ( var i = 0; i <a_urls.length; i++) {
        try {
            var aaa = a_urls[i].getAttribute("data-tools");
            var title = JSON.parse(aaa).title;
            var link = JSON.parse(aaa).url;
            var domain = a_urls[i].parentElement.firstElementChild.text;
            var content = b_urls[i].textContent;
            result[i] = [title, link, content];
        }
        catch (e) {
            result[i] = ['', '', ''];
        }
    }
    return result;
}
