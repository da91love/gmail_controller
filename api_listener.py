# 必要なモジュールの読み込み
import sys
import os
from flask import Flask, jsonify, abort, make_response, request
from flask_cors import CORS

# import apis
from api_gmail_checker.app import app_api_gmail_checker as check_emails
from api_gmail_sender.app import app_api_gmail_sender as send_email
from api_gmail_remind_sender.app import app_api_gmail_remind_sender as send_remind_email
from api_status_updater.app import app_api_status_updater as update_status


os.path.dirname(sys.modules['__main__'].__file__)

# Flaskクラスのインスタンスを作成
# __name__は現在のファイルのモジュール名

api = Flask(__name__)
cors = CORS(api)

"""
# This flask API is only used for the development stage.
# DO NOT deploy on production
"""

@api.route('/update-status', methods=['get'])  # TODO : Insert any URL
def update_status_get():
    # Get body, headers
    # body = request.json
    # headers = request.headers
    # params = request.args

    # Insert necessary data to body
    data = {
        'context': {
            'http-method': 'GET'
        }
    }

    result = update_status(data)

    return make_response(jsonify(result))

@api.route('/send-remind-mail', methods=['get'])  # TODO : Insert any URL
def send_remind_mail_get():
    # Get body, headers
    # body = request.json
    # headers = request.headers
    # params = request.args

    # Insert necessary data to body
    data = {
        'context': {
            'http-method': 'GET'
        }
    }

    result = send_remind_email(data)

    return make_response(jsonify(result))

@api.route('/check-emails', methods=['post'])  # TODO : Insert any URL
def check_email_get():
    # Get body, headers
    body = request.json
    headers = request.headers

    result = check_emails(body)

    return make_response(jsonify(result))

@api.route('/send-email', methods=['post'])  # TODO : Insert any URL
def send_email_post():
    # Get body, headers
    body = request.json
    headers = request.headers

    # Insert necessary data to body
    data = None
    result = send_email(body)

    return make_response(jsonify(result))


# エラーハンドリング
@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


# ファイルをスクリプトとして実行した際に
# ホスト0.0.0.0, ポート3001番でサーバーを起動
if __name__ == '__main__':
    api.run(host='0.0.0.0', port=8888)  # TODO : Insert any port number