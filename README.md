
<h1 align="center">Blogs API</h1>


<p align="center">
   <img src="https://img.shields.io/badge/FastAPI%20v.-0.95.1-brightgreen" alt="FastAPI version">
   <img src="https://img.shields.io/badge/Python-3.11-green" alt="Python version">
   <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License">
</p>


![FastAPI_logo](https://upload.wikimedia.org/wikiversity/en/8/8c/FastAPI_logo.png)


FastAPI REST based project. The project allows you to: 
- Create your own User account by registration and login, which are constructed using OAuth2 security protocol and JWT-Token, 
- Work with efficient blogs API, thankfully to Redis caching,
- Work with background tasks like sending email to the user's email address (which he put in registration form) using Celery + Flower.


## Local launch

### Environment Variables

To run this project, you will need to add the following environment variables
to your .env file:

`SMTP_PASSWORD` - apps password (I use Google)

`SMTP_USER` - app email (I use Gmail)

`REDIS_HOST` - your redis server host (default is localhost)

`REDIS_PORT` - your redis server port (default is 6379)

`SECRET_JWT_KEY` - your very secret JWT key



### Launch the project

1. Install packets from the requirements.txt

```bash
  pip install -r requirements.txt
```
2. Launch the app on ASGI uvicorn web server:
```bash
  --uvicorn app.main:app --reload
```
    
## Docker container launch

### Environment Variables

To run this project in docker container, you will need to create .env-dckr file
and add the following environment variables to your file:

`SMTP_PASSWORD` - apps password (I use Google)

`SMTP_USER` - app email (I use Gmail)

`REDIS_HOST` - your redis server host (has to be "redis")

`REDIS_PORT` - your redis server port (has to be 6379)

`SECRET_JWT_KEY` - your very secret JWT key



### Build Docker container

1. Build your FastAPI app image

```bash
  docker build . -t fastapi_app:latest   
```
2. Build or rebuild services
```bash
  docker compose build
```
3. Create and start container
```bash
  docker compose up
```


## API Reference

#### Registration

```http
  POST /register

  {
    "username": "string",
    "email": "string",
    "password": "string",
    "repeated_password": "string"
  }
```
#### Login

```http
  POST /login

  {
    "username": "string",
    "password": "string"
  }
```

#### Get all blogs

```http
  GET /api/blog
    -h "Authorization": "Bearer ${your access_token}"
  
```


#### Get blog by id

```http
  GET /api/blog/${id}
    -h "Authorization": "Bearer ${your access_token}"
  
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `int` | **Required**. Id of item to fetch |

#### Create a new blog

```http
  POST /api/blog/
    -h "Authorization": "Bearer ${your access_token}"

  {
    "title": "string",
    "body": "string"
  }
```

#### Update the blog (Full)

```http
  PUT /api/blog/${id}
    -h "Authorization": "Bearer ${your access_token}"

  {
    "title": "string",  # optional, default = ""
    "body": "string"  # optional, default = ""
  }
```

#### Update the blog (Partial)

```http
  PATCH /api/blog/${id}
    -h "Authorization": "Bearer ${your access_token}"

  {
    "title": "string",  # optional
    "body": "string"  # optional
  }
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `int` | **Required**. Id of item to update |

#### Delete the blog

```http
  DELETE /api/blog/${id}
    -h "Authorization": "Bearer ${your access_token}"
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `int` | **Required**. Id of item to fetch |

#### Create a User object

```http
  POST /api/user/

  {
    "username": "string",
    "email": "string",
    "password": "string"
  }
```

#### Get user by id

```http
  GET /api/user/${id}
  
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `int` | **Required**. Id of item to fetch |

#### Get greeting email!!

```http
  GET /api/task/greet/
    -h "Authorization": "Bearer ${your access_token}"
  
```

## Developers

- [Illia Borshch](https://github.com/ilborsch)

## License

The Project To Do Application from Illia Borshch is distributed under the [MIT](https://choosealicense.com/licenses/mit/) license.
