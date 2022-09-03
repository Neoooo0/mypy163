
import logging
import os
import json
import requests
from requests import get, post

api = os.environ["API"]
paassword = os.environ["PASSWORD"]
phone = os.environ["PHONE"]  ###填手机号
countrycode = 86


class music163():
    def __init__(self, account, password, api, countrycode):
        self.password = password
        self.account = account
        self.api = api
        self.countrycode = countrycode
        self.session = requests.Session()
        self.headers = {
            "Host": "adventurous-beneficial-centaur.glitch.me",  ###如果修改api记得改头文件
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": '1',

        }

    logFile = open("run.log", encoding="utf-8", mode="a")
    logging.basicConfig(stream=logFile, format="%(asctime)s %(levelname)s:%(message)s", datefmt="%Y-%m-%d %H:%M:%S",level=logging.INFO)

    def login(self):
        data = {
            "phone": self.account,
            "md5_password": self.password,
            "countrycode": self.countrycode,  ##国家码  86为中国
        }
        url = self.api + "/login/cellphone"
        print('下面是登录的账户名称,如果出错则失败')

        try:
            a = json.loads(self.session.get(url, params=data, headers=self.headers).text)['profile']['nickname']
            logging.info('用户详情:' + str(a))
        except:
            return "login错误"

    def task(self):

        url = self.api + "/personalized?limit=300"
        ##获取推荐歌单列表

        res = json.loads(self.session.get(url).text)
        albumlist = res['result']
        count = 1

        for album in albumlist:  ##对获取的推荐歌单列表遍历每一个歌单
            id = album['id']
            url = self.api + "/playlist/track/all"
            data = {
                "id": id,
                "limit": '300'
            }
            musiclist = json.loads(self.session.get(url, params=data).text)['songs']
            ##得到某个歌单包含的音乐列表
            for music in musiclist:  ##刷歌
                songid = music['id']
                name = music['name']
                data = {
                    "id": songid,
                    "sourceid": id
                }
                url = self.api + "/scrobble"
                self.session.get(url, params=data)
                print('第' + str(count) + '首歌曲，名字:' + name + '已听')
                count = count + 1
                if (count == 320):
                    logging.info('刷到320首歌退出')
                    return count ##刷到320首歌退出

    def main(self):
            self.login()
            self.task()

    def get_access_token(self):
            # appId
            app_id = os.environ["APP_ID"]
            #config["app_id"]
            # appSecret
            app_secret = os.environ["APP_SECRET"]
            post_url = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}"
                        .format(app_id, app_secret))
            try:
                access_token = get(post_url).json()['access_token']
            except KeyError:
                print("获取access_token失败，请检查app_id和app_secret是否正确")
                os.system("pause")
                sys.exit(1)
            return access_token



    def send_message(self):

            accessToken = self.get_access_token()
            result = self.task()

            print(result)

            url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(accessToken)

            data = {
                "touser": os.environ["TO_USER"],
                "template_id": os.environ["TEMPLATE_ID"],
                "url": "https://github.com/Neoooo0/mypy163/actions/workflows/daka.yml",
                "topcolor": "#FF0000",
                "data": {

                    "to_user": {
                        "value": result,
                        "color": '#d72e2f'
                    }

                }
            }
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
            }
            response = post(url, headers=headers, json=data).json()
            if response["errcode"] == 40037:
                print("推送消息失败，请检查模板id是否正确")
            elif response["errcode"] == 40036:
                print("推送消息失败，请检查模板id是否为空")
            elif response["errcode"] == 40003:
                print("推送消息失败，请检查微信号是否正确")
            elif response["errcode"] == 0:
                print("推送消息成功")
            else:
                print(response)

def main(event, content):
    music163(phone, paassword, api, countrycode).main()


if __name__ == '__main__':
    music163(phone, paassword, api, countrycode).main()
    music163(phone, paassword, api, countrycode).send_message()
