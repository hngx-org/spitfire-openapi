# API Documentation

## Table of Contents

1. [Introduction](#introduction)
- [Base Uri/Live Deployment](#base-uri)
2. [Error Handling](#error-handling)
3. [User Management](#user-management)
   - 3.1 [Authentication](#authentication)
     - 3.1.1 [register User](#register-user)
     - 3.1.2 [login user](#login-user)
     - 3.1.3 [Get Logged in User Profile](#get-currently-logged-in-user-profile)
     - 3.1.4 [Logout User](#logout)
4. [User Interraction](#user-interraction)
4. [Authors](#authors)
5. [Conclusion](#conclusion)



## IntroductionDev-wonderful
Welcome to the API documentation for our user and event management system. This API documentation provides detailed information about the endpoints. It includes information on how to use each endpoint, expected input data, success responses, and HTTP status codes.

### **Base Uri**
----
----
temporarily hosted for live testing on **https://spitfire-openai.onrender.com**
....


## Error Handling
The API handles errors gracefully and returns JSON responses with appropriate status codes and error messages. Here are some common error responses:

### 400 Bad Request
- **Status Code**: 400
- **Response**:

```JSON
{
  "error": "Bad Request",
  "message": "Invalid input data."
}
```
### 402 Payment Required
- **Status Code**: 402
- **Response**:

```JSON
{
  "error": "Subscription Required",
  "message": "You do not have enough credits"
}
```

### 405 Method Not Allowed
- **Status Code**: 405
- **Response**:

```JSON
{
  "error": "Method Not Allowed",
  "message": "The HTTP method used is not allowed for this endpoint."
}

```
### 413 Payload Too Long
- **Status Code**: 413
- **Response**:

```JSON
{
  "error": "Payload Too Long",
  "message": "The request body is too long"
}

```

### 422 Unprocessable Entity
- **Status Code**: 422
- **Response**:

```JSON
{
  "error": "Unprocessable Entity",
  "message": "The server cannot process the request due to invalid data."
}
```

### 429 Too Many Requests
- **Status Code**: 429
- **Response**:

```JSON
{
  "error": "Too Many Requests",
  "message": "Rate limit exceeded. Please try again later."
}

```

### 500 Internal Server Error
- **Status Code**: 500
- **Response**:

```JSON
{
  "error": "Internal Server Error",
  "message": "It's not you, it's us. We encountered an internal server error."
}

```

## User Management 

### Authentication
- Session based Authentication is used
- A Session Cookie is sent and stored on client after athenticating with google
- subsequent requests should come with the cookie in the request headers
- session cookies expire after 30 days
### register User
- **Endpoint**: **POST** /api/auth/register
- **Description**: Register new user account.
- **Request Body**: 
    - **Input**: JSON with the following.
    ```JSON
    {
      "name": "name",
      "email":"test@mail.com",
      "password": "password",
      "confirm_password": "password"
    }
    ```

- **Success Response**:
    - **Status Code**: 201 (CREATED)
    - **Response**:
    ```JSON
    {
        "message": "User Created Succesfully",
        "data": {
            "name": "name",
            "email": "test@mail.com",
            "id": "1"
        },
    }
    ```


### login User
- **Endpoint**: **POST** /api/auth/login
- **Description**: login user account.
- **Request Body**: 
    - **Input**: JSON with the following.
    ```JSON
    {
      "email":"test@mail.com",
      "password": "password",
    }
    ```

- **Success Response**:
    - **Status Code**: 200 (OK)
    - **Response**:
    ```JSON
    {
        "message": "success",
        "data": {
            "name": "name",
            "email": "test@mail.com",
            "id": "1"
        },
    }
    ```


### Get Currently Logged In User Profile
- **Endpoint**: **GET** /api/auth/@me
- **Description**: Get user details of the currently logged in user
- **Success Response**:
    - **Status Code**: 200 (OK)
    - **Response**:
    ```JSON
    {

      "message": "success",
      "data":{
         "id": "user_id",
         "name": "user display name",
         "email": "user email",
       }
    }

### Logout
- **Endpoint**: **GET/POST** `/api/auth/logout`
- **Description**: log out user session
- **Success Response**:
    - **Status Code**: 200 (OK)
    - **Response**:
    ```JSON
    {
      "message": "success",
    }
    ```
## User Interractions 
The API receives user Requests and acts as a bridge to gracefully transfer the requests to GPT-3.5 and the AI response is converted to JSON  by the API, which is then sent to the user with appropriate status codes.

### Interractions
-   **Endpoint: /api/chat/completions**
-    **Description** Generates a chat completion using the GPT-3.5-turbo model from OpenAI.
- **Request Body**: 
    - **Input**: JSON with the following.
    ```JSON
    {
      "user_input": "what is spitfire?",
    }
    ```

-    **Success Response:**
    - **Status Code**: 201 (Created)
   - **Response**:
      ```JSON
      {
        "message": "Spitfire can refer to different things, so I'll cover a few possibilities"

      }
      ```
## Authors
- [@Godhanded](https://github.com/Godhanded)
- [@Freeman-kuch](https://github.com/Freeman-kuch)
- [@Dev-wonderful](https://github.com/Dev-wonderful)

## Conclusion