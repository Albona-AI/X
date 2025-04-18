import os
import requests
import json

def get_gemini_advice(error_message, context):
    api_key = os.getenv('GEMINI_API_KEY')
    url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent'
    headers = {
        'Content-Type': 'application/json',
        'x-goog-api-key': api_key
    }

    prompt = f'''以下のエラーに遭遇しました：
{error_message}

このエラーの原因と解決方法を教えてください。コンテキスト：{context}'''

    data = {
        'contents': [
            {
                'parts': [
                    {
                        'text': prompt
                    }
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    result = response.json()
    
    if 'candidates' in result and len(result['candidates']) > 0:
        text = result['candidates'][0]['content']['parts'][0]['text']
        return text
    else:
        return f"エラー：Gemini APIからの応答に問題があります。\n{json.dumps(result, indent=2, ensure_ascii=False)}"

if __name__ == "__main__":
    error_message = '''
ERROR: Could not find a version that satisfies the requirement twikit==0.5.1 (from versions: 1.0.3, 1.0.4, 1.0.5, 1.0.6, 1.0.7, 1.0.8, 1.1.0, 1.1.1, 1.1.2, 1.1.3, 1.1.4, 1.1.5, 1.1.6, 1.1.7, 1.1.8, 1.1.9, 1.1.10, 1.1.11, 1.1.12, 1.1.13, 1.1.14, 1.1.15, 1.1.16, 1.1.17, 1.1.18, 1.1.18.1, 1.1.18.2, 1.1.19, 1.1.21, 1.1.22, 1.1.23, 1.1.24a0, 1.1.24b0, 1.1.24, 1.1.25, 1.1.26, 1.1.27, 1.1.28, 1.1.28.1, 1.1.29, 1.2.0, 1.2.1, 1.2.2, 1.2.3, 1.2.4, 1.2.5, 1.2.5.1, 1.2.6a0, 1.2.6b0, 1.2.6rc0, 1.2.6, 1.2.7, 1.3.0, 1.3.1, 1.3.2, 1.3.3, 1.3.4, 1.3.5, 1.3.6, 1.3.7a0, 1.3.7b0, 1.3.7, 1.3.8, 1.3.9, 1.3.10, 1.3.11, 1.3.12, 1.3.13, 1.3.14, 1.3.15, 1.3.16, 1.4.0, 1.4.1, 1.4.2, 1.4.3, 1.4.4, 1.4.5, 1.4.6, 1.4.7, 1.4.8, 1.4.9, 1.5.0, 1.5.1, 1.5.2, 1.5.3, 1.5.4, 1.5.5, 1.5.6, 1.5.7, 1.5.8, 1.5.9, 1.5.10, 1.5.11, 1.5.12, 1.5.13, 1.5.14, 1.6.0, 1.6.1, 1.6.2, 1.6.4, 1.7.0, 1.7.1, 1.7.2, 1.7.3, 1.7.4, 1.7.5, 1.7.6, 2.0.0b1, 2.0.0b2, 2.0.0, 2.0.1, 2.0.2, 2.0.3, 2.1.0, 2.1.1, 2.1.2, 2.1.3, 2.2.0, 2.2.1, 2.2.2, 2.3.0, 2.3.1, 2.3.2, 2.3.3)
ERROR: No matching distribution found for twikit==0.5.1
'''
    context = "Pythonのrequirements.txtでtwikit==0.5.1を指定していますが、このバージョンが見つかりません。利用可能なバージョンの中から、どのバージョンを使用すべきでしょうか？"
    
    advice = get_gemini_advice(error_message, context)
    print("\n解決策：")
    print(advice)
