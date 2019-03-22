import asyncio
from pyppeteer import launch
from optparse import OptionParser
import xlwt
import datetime
import requests


class Crawl:
    def __init__(self, keyword, filename, search_type, pages=10):
        self.keyword = keyword
        self.search_type = 'xls' if search_type is None else search_type
        self.pages = pages
        self.filename = filename
        self.result_count = 0
        self.run()

    def run(self):
        if self.filename is not None:
            keywords = self.readfile(self.filename)
            for keyword in keywords:
                asyncio.get_event_loop().run_until_complete(self.grabContent(keyword))
        elif self.keyword is not None:
            asyncio.get_event_loop().run_until_complete(self.grabContent(self.keyword))
        else:
            return None

    def readfile(self, filename):
        """
        读文件
        :return:
        """
        result = []
        with open(filename, 'r') as f:
            for _ in f.readlines():
                result.append(_.strip('\n'))
        return result

    def writeExcel(self, content, filename):
        """
        写excel
        :return:
        """
        f = xlwt.Workbook()
        sheet1 = f.add_sheet(filename, cell_overwrite_ok=True)
        row0 = ['标题', '域名','简介']
        for col in range(len(row0)):
            sheet1.write(0, col, row0[col])
        for row in range(len(content)):
            for col in range(len(content[row])):
                # 修改302跳转的url
                if col == 1:
                    content[row][col] = self.getLocationUrl(content[row][col])
                sheet1.write(row+1, col, content[row][col])
        now = datetime.datetime.now().strftime('%Y-%m-%d')
        f.save(filename+now+'.xls')

    def getLocationUrl(self, url):
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, sdch, br',
               'Accept-Language': 'zh-CN,zh;q=0.8',
               'Connection': 'keep-alive',
               'Host': 'pan.baidu.com',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        html = requests.get(url, headers=headers, allow_redirects=False)
        return html.headers['Location']

    async def grabContent(self, keyword):
        """
        抓取内容
        :return:
        """
        time = datetime.datetime.now()
        browser = await launch({'headless': False, 'args': ['--no-sandbox', '--disable-setuid-sandbox']})
        page = await browser.newPage()
        await page.goto('https://www.baidu.com')
        await page.waitFor(4000)
        await page.type('#kw', 'filetype:' + self.search_type + ' '+ keyword, {'delay': 100})
        await page.click('#su')
        await page.waitFor(4000)
        is_over = False
        result = []
        for _ in range(1, self.pages+1):
            try:
                next_page = await page.evaluate('()=>{var length=document.getElementsByClassName("n").length;var butn=document.getElementsByClassName("n")[length-1].text;if(butn.indexOf("下一页")==0){console.log("GO");return"GO";}else{console.log("bye");return"BYE";}}')
                # 读取内容
                with open('./libs/baidu.js', 'r') as f:
                    preloadFile = f.read()
                    result = result + await page.evaluate(preloadFile)
                # 点击下一页
                if next_page == 'GO':
                    self.result_count = self.result_count + 1
                    click_next = """()=>{var length=document.getElementsByClassName("n").length;
                                    document.getElementsByClassName("n")[length-1].click()}"""
                    await page.evaluate(click_next)
                    await page.waitFor(2000)
                else:
                    is_over = True
            except Exception as e:
                print(e)
                is_over = True
            if is_over or _ == self.pages:
                # 写excel
                self.writeExcel(result, keyword)
                endtime = datetime.datetime.now()
                print("[*] 关键词："+keyword+" 共搜索出 " + str(_) + " 页" + str(self.result_count) + " 条结果, 共耗时： "+ str((endtime-time).seconds))
                break
        await page.waitFor(4000)

        await browser.close()


def main():
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename",
                      help="关键词文件", metavar="FILE")
    parser.add_option("-t", "--type", dest="type",
                      help="搜索类型")
    parser.add_option("-k", "--keyword", dest='keyword',
                      help='关键词')
    parser.add_option("-p", "--page", dest='page',
                      help='抓取页数')
    (options, args) = parser.parse_args()
    if options.filename is None and options.type is None and options.keyword is None:
        parser.print_help()
    else:
        ca = Crawl(keyword=options.keyword, filename=options.filename, search_type=options.type, pages=int(options.page))
        if ca is None:
            parser.print_help()


if __name__ == "__main__":
    main()
