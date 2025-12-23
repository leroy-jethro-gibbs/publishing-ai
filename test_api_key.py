import streamlit as st
import anthropic

st.title("🔍 APIキー診断ツール")

# secrets.tomlからAPIキーを読み込み
if "ANTHROPIC_API_KEY" in st.secrets:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
    st.success("✅ secrets.tomlからAPIキーを読み込みました")
    
    # APIキーの情報を表示（先頭と末尾のみ）
    key_preview = f"{api_key[:20]}...{api_key[-10:]}"
    st.info(f"APIキー（プレビュー）: {key_preview}")
    st.info(f"APIキーの長さ: {len(api_key)} 文字")
    
    # APIキーのフォーマットチェック
    if api_key.startswith("sk-ant-"):
        st.success("✅ APIキーのフォーマットは正しいです")
    else:
        st.error("❌ APIキーのフォーマットが間違っています")
    
    # 余分なスペースや改行のチェック
    if api_key != api_key.strip():
        st.warning("⚠️ APIキーの前後に余分なスペースや改行があります")
        st.code(f"元: '{api_key}'")
        st.code(f"修正後: '{api_key.strip()}'")
        api_key = api_key.strip()
    else:
        st.success("✅ APIキーに余分なスペースや改行はありません")
    
    # 実際にAPI呼び出しをテスト
    if st.button("🧪 APIテスト実行", type="primary"):
        with st.spinner("テスト中..."):
            try:
                # Anthropic APIクライアント初期化
                client = anthropic.Anthropic(api_key=api_key)
                
                # 簡単なテストリクエスト
                message = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=100,
                    messages=[
                        {"role": "user", "content": "Hello, please respond with 'API test successful!'"}
                    ]
                )
                
                # 成功
                st.success("🎉 APIテスト成功！")
                st.code(message.content[0].text)
                
            except anthropic.AuthenticationError as e:
                st.error("❌ 認証エラー: APIキーが無効です")
                st.error(f"詳細: {e}")
                st.warning("""
                考えられる原因:
                1. APIキーが期限切れまたは無効化されている
                2. Anthropicアカウントに請求の問題がある
                3. APIキーの権限が不足している
                
                対処方法:
                1. Anthropic Consoleでアカウントの状態を確認
                2. 請求情報を確認
                3. 新しいAPIキーを作成
                """)
                
            except Exception as e:
                st.error(f"❌ エラーが発生しました: {type(e).__name__}")
                st.error(f"詳細: {e}")
                
else:
    st.error("❌ secrets.tomlにANTHROPIC_API_KEYが見つかりません")
    st.info("""
    secrets.tomlファイルを以下の場所に作成してください:
    .streamlit/secrets.toml
    
    内容:
    ```
    ANTHROPIC_API_KEY = "あなたのAPIキー"
    ```
    """)
