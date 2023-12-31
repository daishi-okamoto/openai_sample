from dotenv import load_dotenv
# 事前に.envファイルに"OPENAI_API_KEY"の環境変数を設定しておく
load_dotenv()

from langchain.chat_models import ChatOpenAI
from llama_index import (download_loader, GPTVectorStoreIndex,
                         ServiceContext, LLMPredictor)

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
    service_context = ServiceContext.from_defaults(
        llm_predictor=LLMPredictor(
            llm=ChatOpenAI(model_name="gpt-3.5-turbo")
        )
    )
    # documents をもとに Embbeddings API を通信してベクター取得し GPTVectorStoreIndex を生成
    index = GPTVectorStoreIndex.from_documents(
        documents,
        service_context=service_context
    )

    # 作成したインデックスをディスクに保存
    index.storage_context.persist(persist_dir=index_json)

    # プロンプト
    query_engine = index.as_query_engine(streaming=True)
    qry = ""

    # ベクター検索 + Chat Completion API 実行
    response = query(query_engine, qry)
    # stream形式でChatAIからのレスポンスを出力
    response.print_response_stream()


def query(query_engine, query: str) -> str:
    """
    クエリを投げた結果を返す関数
    """
    response = query_engine.query(query)
    return response


if __name__ == '__main__':
    main()
