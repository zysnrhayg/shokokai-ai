"""共通部品（設定処理）
"""
from dynaconf import Dynaconf


# 設定ファイルを読み込む
settings = Dynaconf(environments=False, load_dotenv=True)

class Config:
    """設定処理クラス
    設定ファイルから各種設定値取得処理。

    Raises:
        Exception: 設定ファイル不正
    """

    # 設定項目キー: AWSリージョン
    AWS_REGION = 'AWS_REGION'

    # 設定項目キー: DB接続情報
    DB_SETTING = 'DATABASE'

    # DB接続情報項目キー名
    DB_SETTING_KEYS = [
        'DRIVERNAME',
        'HOST',
        'PORT',
        'DATABASE',
        'USERNAME',
        'PASSWORD'
    ]


    @classmethod
    def get_setting_str(cls, key:str, def_val:str = "") -> str:
        """設定ファイル(settings.yml)から文字列型の設定値を取得する。

        Args:
            key (str): 設定キー
            def_val (str, optional): デフォルト値（未設定の場合は空文字）

        Returns:
            str: 設定値
        """
        return settings.get(key, def_val)
