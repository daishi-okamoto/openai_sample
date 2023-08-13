# openai_sample
LlamaIndexとLangChainを用いた独自データを使ったチャット応答プログラムです。

## ライブラリ説明
### LlamaIndex
公開されていない独自データを使って質問応答を行うチャットAIを簡単に生成できるオープンソースライブラリ。「LLM」は公開されている大量のデータを事前学習して、それを元に文章生成や質問応答を行う。そのため、会社や個人が保有する公開されていない情報については回答できない。  
LlamaIndexでは、公開されていない情報をもとに、質問に応じて回答に関連情報を検索して、それを入力プロンプトに挿入し、LLMの推論能力を利用して応答を生成することで、この問題を解決する。
検索対象となる情報は「テキスト」だけでなく、PDF,ePub,Word,PowerPoint,Audioなどをはじめとする様々なファイル形式、Twitter,Youtube,Slack,Wikipediaなどの様々なWebサービスも指定できる。  
同様のチャットAIは、LangChainでも作成できるが、LlamaIndexは、質問応答の機能に特化することで、コード数行で簡単に作成できるようになっていることが特徴。

### LangChain
LLMを利用したアプリケーション甲斐亜hつを支援するオープンソースライブラリ。  
ChatGPTのようなアプリケーションを開発する際、単純に会話するだけであればOpenAI APIのみで十分なのでLangChainは必要ない。  
LangChainが役立つのは、LLMに外部の知識や計算能力を活用してもらいたい場合になる。自分が学習したことだけを使って会話していたLLMに、本やプログラムを渡して、外部の知識や計算の能力を利用できるようにさせるのがLangChainの役割。  
たとえば、LangChainでLLMにWeb検索の機能を繋げることで、LLMは自分の持っている知識だけでは十分な回答ができない場合でも、Web検索で最新情報を取得して回答できるようになる。

### LlamaIndexとLangChainの使い分け
LlamaIndexは、LangChainで構築したアプリケーションの一つになる。  
LlamaIndex内部ではLangChainが使われている。  
LangChainは絶え間なくLLMの最新技術を取り込んでいるため、最新技術を追い求めたい場合に適している。質問応答専用のチャットAIとして安定したサービスを提供したい場合には、LlamaIndexの方が適している。
  
参考：「OpenAI GPT-4 / ChatGPT /LangChain 人工知能プログラミング実践入門 - 布留川英一 著」

## 利用設定
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
