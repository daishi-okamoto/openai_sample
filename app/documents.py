import os
from dotenv import load_dotenv
# 事前に.envファイルに"OPENAI_API_KEY"の環境変数を設定しておく
load_dotenv()

from langchain.chat_models import ChatOpenAI
from llama_index import (SimpleDirectoryReader, ServiceContext,
                         GPTVectorStoreIndex, LLMPredictor,
                         StorageContext, load_index_from_storage)

index_json = 'index_documents.json'


def main():
    """
    main処理
    """
    # インデックスが作成済みでない場合は新規で作成する処理から実施
    if not os.path.isdir(index_json):
        # 学習データのディレクトリ
        train_data_dir = 'data_documents'
        # train_data_dirから学習データの情報を取得
        documents = SimpleDirectoryReader(train_data_dir).load_data()
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
    else:
        # 作成済みのインデックスを読み込み
        index = load_from_storage()

    # プロンプト
    query_engine = index.as_query_engine(streaming=True)
    qry = ""

    # ベクター検索 + Chat Completion API 実行
    response = query(query_engine, qry)
    # stream形式でChatAIからのレスポンスを出力
    response.print_response_stream()


def load_from_storage():
    """
    作成済みのインデックスを読み込む関数
    """
    storage_context = StorageContext.from_defaults(persist_dir=index_json)
    index = load_index_from_storage(storage_context)
    return index


def query(query_engine, query: str) -> str:
    """
    クエリを投げた結果を返す関数
    """
    response = query_engine.query(query)
    return response


if __name__ == '__main__':
    main()
