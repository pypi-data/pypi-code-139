import requests
def tik_info(user):
    cookies = {
    'csrftoken': 'BtyDLdzzRToomfuTbGqX65vR91eJMaIQlZe2e9r5uPAJnS44djZ7YamKLaQNOSdj',
}
#By moelshafey
    data = {
    'sc': 'tiktok',
    'link': user,
    'uid': '00a176bec7044a4da94bf852696df6ed',
    'csrfmiddlewaretoken': 'biGNCtprSzu6jy2eK5NNfA1iixx65DOLVOmc5phXvvGrkbCpMImX7FSbUG9a7lje',
}

    LO= requests.post('https://instamer.com/en/profile/step_profile_data', cookies=cookies,data=data).json()["profile"]
    User=LO['username']
    followers=LO["followers"]
    praivate=LO['is_private']
    phot=LO["pic_original"]
    photo=requests.get(f"http://tinyurl.com/api-create.php?url={phot}").text
    posts=LO['show_n_posts']
    prog='@ALAA7X  - @Elshafey_Team'
    return {'user': User,'folws':followers,'private':praivate,'photo': photo,'posts': posts,'program':prog}
