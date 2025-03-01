import requests
from prettytable import PrettyTable

 
class Jdcomment_spider(object):
 
    # 请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
 
    def __init__(self, file_name='jd_commet'):
        
         

        # 实例化类的时候运行初始化函数
        # 打开文件
        self.fp = open(f'./{file_name}.txt', 'w', encoding='utf-8')
        self.all_comments = []  # 用于存储所有评论数据
        print(f'正在打开文件{file_name}.txt文件!')
 
 
    def parse_one_page(self, url):
        # 指定url
        url = 'https://club.jd.com/comment/productPageComments.action?productId=10079932124329&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&rid=0&fold=1'
 
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }
 
        # 发起请求
        response = requests.get(url, headers=self.headers)
        # 获取响应
        js_data = response.json()
 
        # 提取评论列表
        comments_list = js_data['comments']
 
        for comment in comments_list:
            # 商品id
            goods_id = comment.get('id')
            # 用户昵称
            nickname = comment.get('nickname')
            # 评分
            score = comment.get('score')
            # 商品尺寸
            productSize = comment.get('productSize')
            # 商品颜色
            productColor = comment.get('productColor')
            # 评论时间
            creationTime = comment.get('creationTime')
            # 评论内容
            content = comment.get('content')
            content = content.replace('\n', ' ') #处理换行符
 
           # 暂时不打印，先将数据存储起来
            self.all_comments.append([
                goods_id,
                nickname,
                score,
                productSize,
                productColor,
                creationTime,
                content
            ])
 
        
 
 
    def parse_max_page(self):
        table = PrettyTable()
        table.field_names = ["商品id", "用户昵称", "评分", "商品尺寸", "商品颜色", "评论时间", "评论内容"]
        for page_num in range(500):  # 抓包获得最大页数
            # 指定通用的url模板
            new_url = f'https://club.jd.com/comment/productPageComments.action?productId=10079932124329&score=0&sortType=5&page={page_num}&pageSize=10&isShadowSku=0&rid=0&fold=1'

            print(f'正在获取第{page_num+1}页')

            # 调用函数解析页面
            self.parse_one_page(new_url)

        # 数据收集完成后统一打印
        for row in self.all_comments:
            table.add_row(row)

        # 打印表格
        print(table)

        # 保存到文件
        with open('output.txt', 'w', encoding='utf-8') as fp:
            fp.write(table.get_string())

 
 
    def close_files(self):
        self.fp.close()
        print('爬虫结束，关闭文件！')
 
 
if __name__ == '__main__':
    # 实例对象
    jd_spider = Jdcomment_spider()
    # 开始爬虫
    jd_spider.parse_max_page()
    # 关闭文件
    jd_spider.close_files()