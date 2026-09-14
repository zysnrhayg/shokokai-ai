import boto3
from botocore.exceptions import ClientError
from log_util import Log


logger = Log.get_logger()


def get_user_id_from_cognito(token:str) -> dict:
    """CognitoにアクセストークンでCognitoユーザープールのユーザー情報を問い合わせる
    アクセストークンはAPIリクエスト時にAuthorizationリクエストヘッダに以下のように設定される。
    Authorization: bearer <access_token>

    ユーザーIDはCognitoユーザー情報のUsernameに設定されている。

    Args:
        token (str): Cognitoアクセストークン
    
    Returns:
        dict: Cognitoユーザープールのユーザー情報
    """
    FUNCTION_NAME = '共通機能(CognitoユーザーID取得)'

    # Cognitoクライアントを取得    
    client = boto3.client('cognito-idp')

    # Cognitoユーザー情報を取得
    try:
        logger.info(f'{FUNCTION_NAME}: アクセストークン {token}')
        user_info = client.get_user(AccessToken = token)
        username = user_info.get('Username', '')
        logger.info(f'{FUNCTION_NAME}: ユーザーID {username}')
        return user_info
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        logger.info(f'{FUNCTION_NAME}: {error_code} {error_message}')
        if error_code == 'NotAuthorizedException':
            logger.info(f'{FUNCTION_NAME}: 無効なトークン')
        return None
