import os
from dotenv import load_dotenv
# 事前に.envファイルに"OPENAI_API_KEY"の環境変数を設定しておく
load_dotenv()

from langchain.chat_models import ChatOpenAI
from llama_index import download_loader, GPTVectorStoreIndex, ServiceContext, LLMPredictor

url_list = [
    "https://ja.wikipedia.org/wiki/Python",
    "https://ja.wikipedia.org/wiki/JavaScript",
    "https://ja.wikipedia.org/wiki/Java"
]
index_json = 'index_web.json'


def main():
    # Webページのドキュメントを読み込み
    BeautifulSoupWebReader = download_loader("BeautifulSoupWebReader")
    loader = BeautifulSoupWebReader()
    documents = loader.load_data(urls=url_list)

    # LLMにgpt-3.5-turbo を指定（現状デフォルトは davinci ）
    service_context = ServiceContext.from_defaults(llm_predictor = LLMPredictor(llm= ChatOpenAI( model_name="gpt-3.5-turbo")))
    # documents をもとに Embbeddings API を通信してベクター取得し GPTVectorStoreIndex を生成
    index = GPTVectorStoreIndex.from_documents(documents, service_context=service_context)

    # 作成したインデックスをディスクに保存
    index.storage_context.persist(persist_dir=index_json)

    # プロンプト
    query_engine = index.as_query_engine()
    qry = "機械学習のアプリケーションを実装したい場合はどのプログラミング言語がおすすめですか？" 

    # ベクター検索 + Chat Completion API 実行
    response = query(query_engine, qry)
    print("Answer:", response)


def load_from_storage():
    """
    作成済みのインデックスを読み込む関数
    """
    storage_context = StorageContext.from_defaults(persist_dir=index_json)
    index = load_index_from_storage(storage_context)
    return index


def query(query_engine, query:str) -> str:
    """
    クエリを投げた結果を返す関数
    """
    response = query_engine.query(query)
    return response


if __name__ == '__main__':
    main()
