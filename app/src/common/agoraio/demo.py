#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from app.src.common.agoraio.rtc_token import Role_Subscriber, RtcTokenBuilder


def main():
    app_id = ""
    app_certificate = ""
    channel_name = ""
    uid = 2882341273
    account = ""
    token_expiration_in_seconds = 3600
    privilege_expiration_in_seconds = 3600

    token = RtcTokenBuilder.build_token_with_uid(
        app_id,
        app_certificate,
        channel_name,
        uid,
        Role_Subscriber,
        token_expiration_in_seconds,
        privilege_expiration_in_seconds,
    )
    print("Token with int uid: {}\n".format(token))

    token = RtcTokenBuilder.build_token_with_user_account(
        app_id,
        app_certificate,
        channel_name,
        account,
        Role_Subscriber,
        token_expiration_in_seconds,
        privilege_expiration_in_seconds,
    )
    print("Token with user account: {}\n".format(token))

    token = RtcTokenBuilder.build_token_with_uid_and_privilege(
        app_id,
        app_certificate,
        channel_name,
        uid,
        privilege_expiration_in_seconds,
        privilege_expiration_in_seconds,
        privilege_expiration_in_seconds,
        privilege_expiration_in_seconds,
        privilege_expiration_in_seconds,
    )
    print("Token with int uid and privilege: {}".format(token))

    token = RtcTokenBuilder.build_token_with_user_account_and_privilege(
        app_id,
        app_certificate,
        channel_name,
        account,
        privilege_expiration_in_seconds,
        privilege_expiration_in_seconds,
        privilege_expiration_in_seconds,
        privilege_expiration_in_seconds,
        privilege_expiration_in_seconds,
    )
    print("Token with user account and privilege: {}".format(token))


if __name__ == "__main__":
    main()
