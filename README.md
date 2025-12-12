# django-asct
암호 : test4321
export PS1="\\W \\$ "
# wsl(linux, 우분투)에서 django 설치하고 실행하기
## 방화벽 연결(db)
## apt install ufw
## sudo ufw allow 5432/tcp
# venv 설정 : apt install python3-venv
 source venv/bin/activate
``` 
pip install 
pip install Pillow
pip install crispy-bootstrap5
pip install psycopg2 (컴파일 라이블러리 설치하고 ...)
```
## db 설정
### postgresql 설치하고, pg_hba.conf 설정하고, 원격접속 password 설정
```
sudo -u postgres psql
ALTER USER postgres WITH PASSWORD '새_비밀번호';
sudo nano /etc/postgresql/16/main/pg_hba.conf  # <version>을 실제 버전에 맞게 변경

TYPE  DATABASE  USER    ADDRESS         METHOD
host    all       all     127.0.0.1/32    md5
아래 ip도 추가
host    all             all             172.31.16.1/32            md5

sudo vi /etc/postgresql/16/main/postgresql.conf
password_encryption = md5
listen_addresses = '*'          # what IP address(es) to listen on;

sudo systemctl restart postgresql

- 연결 시험
psql -h localhost -U postgres -W
python manage.py migrate
```

import json
with open('blog/post_data.json', 'r') as f:
  posts_json = json.load(f)
for p in posts_json:
  post = Post(title=p['title'], content=p['content'], author_id = p['user_id'])
  post.save()
