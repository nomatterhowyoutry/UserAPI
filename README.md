# UserAPI
Simple Rest API that provides CRUD for Posts and Users

**Get Post List and Create new one:**

  ~/api/posts/
  
  Expected Input:
  {
    - title
    - content
  }
  
  Expected Output:
  {
    -url,
    -id,
    -title,
    -user,
    -content,
    -likes,
    -dislikes,
    -rating,
    -timestamp,
  }
  

**Retrieve, Update, Delete Post:**

  ~/api/posts/pk/
  - where pk - Post id
  
**Login:**

  ~/api/auth/login/
  
  Expected Input:
  {
    username,
    email(required),
    password(required),
  }

**Register new User:**

  ~/api/auth/register/
  
  Expected Input:
  {
    username,
    email(required),
    password(required),
  }

**Logout:**

  ~/api/auth/logout/

**Like Post:**

  ~/api/posts/like/pk
  
**Dislike Post:**

  ~/api/posts/dislike/pk
