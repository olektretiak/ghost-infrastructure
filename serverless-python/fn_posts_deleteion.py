import json
import jwt
import requests
import logging 
from datetime import datetime as dt

log = logging.getLogger()
log.setLevel(logging.INFO)

SUCCESS = "SUCCESS"
FAILED = "FAILED"

def create_enc_token(admin_api_key):
    log.info("Creating encrypted token...")
    key = admin_api_key
    id, secret = key.split(":")
    iat = int(dt.now().timestamp())
    header = {"alg": "HS256", "typ": "JWT", "kid": id}
    payload = {"iat": iat, "exp": iat + (5 * 60), "aud": "/v3/admin/"}
    token = jwt.encode(
        payload, bytes.fromhex(secret), algorithm="HS256", headers=header
    )
    return token


def create_headers(admin_api_key):
    log.info("Creating headers...")
    token = create_enc_token(admin_api_key)
    headers = {"Authorization": "Ghost {}".format(token)}
    return headers


def get_all_posts(blog_endpoint, blog_token):
    log.info("Getting all posts...")
    url = blog_endpoint + "/ghost/api/content/posts/?key=" + blog_token
    params = {"formats": "html,mobiledoc", "limit": "all", "filter": "slug: -tags"}
    try:
        result = requests.get(url, params=params)
        if result.status_code != 200:
            log.warn(f"Site is no reachable: {url}")
    except requests.exceptions.ConnectionError as e:
        log.error(f"Error: {e}")
        raise
    posts = json.loads(result.text)["posts"]
    return posts


def delete_all_posts(list_of_posts, blog_endpoint, admin_api_key):
    for post in list_of_posts:
        url = blog_endpoint + "/ghost/api/admin/posts/" + post["id"] + "/"
        log.info(f"post id will be deleted: {post['id']}")
        result = requests.delete(url, headers=admin_api_key)
        if result.ok:
            result = (
                "success: post deleted (status_code:" + str(result.status_code) + ")"
            )
            log.info(result)
        else:
            result = (
                "error: post NOT deleted (status_code:" + str(result.status_code) + ")"
            )
            log.info(result)


def is_valid_event(event):
    expected_fields = ["admin_api_key", "content_api_key", "blog_endpoint"]
    return all(field in expected_fields for field in event)


def lambda_handler(event, context):
    if not is_valid_event(event):
        log.error(f"Provided event {event} is not valid.")
        return FAILED

    try:
        tmp_key = create_headers(admin_api_key=event["admin_api_key"])
        delete_all_posts(
            list_of_posts=get_all_posts(
                blog_endpoint=event["blog_endpoint"], blog_token=event["content_api_key"]
            ),
            blog_endpoint=event["blog_endpoint"],
            admin_api_key=tmp_key,
        )
    except Exception as e:
        log.error(f"Exception happened during lambda execution: {e}")
        return FAILED

    return SUCCESS

