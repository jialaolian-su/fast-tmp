# -*- encoding: utf-8 -*-
"""
@File    : main.py
@Time    : 2020/12/2 21:57
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
import uvicorn

from example import settings
from example.factory import create_app

app = create_app()
x = {
    "openapi": "3.0.2",
    "info": {
        "title": "app1的接口文档",
        "version": "0.1.0"
    },
    "servers": [{
        "url": "/test"
    }],
    "paths": {
        "/app1/login": {
            "post": {
                "summary": "登录",
                "operationId": "login_app1_login_post",
                "requestBody": {
                    "content": {
                        "application/x-www-form-urlencoded": {
                            "schema": {
                                "$ref": "#/components/schemas/Body_login_app1_login_post"
                            }
                        }
                    },
                    "required": True
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "text/plain": {
                                "schema": {
                                    "type": "string"
                                }
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/app1/user": {"get": {"summary": "用户信息", "operationId": "userinfo_app1_user_get", "requestBody": {
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Login2"}}}, "required": True},
                               "responses": {"200": {"description": "Successful Response",
                                                     "content": {"text/plain": {"schema": {"type": "string"}}}},
                                             "422": {"description": "Validation Error",
                                                     "content": {"application/json": {
                                                         "schema": {
                                                             "$ref": "#/components/schemas/HTTPValidationError"}}}}}}}},
    "components": {
        "schemas": {
        "Body_login_app1_login_post": {
            "title": "Body_login_app1_login_post",
            "required": ["username", "password"],
            "type": "object",
            "properties": {
                "username": {
                    "title": "Username", "maxLength": 1, "type": "string"},
                "password": {
                    "title": "Password", "type": "string"
                }
            }
        },
        "HTTPValidationError": {
            "title": "HTTPValidationError",
            "type": "object",
            "properties": {
                "detail": {
                    "title": "Detail",
                    "type": "array",
                    "items": {
                        "$ref": "#/components/schemas/ValidationError"}}}},
        "Login2": {
            "title": "Login2",
            "required": ["username", "d"],
            "type": "object",
            "properties": {
                "username": {
                    "title": "Username",
                    "type": "string"
                },
                "d": {
                    "title": "D",
                    "type": "string",
                    "format": "date-time"
                }
            }
        },
        "UserInfo": {"title": "UserInfo", "required": ["name", "nickname", "age"], "type": "object",
                     "properties": {"name": {"title": "Name", "type": "string"},
                                    "nickname": {"title": "Nickname", "type": "string"},
                                    "age": {"title": "Age", "type": "integer"}}, "description": "用户信息"},
        "ValidationError": {"title": "ValidationError", "required": ["loc", "msg", "type"], "type": "object",
                            "properties": {"loc": {"title": "Location", "type": "array", "items": {"type": "string"}},
                                           "msg": {"title": "Message", "type": "string"},
                                           "type": {"title": "Error Type", "type": "string"}}}}}}

if __name__ == "__main__":
    uvicorn.run(
        "example.main:app", host="0.0.0.0", port=8000, debug=settings.DEBUG, reload=settings.DEBUG, lifespan="on"
    )
