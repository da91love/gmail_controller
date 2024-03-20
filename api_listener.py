# 必要なモジュールの読み込み
import sys
import os
from flask import Flask, jsonify, abort, make_response, request
from flask_cors import CORS

# import apis
from api_gmail_checker.app import app_api_gmail_checker as check_emails
from api_gmail_force_checker.app import app_api_force_gmail_checker as force_check_emails
from api_gmail_sender.app import app_api_gmail_sender as send_email
from api_gmail_remind_sender.app import app_api_gmail_remind_sender as send_re_email
from api_status_updater.app import app_api_status_updater as update_status
from api_delivery_tracker.app import app_api_delivery_tracker as track_delivery
from api_gmail_converting_sender.app import app_api_gmail_converting_sender as send_converting_email
from api_tiktok_profile_updater.app import app_api_tiktok_profile_updater as get_profile_stat
from api_gmail_follow_up_sender.app import app_api_gmail_follow_up_sender as send_follow_up
from api_mia_reminder.app import app_api_mia_reminder as remind_mia


os.path.dirname(sys.modules['__main__'].__file__)

# Flaskクラスのインスタンスを作成
# __name__は現在のファイルのモジュール名

api = Flask(__name__)
cors = CORS(api)

"""
# This flask API is only used for the development stage.
# DO NOT deploy on production
"""
@api.route('/remind-mia', methods=['get'])  # TODO : Insert any URL
def remind_mia_get():
    # Get body, headers
    # body = request.json
    # headers = request.headers

    result = remind_mia(None)

    return make_response(jsonify(result))

@api.route('/send-follow-up', methods=['get'])  # TODO : Insert any URL
def send_follow_up_get():
    # Get body, headers
    # body = request.json
    # headers = request.headers

    result = send_follow_up(None)

    return make_response(jsonify(result))

@api.route('/get-profile-stat', methods=['get'])  # TODO : Insert any URL
def get_profile_stat_get():
    # Get body, headers
    # body = request.json
    # headers = request.headers

    result = get_profile_stat(None)

    return make_response(jsonify(result))
@api.route('/send-converting-mail', methods=['get'])  # TODO : Insert any URL
def send_converting_email_post():
    # Get body, headers
    # body = request.json
    # headers = request.headers

    result = send_converting_email(None)

    return make_response(jsonify(result))
@api.route('/track-delivery', methods=['post'])  # TODO : Insert any URL
def track_delivery_post():
    # Get body, headers
    # body = request.json
    # headers = request.headers

    result = track_delivery(None)

    return make_response(jsonify(result))


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

    result = send_re_email(data)

    return make_response(jsonify(result))

@api.route('/check-emails', methods=['post'])  # TODO : Insert any URL
def check_email_post():
    # Get body, headers
    body = request.json
    headers = request.headers

    result = check_emails(body)

    return make_response(jsonify(result))

@api.route('/force-check-emails', methods=['post'])  # TODO : Insert any URL
def force_check_emails_post():
    # Get body, headers
    body = request.json
    headers = request.headers

    result = force_check_emails(body)

    return make_response(jsonify(result))

@api.route('/send-email', methods=['post'])  # TODO : Insert any URL
def send_email_post():
    # Get body, headers
    # body = request.json
    # headers = request.headers

    # Insert necessary data to body
    # data = None
    result = send_email(None)

    return make_response(jsonify(result))


# エラーハンドリング
@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


# ファイルをスクリプトとして実行した際に
# ホスト0.0.0.0, ポート3001番でサーバーを起動
if __name__ == '__main__':
    api.run(host='0.0.0.0', port=8888)  # TODO : Insert any port number