#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Redis Keys
KEY_SMS_VERIFY_ID = "sms:verify_id:{uuid}"
KEY_SMS_SENDED = "sms:sended:{phone}"
KEY_SMS_CODE = "sms:code:{phone}"
KEY_SMS_TOTAL = "sms:total:count:{region}"
KEY_SMS_VERIFY_LIMIT = "sms:verify:limit:{phone}"
KEY_FORWARD_MESSAGE = "forward:message:{group_id}"
