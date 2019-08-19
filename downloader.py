import requests
import csv
import re

'''
Получение access_token
params = {'client_id': '7103079',
          'client_secret': 'mROyU8bwp0vPVjUavkl8',
          'redirect_url': 'http://localhost/callback',
          'code': 'a5f8acc02a45511590'}

r = requests.request('get', 'https://oauth.vk.com/access_token', params=params)
'''
access_token = '1439b4a59fb6d4347c9733f2114447e21ad68ba8f36cb7ee85b8a5e6322c202c3639aea3a2fa4ecd6b6f8'


def deemojify(inputstring):
    emoji_pattern = re.compile("["
                              u"\U0001F600-\U0001F64F"  # emoticons
                              u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                              u"\U0001F680-\U0001F6FF"  # transport & map symbols
                              u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                              "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', inputstring)


def get_posts_id(public_id):
    post_id_params = {'owner_id': public_id,
                      'count': 10,
                      'access_token': access_token,
                      'v': '5.101.'
                      }

    r = requests.request('get', 'https://api.vk.com/method/wall.get', params=post_id_params)
    posts_id = [r.json()['response']['items'][i]['id'] for i in range(len(r.json()['response']['items']))]

    return posts_id


def get_comments(public_id, post_id):
    comment_params = {'owner_id': public_id,
                      'post_id': post_id,
                      'count': 10,
                      'extended': 1,
                      'access_token': access_token,
                      'v': '5.101.'
                      }
    r = requests.request('get', 'https://api.vk.com/method/wall.getComments', params=comment_params)
    comments = []
    for i in range(len(r.json()['response']['items'])):
        if 'text' in r.json()['response']['items'][i].keys():
            comments.append(deemojify(r.json()['response']['items'][i]['text']))

    return comments


def get_public_id(public_name):
    public_params = {
        'group_id': public_name,
        'access_token': access_token,
        'v': '5.101.'
    }
    r = requests.request('get', 'https://api.vk.com/method/groups.getById', params=public_params)
    return r.json()['response'][0]['id']


def save_comment(public_name):
    #out = open(f'{public_name}.txt', 'a', encoding='UTF-8')

    public_id = -get_public_id(public_name)
    posts_id = get_posts_id(public_id)
    public_comments = []
    for post_id in posts_id:
        public_comments += get_comments(public_id, post_id)

    '''
    for comment in public_comments:
        out.write(comment + '\n')
    out.close()
    '''
    return public_comments

# 4ch : -45745333  medusa: -76982440  лентач: -29534144


'''groups_name = ['oldlentach']

for group_name in groups_name:
    save_comment(group_name)

print('готово')
'''