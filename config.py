from faker import Faker

HEADER = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Host": "www.cbirc.gov.cn",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": Faker().user_agent()
}


LIST_URL = {
    "yunnan": "http://www.cbirc.gov.cn/cbircweb/DocInfo/SelectDocItemByItemPId?itemId=1954&pageSize=18&pageIndex={0}",
    "beijing": "http://www.cbirc.gov.cn/cbircweb/DocInfo/SelectDocItemByItemPId?itemId=1855&pageSize=18&pageIndex={0}",
    "tianjing": "http://www.cbirc.gov.cn/cbircweb/DocInfo/SelectDocItemByItemPId?itemId=1789&pageSize=18&pageIndex={0}"
}

PAGE_URL = "http://www.cbirc.gov.cn/cn/static/data/DocInfo/SelectByDocId/data_docId={0}.json"

RETRY = 3

proxies = {

}