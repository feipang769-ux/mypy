import requests,re,time

def run():
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36'
        }

    url = 'https://movie.douban.com/top250'

    for page in range(0,250,25):
        params = {'start':page,'filter':None}
        all_page = requests.get(url,params=params,headers=headers)

        try:
            all_page.raise_for_status()
            print('请求成功,正在执行解析')
        except Exception as e:
            print('请求失败了!')
            continue

        movie_name = re.findall(r'<span class="title">([^/]*)</span>',all_page.text)
        grade = re.findall(r'<span class="rating_num" property="v:average">(.*)</span>',all_page.text)
        time.sleep(2)

        

        for (index,title),grades in zip(enumerate(movie_name,start=page + 1),grade):
            print(f'{index}.{title} 评分:{grades}')


if __name__ == '__main__':
    run()