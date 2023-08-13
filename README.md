# openai_sample
Llama Indexを用いた独自データを使ったチャット応答プログラムです。

## 初期設定
1. ライブラリのインストール  
※venv利用推奨
```
pip install -r requirements.txt
```

2. OpenAIのAPIキーを登録
事前にOpenAIのAPIキーを取得し、".env"ファイルのOPENAI_API_KEYに設定する。  
OpenAIのAPIを利用する場合はOPENAI_API_KEYの設定のみでよい。  
Azure OpenAI利用時は、追加で下記の環境変数の設定も必要になりそう。
```
OPENAI_API_TYPE="azure"
OPENAI_API_BASE="<エンドポイント>"
OPENAI_API_VERSION="yyyy-mm-dd"
```  
※Azure OpenAI利用時の参考  
https://gpt-index.readthedocs.io/en/latest/examples/customization/llms/AzureOpenAI.html

## 独自データにファイルを利用する場合
1. app/フォルダ内にフォルダを作成し、そのフォルダ内に学習データ用のドキュメントを格納する  
学習データのフォーマットは.txt/.docx/.xlsx/.pptx/.pdf ・・・などいろいろいける

2. 作成したフォルダ名をdocuments.pyのtrain_data_dir変数に設定

3. documents.pyのqry変数にクエリを設定

4. 下記のコマンドでプログラムを実行
```
cd app
python documents.py
```

## 独自データにWebページを利用する場合
1. web.pyのurl_list変数に学習データ用のWebページを設定

2. web.pyのqry変数にクエリを設定

3. 下記のコマンドでプログラムを実行
```
cd app
python web.py
```