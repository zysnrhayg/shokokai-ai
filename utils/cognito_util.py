""" 共通関数 """

from datetime import datetime, timedelta, timezone
import jwt
import json
from botocore.exceptions import ClientError
from sqlalchemy import select
from sqlalchemy.orm import Session
import boto3
from flask import request, jsonify
from util.log_util import Log 
from util.config_util import Config
from util.get_user_id_from_cognito import get_user_id_from_cognito
import hmac, hashlib, base64
from jwt.exceptions import DecodeError


logger = Log.get_logger()
client_cognito = boto3.client('cognito-idp')

def get_user_id() -> str:
    """TokenからUserIDを取得"""

    auth = request.headers.get('Authorization')
    if auth is None:
        logger.info(f'Authorizationヘッダ不正(None)')
        return None

    # リクエストヘッダからアクセストークンを分離
    try:
        (_, access_token) = request.headers.get('Authorization').split()
    except:
        logger.info(f'Authorizationヘッダ不正')
        return None
    
    # アクセストークンを使用した認証処理
    # ここで認証が成功すれば、正常な処理を続行
    # アクセストークンでCognitoユーザー情報照会
    response = get_user_id_from_cognito(access_token)
    logger.info(f'response: {response}')
    # レスポンスからユーザーIDを取得
    user_id = response['Username']
    logger.info('get_user_id: %s', user_id)

    # 取得したユーザーIDを返却
    return user_id


def get_user_mail() -> str:
    """TokenからUserIDを取得"""

    auth = request.headers.get('Authorization')
    if auth is None:
        logger.info(f'Authorizationヘッダ不正(None)')
        return None

    # リクエストヘッダからアクセストークンを分離
    try:
        (_, access_token) = request.headers.get('Authorization').split()
    except:
        logger.info(f'Authorizationヘッダ不正')
        return None

    # アクセストークンでCognitoユーザー情報照会
    response = get_user_id_from_cognito(access_token)
    if not response:
        logger.info(f'無効なアクセストークン')
        return None
    
    # レスポンスからユーザー属性を取得
    UserAttributes = response['UserAttributes']

    email = None
    for attribute in UserAttributes:
        if attribute['Name'] == 'email':
            email = attribute['Value']
            break

    # 取得したメールアドレスを返却
    return email

def get_user_email_by_userid(user_id):
    client = boto3.client('cognito-idp')
    
    try:
        response = client.admin_get_user(
            UserPoolId = Config.get_setting_str('USER_POOL_ID'),
            Username = user_id,
        )
        for attribute in response['UserAttributes']:
            if attribute['Name'] == 'email':
                return attribute['Value']
    except client.exceptions.UserNotFoundException:
        logger.warning("User not found")
    except Exception as e:
        logger.exception("get_user_email_by_userid failed")
    return None


def send_mail(to_addr: str, subject: str, content: str, cc_addr: str = None, bcc_addr: str = None, reply_addr: str = None):
    """TokenからUserIDを取得"""

    client = boto3.client('sesv2')
    # logger.info("content: %s", content)
    # logger.info("send mail: %s", Config.get_setting_str('SEND_EMAIL_FROM'))
    try: 
        response = client.send_email(
            FromEmailAddress = Config.get_setting_str('SEND_EMAIL_FROM'),
            Destination={
                'ToAddresses': [
                    to_addr,
                ],
                # 'CcAddresses': [
                #     cc_addr,
                # ],
                # 'BccAddresses': [
                #     bcc_addr,
                # ]
            },
            # ReplyToAddresses=[
            #     reply_addr,
            # ],
            Content={
                'Simple': {
                    'Subject': {
                        'Data': subject,
                        'Charset': 'UTF-8'
                    },
                    'Body': {
                        'Html': {
                            'Data': content,
                            'Charset': 'UTF-8'
                        }
                    }
                },
            }
        )
        # 送信結果をログ出力
        logger.info(f"send result: {response}")
        result = {
            'send_status': 1,
            'msg': "",
        }
        return result
    except Exception as ex:
        logger.error(f"send mail error: {ex}")
        result = {
            'send_status': 0,
            'msg': str(ex),
        }
        return result


def edit_kana_for_verify(in_str:str, need_cut:bool = False)->str:
    """照合用カナ文字列の編集処理

    Args:
        in_str (str): 編集対象文字列
        need_cut (bool, ooptional): 先頭40桁取得フラグ
    Returns:
        str: 編集結果文字列
    """

    # 1.半角スペースを全角スペースへ変換
    in_str = in_str.replace(' ', '　')

    # 2.半角ハイフン「-」記号をに全角長音「ー」、半角長音「ｰ」置換
    in_str = in_str.replace('-', 'ー')\
                   .replace('ｰ', 'ー')

    # 3.半角カナを濁点・半濁点の全角カナに置換
    in_str = in_str.replace('ｶﾞ', 'ガ')\
               .replace('ｷﾞ', 'ギ')\
               .replace('ｸﾞ', 'グ')\
               .replace('ｹﾞ', 'ゲ')\
               .replace('ｺﾞ', 'ゴ')\
               .replace('ｻﾞ', 'ザ')\
               .replace('ｼﾞ', 'ジ')\
               .replace('ｽﾞ', 'ズ')\
               .replace('ｾﾞ', 'ゼ')\
               .replace('ｿﾞ', 'ゾ')\
               .replace('ﾀﾞ', 'ダ')\
               .replace('ﾁﾞ', 'ヂ')\
               .replace('ﾂﾞ', 'ヅ')\
               .replace('ﾃﾞ', 'デ')\
               .replace('ﾄﾞ', 'ド')\
               .replace('ﾊﾞ', 'バ')\
               .replace('ﾋﾞ', 'ビ')\
               .replace('ﾌﾞ', 'ブ')\
               .replace('ﾍﾞ', 'ベ')\
               .replace('ﾎﾞ', 'ボ')\
               .replace('ﾊﾟ', 'パ')\
               .replace('ﾋﾟ', 'ピ')\
               .replace('ﾌﾟ', 'プ')\
               .replace('ﾍﾟ', 'ペ')\
               .replace('ﾎﾟ', 'ポ')\
               .replace('ｳﾞ', 'ヴ')

    # 4.小文字の全・半角カナを大文字の全角カナ置換
    in_str = in_str.replace('ｧ', 'ア')\
               .replace('ｨ', 'イ')\
               .replace('ｩ', 'ウ')\
               .replace('ｪ', 'エ')\
               .replace('ｫ', 'オ')\
               .replace('ｯ', 'ツ')\
               .replace('ｬ', 'ヤ')\
               .replace('ｭ', 'ユ')\
               .replace('ｮ', 'ヨ')\
               .replace('ァ', 'ア')\
               .replace('ィ', 'イ')\
               .replace('ゥ', 'ウ')\
               .replace('ェ', 'エ')\
               .replace('ォ', 'オ')\
               .replace('ヵ', 'カ')\
               .replace('ヶ', 'ケ')\
               .replace('ッ', 'ツ')\
               .replace('ャ', 'ヤ')\
               .replace('ュ', 'ユ')\
               .replace('ョ', 'ヨ')\
               .replace('ヮ', 'ワ')

    # 5.半角カナを全角カナに置換
    in_str = in_str.replace('ｱ', 'ア')\
               .replace('ｲ', 'イ')\
               .replace('ｳ', 'ウ')\
               .replace('ｴ', 'エ')\
               .replace('ｵ', 'オ')\
               .replace('ｶ', 'カ')\
               .replace('ｷ', 'キ')\
               .replace('ｸ', 'ク')\
               .replace('ｹ', 'ケ')\
               .replace('ｺ', 'コ')\
               .replace('ｻ', 'サ')\
               .replace('ｼ', 'シ')\
               .replace('ｽ', 'ス')\
               .replace('ｾ', 'セ')\
               .replace('ｿ', 'ソ')\
               .replace('ﾀ', 'タ')\
               .replace('ﾁ', 'チ')\
               .replace('ﾂ', 'ツ')\
               .replace('ﾃ', 'テ')\
               .replace('ﾄ', 'ト')\
               .replace('ﾅ', 'ナ')\
               .replace('ﾆ', 'ニ')\
               .replace('ﾇ', 'ヌ')\
               .replace('ﾈ', 'ネ')\
               .replace('ﾉ', 'ノ')\
               .replace('ﾊ', 'ハ')\
               .replace('ﾋ', 'ヒ')\
               .replace('ﾌ', 'フ')\
               .replace('ﾍ', 'ヘ')\
               .replace('ﾎ', 'ホ')\
               .replace('ﾏ', 'マ')\
               .replace('ﾐ', 'ミ')\
               .replace('ﾑ', 'ム')\
               .replace('ﾒ', 'メ')\
               .replace('ﾓ', 'モ')\
               .replace('ﾔ', 'ヤ')\
               .replace('ﾕ', 'ユ')\
               .replace('ﾖ', 'ヨ')\
               .replace('ﾗ', 'ラ')\
               .replace('ﾘ', 'リ')\
               .replace('ﾙ', 'ル')\
               .replace('ﾚ', 'レ')\
               .replace('ﾛ', 'ロ')\
               .replace('ﾜ', 'ワ')\
               .replace('ｦ', 'ヲ')\
               .replace('ﾝ', 'ン')

    
    
def add_user_mail_address(email: str, user_id: str) -> dict:
    '''管理者権限でメールアドレスをユーザに追加'''
    
    client = boto3.client('cognito-idp')
    try:
        response = client.admin_update_user_attributes(
            UserPoolId = Config.get_setting_str('USER_POOL_ID'),
            Username = user_id,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': email
                },
                                {
                    'Name': 'email_verified',
                    'Value': 'true'
                },
                 
            ]
        )
        result = {
            'send_status': 1,
            'msg': "",
        }
        return result
    except Exception as ex:
        logger.error(f"send mail error: {ex}")
        result = {
            'send_status': 0,
            'msg': str(ex),
        }
        return result

def get_token(**kwarg):
    """パスワード変更用認証トークン生成
    """
    send_status = ''
    msg = ''

    exp = datetime.now(tz=timezone.utc) + timedelta(hours=1)
    email = kwarg.get('email')
    user_id = kwarg.get('user_id')
    if user_id is None:
        user_id = get_user_id(email)
        # cognitoからのレスポンスコード
        send_status = user_id.get('send_status')
        # cognitoからのレスポンスメッセージ
        msg = user_id.get('msg')
    logger.info(f"user_id: {user_id}")

    if send_status == 0:
        return send_status

    jwt_secret = Config.get_setting_str('JWT_SECRET')
    token = jwt.encode({
        'exp': exp,
        'user_id': user_id,
        'email': email,
    },
        jwt_secret,
        'HS256',
    )
    logger.info(f"token　: {token}")
    cognito_secret = get_cognito_secret()
    try:
        client_cognito \
            .admin_update_user_attributes(UserPoolId=cognito_secret['USER_POOL_ID'],
                                          Username=user_id,
                                          UserAttributes=[
                                              {
                                                  'Name': 'custom:token',
                                                  'Value': token,
                                              },
                                          ]
                                          )
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        logger.error(f'AWS APIエラー: {user_id} {error_code} {error_message}')
        raise e
    logger.info(f'パスワード変更トークン発行: {user_id} {token}')
    return token
  
  
def get_cognito_secret():
    """Cognitoシークレット情報取得
    """
    # AWSリージョン取得
    region_name = Config.get_setting_str(Config.AWS_REGION)
    logger.info(f"region_name:{region_name}")
    
    # Cognitoシークレット情報のシークレット名取得
    secret_name = Config.get_setting_str('COGNITO_SECRET')
    logger.info(f"secret_name:{secret_name}")

    client = boto3.client('secretsmanager', region_name = region_name)
    secret_value = client.get_secret_value(SecretId = secret_name)

    return json.loads(secret_value['SecretString'])



def get_user_id_by_mail_or_login_id(email: str, login_id: str) -> dict:
    '''ログインIDまたはメールアドレスからユーザIDを取得'''

    client = boto3.client('cognito-idp')
    try:
        logger.info(f"email: {email}, login_id: {login_id}")
        response = client.list_users(
            UserPoolId=Config.get_setting_str('USER_POOL_ID'),
            AttributesToGet=['email'],
            Filter=f'email = \"{email}\"'
        )
        users = response.get("Users", [])
        logger.info(f"users: {users}")
        
        # 次にログインIDをフィルタとして使用
        response_login = client.list_users(
            UserPoolId=Config.get_setting_str('USER_POOL_ID'),
            AttributesToGet=['email'],
            Filter=f'username = \"{login_id}\"'
        )
        users_login = response_login.get("Users", [])
        logger.info(f"users_login: {users_login}")

        if len(users_login) == 0:
            result = {
                'send_status': 0,
                'msg': "該当ユーザが存在しません。",
            }
            return result
            logger.info(f"result: {result}")
        else:
            user = list(users_login)[0]  # 最初のユーザを取得
            userid = user.get("Username")
            logger.info(f"userid: {userid}")
            result = {
                'send_status': 1,
                'userid': userid,
            }
            return result
            logger.info(f"result: {result}")
    except Exception as ex:
        logger.error(f"send mail error: {ex}")
        result = {
            'send_status': 0,
            'msg': str(ex),
        }
        return result


def add_user_expirydate_and_userkbn(date: str, user_id: str) -> dict:
    '''管理者権限で有効期限日、ユーザ区分をユーザに追加'''

    client = boto3.client('cognito-idp')
    try:
        response = client.admin_update_user_attributes(
            UserPoolId = Config.get_setting_str('USER_POOL_ID'),
            Username = user_id,
            UserAttributes=[
                {
                    'Name': 'custom:expiration_date',
                    'Value': date
                },
                {
                    'Name': 'custom:user_kbn',
                    'Value': '05'
                },

            ]
        )
        result = {
            'send_status': 1,
            'msg': "",
        }
        return result
    except Exception as ex:
        logger.error(f"send mail error: {ex}")
        result = {
            'send_status': 0,
            'msg': str(ex),
        }
        return result
    
    

'''settings.xml template
'''
'''
# 開発環境設定
# AWSリージョン（東京リージョン）
AWS_REGION: ap-northeast-1

# Cognitoシークレット名
AWS_COGNITO_SECRET: KE-DEV-SECRET-COGNITO-01

# パスワード変更トークンソルト
JWT_SECRET: KE-DEV-JWTSECRET-01

# 認証メール
SEND_EMAIL_FROM: xxx@xxx.com
USER_POOL_ID: ap-northeast-1_1REXNTSOx

# 一時ユーザーIDの長さ
TMEP_USER_ID_LENGTH: 10
# 一時ユーザーIDプレフィクス
TEMP_USER_ID_PREFIX: TMPUSR
# 一時ユーザーパスワード
TEMP_USER_PASSWORD: Test#1234!


# S3バケット名（静的コンテンツ）
S3_BUCKET: ke-dev-s3-staticcontent-01
# 設定ファイル
S3_SETTINGS_FILE: settings.properties

'''
