# -*- encoding: utf-8 -*-
from fake_useragent import UserAgent
import time
import requests
import random
import json
import csv
import io


# 保存评论数据
def commentSave(list_comment):
    '''
    list_comment: 二维list,包含了多条用户评论信息
    '''
    file = io.open('./JDComment_data.csv', 'w', encoding="utf-8", newline='')
    writer = csv.writer(file)
    writer.writerow(['用户ID', '评论内容', '购买时间', '点赞数', '回复数', '得分', '评价时间', '手机型号'])
    for i in range(len(list_comment)):
        writer.writerow(list_comment[i])
    file.close()
    print('存入成功')


def getCommentData(format_url, i, maxPage):
    '''
    format_url: 格式化的字符串架子，在循环中给它添上参数
    proc: 商品的productID，标识唯一的商品号
    i: 商品的排序方式，例如全部商品、晒图、追评、好评等
    maxPage: 商品的评论最大页数
    '''
    sig_comment = []
    global list_comment
    cur_page = 0
    # 异常循环三次退出循环
    sum = maxPage - 3
    while cur_page < maxPage:
        if sum == maxPage:
            break
        cur_page += 1
        url = format_url.format(i, cur_page)  # 给字符串添上参数
        try:
            response = requests.get(url=url, headers=headers)
            time.sleep(random.uniform(2, 3))
            jsonData = response.text
            # 返回 { 下标索引
            startLoc = jsonData.find('{')
            # print(jsonData[::-1])//字符串逆序
            jsonData = jsonData[startLoc:-2]
            # 转化类型
            jsonData = json.loads(jsonData)
            pageLen = len(jsonData['comments'])
            print("当前第%s页" % cur_page)
            for j in range(0, pageLen):
                userId = jsonData['comments'][j]['id']  # 用户ID
                content = jsonData['comments'][j]['content']  # 评论内容
                boughtTime = jsonData['comments'][j]['referenceTime']  # 购买时间
                voteCount = jsonData['comments'][j]['usefulVoteCount']  # 点赞数
                replyCount = jsonData['comments'][j]['replyCount']  # 回复数目
                starStep = jsonData['comments'][j]['score']  # 得分
                creationTime = jsonData['comments'][j]['creationTime']  # 评价时间
                referenceName = jsonData['comments'][j]['referenceName']  # 手机型号
                sig_comment.append(userId)  # 每一行数据
                sig_comment.append(content)
                sig_comment.append(boughtTime)
                sig_comment.append(voteCount)
                sig_comment.append(replyCount)
                sig_comment.append(starStep)
                sig_comment.append(creationTime)
                sig_comment.append(referenceName)
                list_comment.append(sig_comment)
                sig_comment = []
        except:
            time.sleep(8)
            cur_page -= 1
            sum += 1
            print('网络故障或者是网页出现了问题，八秒后重新连接')


if __name__ == "__main__":
    global list_comment
    format_url = 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=100004770263&score={}&sortType=5&page={}&pageSize=10&isShadowSku=0&fold=1'
    # 设置访问请求头
    headers = {
        'Accept': '*/*',
        "User-Agent": UserAgent().random,
        'Cookie':'__jdu=16044877251811259445840; shshshfpa=f685d29c-db54-0fbf-6432-fa5e1a9c93fc-1604487726; shshshfpb=f3M2cAIGqVpasNy9t4ZoOhQ%3D%3D; jwotest_product=99; areaId=1; PCSYCityID=CN_110000_110100_110106; ipLoc-djd=1-72-55653-0; unpl=V2_ZzNtbRFRRxwgCk9VckpeBmJTQllLUBRCdwkSVSkdVQxvARBdclRCFnQURldnGVQUZwsZWENcQBFFCEdkeB5fA2AFEFlBZxBFLV0CFi9JH1c%2bbRJcRV5CE3cPRVB7Gmw1ZAMiXUNnQxJ0DUNdfR9fAWcKEl1BU0sQcAxPUXopbAJXMyJdSlBLHXI4R2R6KR5ROwoRX0BRDhVyCUNRch9aBmMDG11CVEcdcA1CXX4YbARXAA%3d%3d; __jdv=76161171|baidu-search|t_262767352_baidusearch|cpc|106807362512_0_b758d3808b324aa586ff30e0c5889331|1608378026217; __jda=122270672.16044877251811259445840.1604487725.1608363960.1608378026.7; __jdc=122270672; shshshfp=8407fffe2c2509197abee21f5f3d0c4c; 3AB9D23F7A4B3C9B=KRREJXKBI4XMNSAAWVQ5FF75HVXAFCNIN6XKBTGIHKWFY4EUV2RT5JRTNELJD2QEGWQT5GBXF5M45R5W3MVYEOC5YE; JSESSIONID=D872A776B48D02C380DA4D216F129513.s1',
        'Referer': "https://item.jd.com/100000177760.html#comment"
    }
    # 手机四种颜色对应的产品id参数
    # productid = ['productId=100006795590','136061&productId=5089275','22778&productId=5475612','7021&productId=6784504']
    list_comment = [[]]
    sig_comment = []
    # for proc in productid:#遍历产品颜色
    # 发现不同评价的score不同 且不超过7 且没有6
    i = -1
    while i < 7:  # 遍历排序方式
        i += 1
        if (i == 6):
            continue
        # 先访问第0页获取最大页数，再进行循环遍历
        url = format_url.format(i, 0)
        print(url)

        try:
            jsonData = requests.get(url=url, headers=headers).text
            print(jsonData)
            # 获取{所在下标索引
            startLoc = jsonData.find('{')
            # 通过切片取出字典内用
            jsonData = jsonData[startLoc:-2]
            # 转换格式
            jsonData = json.loads(jsonData)
            print(jsonData['maxPage'])
            print("最大页数%s" % jsonData['maxPage'])
            getCommentData(format_url, i, jsonData['maxPage'])
        except Exception as e:
            # 减1 重新做循环
            i -= 1
            print("the error is ", e)
            # print("wating---")
            time.sleep(5)
            # commentSave(list_comment)
    print("爬取结束，开始存储-------")
    commentSave(list_comment)
