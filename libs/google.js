() => {

    var a_urls = document.getElementsByClassName("r");
    var result = new Array();
    for (var i = 0; i < a_urls.length; i++) {
        var link = a_urls[i].getElementsByTagName('a')[0].href;
        if (link.indexOf("www.google.com") == -1) {
            var title = a_urls[i].getElementsByClassName('LC20lb')[0].textContent;
            console.log(title);
            console.log(link);

            result[i] = [title, link, link];
        }
    }
    return result;
}