# Nike Crawling Service
나이키 사이트에서 SNKR 응모를 하는 상품을 가져와서 email로 전송하는 서비스

# environment variables
Set `.env` file
```
EMAIL_ID={Your Email}
EMAIL_PASSWORD={Your Email password}
EMAIL_USERNAME={Email send user name}
ADMIN_ID={Admin Email}
```

# Using JOB
```commandline
python3 manage.py start --recipients {email1,email2}
```

# Using Server
Run django server
```commandline
python manage.py runserver
```

# EndPoints
| Method | Endpoint                         |   Param   | Description |
|:------:|----------------------------------|:---------:|:-----------:|
|  Get   | http://localhost:8000            |  Welcome  |             |
|  Get   | http://localhost:8000/job        | Call List |             |

# Example
- http://localhost:8000/job/?recipients={YourEmail}
- http://localhost:8000/job/?recipients={YourEmail}&date=2023-05-21