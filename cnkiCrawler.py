import time
import math
from bs4 import BeautifulSoup
from selenium import webdriver


def numbers(number):
    temp = {str(i): i for i in range(0, 100000)}
    return temp[number]


# 获取当前文献的描述信息
def get_file_info(file, soup):
    time.sleep(3)
    info = {
        'author': '',
        'organ': '',
        'abstract': '',
        'keywords': [],
        'funds': '',
        'doi': '',
        'class_num': '',
        'citing_freq': 0,
        'download_freq': 0
    }

    try:
        for item in soup.select("p"):
            if "【作者】" in item.text:
                info['author'] = item.select("a")[0].text.strip()

            if "【机构】" in item.text:
                info['organ'] = item.select("a")[0].text.strip()

            if "【摘要】" in item.text:
                info['abstract'] = item.select("#ChDivSummary")[0].text.strip()
    except:
        print('* ' + file[0]+', '+file[2] + ': 无法找到【作者】【机构】【摘要】区域，请手动查找！')
    try:
        for item in soup.select('div.keywords.int5'):
            if '【关键词】' in item.text:
                info['keywords'] = [keyword.strip() for keyword in item.text.strip().strip('【关键词】').strip('；').split('；')]

            if '【基金】' in item.text:
                info['funds'] = item.text.strip().strip("【基金】").strip()
    except:
        print('* ' + file[0]+', '+file[2] + ': 无法找到【关键词】【基金】区域，请手动查找！')

    try:
        for item in soup.select(".break li"):
            if "【DOI】" in item.text:
                info['doi'] = item.text.strip().strip("【DOI】").strip()

            if "【分类号】" in item.text:
                info['class_num'] = item.text.strip().strip("【分类号】").strip()

            if "【被引频次】" in item.text:
                info['citing_freq'] = numbers(item.text.strip().strip("【被引频次】").strip())

            if "【下载频次】" in item.text:
                info['download_freq'] = numbers(item.text.strip().strip("【下载频次】").strip())
    except:
        print('* ' + file[0]+', '+file[2] + ': 无法找到【DOI】【分类号】【被引频次】【下载频次】区域，请手动查找！')
    return info


# 获取参考文献——中国图书全文数据库
def getCBBD(file, driver):
    references = {}
    box = driver.find_element_by_xpath('//*[@id="selectlist"]')
    box.send_keys('中国图书全文数据库')
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    count = numbers(soup.select('.count')[0].text.split('到')[1].split('条')[0].strip())
    pages = int(math.ceil(count / 10.0))
    if pages == 0:
        pass
    else:
        page = 1
        try:
            while True:
                for li in soup.select('.content li'):
                    num = li.text.split('.')[0].strip().split(']')[0].split('[')[1].strip()
                    references[num] = {}
                    if len(li.text.split('.')) == 3:
                        references[num]['author'] = li.text.split('.')[0].strip().split(']')[1].strip()
                        references[num]['title'] = li.text.split('.')[1].strip()
                        references[num]['publisher'] = li.text.split('.')[2].strip().split(',')[0].strip()
                        references[num]['year'] = li.text.split('.')[2].strip().split(',')[1].strip()
                    else:
                        references[num] = li.text.strip()
                if page == pages:
                    break
                else:
                    time.sleep(5)
                    driver.find_element_by_link_text(str(page + 1)).click()
                    time.sleep(5)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                page = page + 1
        except:
            print('% ' + file[0] + ', ' + file[2] + ': ' + '中国图书全文数据库的参考文献没加载完成！')
    return references


# 获取参考文献——中国重要报纸全文数据库
def getCCND(file, driver):
    references = {}
    box = driver.find_element_by_xpath('//*[@id="selectlist"]')
    box.send_keys('中国重要报纸全文数据库')
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    count = numbers(soup.select('.count')[0].text.split('到')[1].split('条')[0].strip())
    pages = int(math.ceil(count / 10.0))
    if pages == 0:
        pass
    else:
        page = 1
        try:
            while True:
                for li in soup.select('.content li'):
                    num = li.text.split('.')[0].strip().split(']')[0].split('[')[1].strip()
                    references[num] = {}
                    if len(li.text.split('.')) == 4:
                        references[num]['author'] = li.text.split('.')[0].strip().split(']')[1].strip()
                        references[num]['title'] = li.text.split('.')[1].strip()
                        references[num]['publisher'] = li.text.split('.')[2].strip()

                        year = li.text.split('.')[-1].split('(')[0].strip()
                        issue = li.text.split('.')[-1].split('(')[1].strip().split(')')[0].strip()
                        references[num]['issue'] = year + '年' + issue + '期'

                        try:
                            references[num]['filename'] = li.select('a')[0]['href'].split('filename=')[1].split('&')[
                                0].strip()
                        except:
                            references[num]['filename'] = ''
                    else:
                        references[num] = li.text.strip()
                if page == pages:
                    break
                else:
                    time.sleep(5)
                    driver.find_element_by_link_text(str(page + 1)).click()
                    time.sleep(5)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                page = page + 1
        except:
            print('% ' + file[0] + ', ' + file[2] + ': ' + '中国重要报纸全文数据库的参考文献没加载完成！')
    return references


# 获取参考文献——中国博士学位论文全文数据库
def getCDFD(file, driver):
    references = {}
    box = driver.find_element_by_xpath('//*[@id="selectlist"]')
    box.send_keys('中国博士学位论文全文数据库')
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    count = numbers(soup.select('.count')[0].text.split('到')[1].split('条')[0].strip())
    pages = int(math.ceil(count / 10.0))
    if pages == 0:
        pass
    else:
        page = 1
        try:
            while True:
                for li in soup.select('.content li'):
                    num = li.text.split('.')[0].strip().split(']')[0].split('[')[1].strip()
                    references[num] = {}
                    if len(li.text.split('.')) == 3:
                        references[num]['author'] = li.text.split('.')[0].strip().split(']')[1].strip()
                        references[num]['title'] = li.text.split('.')[1].strip().replace('\u3000', '：')
                        references[num]['publisher'] = li.text.split('.')[-1].strip().split(' ')[0].strip()
                        references[num]['year'] = li.text.split('.')[-1].strip().split(' ')[1].strip()

                        try:
                            references[num]['filename'] = li.select('a')[0]['href'].split('filename=')[1].split('&')[
                                0].strip()
                        except:
                            references[num]['filename'] = ''
                    else:
                        references[num] = li.text.strip()
                if page == pages:
                    break
                else:
                    time.sleep(5)
                    driver.find_element_by_link_text(str(page + 1)).click()
                    time.sleep(5)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                page = page + 1
        except:
            # 需要手动检索。如果前方有相同title的e标签，则无需检索
            print('% ' + file[0] + ', ' + file[2] + ': ' + '中国博士学位论文全文数据库')
    return references


# 获取参考文献——《中国学术期刊（网络版）》
def getCJFQ(file, driver):
    references = {}
    box = driver.find_element_by_xpath('//*[@id="selectlist"]')
    box.send_keys('《中国学术期刊（网络版）》')
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    count = numbers(soup.select('.count')[0].text.split('到')[1].split('条')[0].strip())
    pages = int(math.ceil(count / 10.0))
    if pages == 0:
        pass
    else:
        page = 1
        try:
            while True:
                for li in soup.select('.content li'):
                    num = li.text.split('.')[0].strip().split(']')[0].split('[')[1].strip()
                    references[num] = {}
                    if len(li.text.split('.')) == 4:
                        references[num]['author'] = li.text.split('.')[0].strip().split(']')[1].strip()
                        references[num]['title'] = li.text.split('.')[1].strip()
                        references[num]['publisher'] = li.text.split('.')[2].strip()

                        year = li.text.split('.')[-1].split('(')[0].strip()
                        issue = li.text.split('.')[-1].split('(')[1].strip().split(')')[0].strip()
                        references[num]['issue'] = year + '年' + issue + '期'

                        try:
                            references[num]['filename'] = li.select('a')[0]['href'].split('filename=')[1].split('&')[
                                0].strip()
                        except:
                            references[num]['filename'] = ''
                    else:
                        references[num] = li.text.strip()
                if page == pages:
                    break
                else:
                    time.sleep(5)
                    driver.find_element_by_link_text(str(page + 1)).click()
                    time.sleep(5)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                page = page + 1
        except:
            # 需要手动检索。如果前方有相同title的e标签，则无需检索
            print('% ' + file[0] + ', ' + file[2] + ': ' + '《中国学术期刊（网络版）》的参考文献没加载完成！')
    return references


# 获取参考文献——中国优秀硕士学位论文全文数据库
def getCMFD(file, driver):
    references = {}
    box = driver.find_element_by_xpath('//*[@id="selectlist"]')
    box.send_keys('中国优秀硕士学位论文全文数据库')
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    count = numbers(soup.select('.count')[0].text.split('到')[1].split('条')[0].strip())
    pages = int(math.ceil(count / 10.0))
    if pages == 0:
        pass
    else:
        page = 1
        try:
            while True:
                for li in soup.select('.content li'):
                    num = li.text.split('.')[0].strip().split(']')[0].split('[')[1].strip()
                    references[num] = {}
                    if len(li.text.split('.')) == 3:
                        references[num]['author'] = li.text.split('.')[0].strip().split(']')[1].strip()
                        references[num]['title'] = li.text.split('.')[1].strip().replace('\u3000', '：')
                        references[num]['publisher'] = li.text.split('.')[-1].strip().split(' ')[0].strip()
                        references[num]['year'] = li.text.split('.')[-1].strip().split(' ')[1].strip()

                        try:
                            references[num]['filename'] = li.select('a')[0]['href'].split('filename=')[1].split('&')[
                                0].strip()
                        except:
                            references[num]['filename'] = ''
                    else:
                        references[num] = li.text.strip()
                if page == pages:
                    break
                else:
                    time.sleep(5)
                    driver.find_element_by_link_text(str(page + 1)).click()
                    time.sleep(5)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                page = page + 1
        except:
            # 需要手动检索。如果前方有相同title的e标签，则无需检索
            print('% ' + file[0] + ', ' + file[2] + ': ' + '中国优秀硕士学位论文全文数据库')
    return references


# 获取参考文献——中国重要会议论文全文数据库
def getCPFD(file, driver):
    references = {}
    box = driver.find_element_by_xpath('//*[@id="selectlist"]')
    box.send_keys('中国重要会议论文全文数据库')
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    count = numbers(soup.select('.count')[0].text.split('到')[1].split('条')[0].strip())
    pages = int(math.ceil(count / 10.0))
    if pages == 0:
        pass
    else:
        page = 1
        try:
            while True:
                for li in soup.select('.content li'):
                    num = li.text.split('.')[0].strip().split(']')[0].split('[')[1].strip()
                    references[num] = {}
                    if len(li.text.split('.')) == 4:
                        references[num]['author'] = li.text.split('.')[0].strip().split(']')[1].strip()
                        references[num]['title'] = li.text.split('.')[1].strip().replace('\u3000', '：')
                        references[num]['publisher'] = li.text.split('.')[2].strip()
                        references[num]['year'] = li.text.split('.')[-1].strip()

                        try:
                            references[num]['filename'] = li.select('a')[0]['href'].split('filename=')[1].split('&')[
                                0].strip()
                        except:
                            references[num]['filename'] = ''

                    else:
                        references[num] = li.text.strip()
                if page == pages:
                    break
                else:
                    time.sleep(5)
                    driver.find_element_by_link_text(str(page + 1)).click()
                    time.sleep(5)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                page = page + 1
        except:
            print('% ' + file[0] + ', ' + file[2] + ': ' + '中国重要会议论文全文数据库！')
    return references


# 获取参考文献——外文题录数据库
def getCRLDENG(file, driver):
    references = {}
    box = driver.find_element_by_xpath('//*[@id="selectlist"]')
    box.send_keys('外文题录数据库')
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    count = numbers(soup.select('.count')[0].text.split('到')[1].split('条')[0].strip())
    pages = int(math.ceil(count / 10.0))
    if pages == 0:
        pass
    else:
        page = 1
        try:
            while True:
                for li in soup.select('.content li'):
                    num = li.text.split('.')[0].strip().split(']')[0].split('[')[1].strip()
                    references[num] = {}
                    if len(li.text.split('.')) == 4:
                        references[num]['author'] = li.text.split('.')[0].strip().split(']')[1].strip()
                        references[num]['title'] = li.text.split('.')[1].strip()
                        references[num]['publisher'] = li.text.split('.')[2].strip()
                        references[num]['year'] = li.text.split('.')[3].strip()

                    else:
                        references[num] = li.text.strip()
                if page == pages:
                    break
                else:
                    time.sleep(5)
                    driver.find_element_by_link_text(str(page + 1)).click()
                    time.sleep(5)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                page = page + 1
        except:
            print('% ' + file[0] + ', ' + file[2] + ': ' + '外文题录数据库的参考文献没加载完成！')
    return references


# 获取参考文献——中国年鉴网络出版总库
def getCYFD(file, driver):
    references = {}
    box = driver.find_element_by_xpath('//*[@id="selectlist"]')
    box.send_keys('中国年鉴网络出版总库')
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    count = numbers(soup.select('.count')[0].text.split('到')[1].split('条')[0].strip())
    pages = int(math.ceil(count / 10.0))
    if pages == 0:
        pass
    else:
        page = 1
        try:
            while True:
                for li in soup.select('.content li'):
                    num = li.text.split('.')[0].strip().split(']')[0].split('[')[1].strip()
                    references[num] = {}
                    if len(li.text.split('.')) == 4:
                        references[num]['author'] = li.text.split('.')[0].strip().split(']')[1].strip()
                        references[num]['title'] = li.text.split('.')[1].strip().replace('\u3000', '：')
                        references[num]['publisher'] = li.text.split('.')[2].strip()
                        references[num]['year'] = li.text.split('.')[-1].strip()

                        try:
                            references[num]['filename'] = li.select('a')[0]['href'].split('filename=')[1].split('&')[
                                0].strip()
                        except:
                            references[num]['filename'] = ''

                    else:
                        references[num] = li.text.strip()
                if page == pages:
                    break
                else:
                    time.sleep(5)
                    driver.find_element_by_link_text(str(page + 1)).click()
                    time.sleep(5)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                page = page + 1
        except:
            print('% ' + file[0] + ', ' + file[2] + ': ' + '中国年鉴网络出版总库！')
    return references


# 获取参考文献——国际会议论文全文数据库
def getIPFD(file, driver):
    references = {}
    box = driver.find_element_by_xpath('//*[@id="selectlist"]')
    box.send_keys('国际会议论文全文数据库')
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    count = numbers(soup.select('.count')[0].text.split('到')[1].split('条')[0].strip())
    pages = int(math.ceil(count / 10.0))
    if pages == 0:
        pass
    else:
        page = 1
        try:
            while True:
                for li in soup.select('.content li'):
                    num = li.text.split('.')[0].strip().split(']')[0].split('[')[1].strip()
                    references[num] = {}
                    if len(li.text.split('.')) == 4:
                        references[num]['author'] = li.text.split('.')[0].strip().split(']')[1].strip()
                        references[num]['title'] = li.text.split('.')[1].strip().replace('\u3000', '：')
                        references[num]['publisher'] = li.text.split('.')[2].strip()
                        references[num]['year'] = li.text.split('.')[-1].strip()

                        try:
                            references[num]['filename'] = li.select('a')[0]['href'].split('filename=')[1].split('&')[
                                0].strip()
                        except:
                            references[num]['filename'] = ''

                    else:
                        references[num] = li.text.strip()
                if page == pages:
                    break
                else:
                    time.sleep(5)
                    driver.find_element_by_link_text(str(page + 1)).click()
                    time.sleep(5)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                page = page + 1
        except:
            print('% ' + file[0] + ', ' + file[2] + ': ' + '国际会议论文全文数据库！')
    return references


# 获取参考文献——中国专利数据库
def getSCPD(file, driver):
    references = {}
    box = driver.find_element_by_xpath('//*[@id="selectlist"]')
    box.send_keys('中国专利数据库')
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    count = numbers(soup.select('.count')[0].text.split('到')[1].split('条')[0].strip())
    pages = int(math.ceil(count / 10.0))
    if pages == 0:
        pass
    else:
        page = 1
        try:
            while True:
                for li in soup.select('.content li'):
                    num = li.text.split('.')[0].strip().split(']')[0].split('[')[1].strip()
                    references[num] = {}
                    if len(li.text.split('.')) == 3:
                        references[num]['author'] = li.text.split('.')[0].strip().split(']')[1].strip()
                        references[num]['title'] = li.text.split('.')[1].strip().replace('\u3000', '：')
                        references[num]['code'] = li.text.split('.')[-1].strip().split('(')[0].strip()

                        try:
                            references[num]['filename'] = li.select('a')[0]['href'].split('filename=')[1].split('&')[0].strip()
                        except:
                            references[num]['filename'] = ''
                    else:
                        # 没有author, title, publisher, issue字段
                        references[num] = li.text.strip()

                if page == pages:
                    break
                else:
                    time.sleep(5)
                    driver.find_element_by_link_text(str(page + 1)).click()
                    time.sleep(5)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                page = page + 1
        except:
            print('% ' + file[0] + ', ' + file[2] + ': ' + '中国专利数据库！')
    return references


# 获取参考文献——中国标准数据库
def getSCSD(file, driver):
    references = {}
    box = driver.find_element_by_xpath('//*[@id="selectlist"]')
    box.send_keys('中国标准数据库')
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    count = numbers(soup.select('.count')[0].text.split('到')[1].split('条')[0].strip())
    pages = int(math.ceil(count / 10.0))
    if pages == 0:
        pass
    else:
        page = 1
        try:
            while True:
                for li in soup.select('.content li'):
                    num = li.text.split('.')[0].strip().split(']')[0].split('[')[1].strip()
                    references[num] = {}
                    if len(li.text.split('.')) == 3:
                        references[num]['author'] = li.text.split('.')[0].strip().split(']')[1].strip()
                        references[num]['title'] = li.text.split('.')[1].strip().replace('\u3000', '：')
                        references[num]['year'] = li.text.split('.')[-1].strip().split('(')[0].strip()

                        try:
                            references[num]['filename'] = li.select('a')[0]['href'].split('filename=')[1].split('&')[
                                0].strip()
                        except:
                            references[num]['filename'] = ''
                    else:
                        # 没有author, title, publisher, issue字段
                        references[num] = li.text.strip()

                if page == pages:
                    break
                else:
                    time.sleep(5)
                    driver.find_element_by_link_text(str(page + 1)).click()
                    time.sleep(5)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                page = page + 1
        except:
            print('% ' + file[0] + ', ' + file[2] + ': ' + '中国标准数据库！')
    return references


# 获取参考文献——国际期刊数据库
def getSSJD(file, driver):
    references = {}
    box = driver.find_element_by_xpath('//*[@id="selectlist"]')
    box.send_keys('国际期刊数据库')
    time.sleep(3)  # 转换数据库 time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    count = numbers(soup.select('.count')[0].text.split('到')[1].split('条')[0].strip())
    pages = int(math.ceil(count / 10.0))
    if pages == 0:
        pass
    else:
        page = 1
        try:
            while True:
                for li in soup.select('.content li'):
                    num = li.text.split('.')[0].strip().split(']')[0].split('[')[1].strip()
                    references[num] = {}
                    if len(li.text.split('.')) == 4:
                        references[num]['author'] = li.text.split('.')[0].strip().split(']')[1].strip()
                        references[num]['title'] = li.text.split('.')[1].strip()
                        references[num]['publisher'] = li.text.split('.')[2].strip()

                        year = li.text.split('.')[-1].split('(')[0].strip()
                        issue = li.text.split('.')[-1].split('(')[1].strip().split(')')[0].strip()
                        references[num]['issue'] = year + '年' + issue + '期'

                        try:
                            references[num]['filename'] = li.select('a')[0]['href'].split('filename=')[1].split('&')[
                                0].strip()
                        except:
                            references[num]['filename'] = ''
                    else:
                        # 没有author, title, publisher, issue字段
                        references[num] = li.text.strip()

                if page == pages:
                    break
                else:
                    time.sleep(5)
                    driver.find_element_by_link_text(str(page + 1)).click()
                    time.sleep(5)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                page = page + 1
        except:
            print('% ' + file[0] + ', ' + file[2] + ': ' + '国际期刊数据库的参考文献没加载完成！')
    return references


# 将获得的文献信息放到字典中保存
def get_article_info(file, driver):
    article = {}
    has_ref = {}
    references = {}
    article['title'] = file[0]
    article['filename'] = file[1]
    article['issue'] = file[2]
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 获取文献的描述信息
    article['file_info'] = get_file_info(file, soup)

    # 获取参考文献
    driver.switch_to.frame('frame1')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    if '【参考文献】' in soup.select('html')[0].text:
        try:
            time.sleep(2)
            references['CBBD'] = getCBBD(file, driver)
        except:
            references['CBBD'] = {}
            print('# ' + file[0] + ': 获取中国图书全文数据库出错！')

        try:
            time.sleep(2)
            references['CCND'] = getCCND(file, driver)
        except:
            references['CCND'] = {}
            print('# ' + file[0] + ': 获取中国重要报纸全文数据库出错！')

        try:
            time.sleep(2)
            references['CDFD'] = getCDFD(file, driver)
        except:
            references['CDFD'] = {}
            print('# ' + file[0] + ': 中国博士学位论文全文数据库出错！')

        try:
            time.sleep(2)
            references['CJFQ'] = getCJFQ(file, driver)
        except:
            references['CJFQ'] = {}
            print('# ' + file[0] + ': 获取《中国学术期刊（网络版）》出错！')

        try:
            time.sleep(2)
            references['CMFD'] = getCMFD(file, driver)
        except:
            references['CMFD'] = {}
            print('# ' + file[0] + ': 中国优秀硕士学位论文全文数据库出错！')

        try:
            time.sleep(2)
            references['CPFD'] = getCPFD(file, driver)
        except:
            references['CPFD'] = {}
            print('# ' + file[0] + ': 中国重要会议论文全文数据库出错！')

        try:
            time.sleep(2)
            references['CRLDENG'] = getCRLDENG(file, driver)
        except:
            references['CRLDENG'] = {}
            print('# ' + file[0] + ': 获取外文题录数据库出错！')

        try:
            time.sleep(2)
            references['CYFD'] = getCYFD(file, driver)
        except:
            references['CYFD'] = {}
            print('# ' + file[0] + ': 中国年鉴网络出版总库出错！')

        try:
            time.sleep(2)
            references['IPFD'] = getIPFD(file, driver)
        except:
            references['IPFD'] = {}
            print('# ' + file[0] + ': 国际会议论文全文数据库出错！')

        try:
            time.sleep(2)
            references['SCPD'] = getSCPD(file, driver)
        except:
            references['SCPD'] = {}
            print('# ' + file[0] + ': 中国专利数据库出错！')

        try:
            time.sleep(2)
            references['SCSD'] = getSCSD(file, driver)
        except:
            references['SCSD'] = {}
            print('# ' + file[0] + ': 中国标准数据库出错！')

        try:
            time.sleep(2)
            references['SSJD'] = getSSJD(file, driver)
        except:
            references['SSJD'] = {}
            print('# ' + file[0] + ': 获取国际期刊数据库出错！')

    article['references'] = references
    article['has_ref'] = has_ref
    time.sleep(5)
    return article


def crawling(journal_name, articles):
    journal = {}
    num = 0
    not_finished = []

    print('开始爬取《' + journal_name + '》：')
    for article in articles:

        file = search_file(journal_name, article)
        if len(file) == 0:
            not_finished.append(article)
            time.sleep(3)
        else:
            num += 1
            journal[num] = file
            time.sleep(3)
    print('《' + journal_name + '》已经爬取完成！')

    return journal, not_finished


#journalNames = ['法学杂志',
#    '比较法研究', '当代法学', '德国研究', '东方法学', '法律科学',
#    '法商研究', '法学', '法学家', '法学论坛', '法学评论', '法学研究',
#    '法学杂志', '法制与社会发展', '行政法学研究', '华东政法大学学报',
#    '环球法律评论', '清华法学', '现代法学', '政法论丛', '政法论坛',
#    '政治与法律','中国法学', '中国刑事法杂志', '中外法学', '中国社会科学']"

def search_file(journal_name, article):
    url = 'http://search.cnki.net/AdvanceSearch.aspx'
    options = webdriver.ChromeOptions()
    options.add_argument('lang=zh_CN.UTF-8')  # 中文字符打开
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url)
    time.sleep(3)

    title = article[0]
    real_title = article[2]
    filename = article[1]

    info = {}

    try:  # 尝试打开网页
        # 填入题目
        title_box = driver.find_element_by_xpath('//*[@id="txttitle"]')
        title_box.clear()
        title_box.send_keys(title)
        # 填入期刊
        jo_box = driver.find_element_by_xpath('//*[@id="txtarticlefrom"]')
        jo_box.clear()
        jo_box.send_keys(journal_name)
        # 点击搜索按钮
        time.sleep(3)
        button = driver.find_element_by_xpath('//*[@id="btnSearch"]')
        button.click()
    except:
        driver.quit()
        time.sleep(3)
        return info

    # 获得file信息
    if '.' in filename:
        year = '199' + filename[4:5]
        issue = filename[5:6]
        file = (real_title, filename, year + '年' + issue + '期')
    else:
        year = filename[4:8]
        issue = filename[8:10]
        file = (real_title, filename, year + '年' + issue + '期')

    try:
        elements = driver.find_elements_by_partial_link_text(title)
        for element in elements:
            time.sleep(3)
            element.click()
            driver.switch_to.window(driver.window_handles[1])
            # 匹配filename获得爬取唯一的文献
            if filename.upper() == driver.current_url.upper().split('FILENAME=')[1].split('&')[0].strip():
                time.sleep(2)
                info = get_article_info(file, driver)
                time.sleep(3)
            else:
                time.sleep(3)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

        # 如果file为{}则当前页没有该文献
        time.sleep(3)
        driver.quit()
        return info
    except:
        time.sleep(3)
        driver.quit()
        return info

