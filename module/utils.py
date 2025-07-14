import re

def normalize_name(name: str) -> str:
    """
    馬名を正規化する（全角→半角、スペース除去など）
    'の'の次に'20'を挿入する（例：ヒルダズパッションの24 → ヒルダズパッションの2024）
    
    Args:
        name (str): 正規化前の馬名
        
    Returns:
        str: 正規化後の馬名
    """
    if not name:
        return ""
    
    # 前後の空白を除去
    normalized = name.strip()
    
    # 全角英数字を半角に変換
    normalized = normalized.translate(str.maketrans(
        'ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ０１２３４５６７８９',
        'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    ))
    
    # 全角スペースを半角スペースに変換
    normalized = normalized.replace('　', ' ')
    
    # 連続する空白を単一の空白に変換
    normalized = re.sub(r'\s+', ' ', normalized)
    
    # 前後の空白を再度除去
    normalized = normalized.strip()

    # 右から3文字目が'の'の場合、'の'の次に'20'を挿入
    if len(normalized) >= 3 and normalized[-3] == 'の':
        if 'の' in normalized:
            parts = normalized.split('の')
            if len(parts) > 1:
                parts[1] = '20' + parts[1]
                normalized = 'の'.join(parts)
    
    return normalized