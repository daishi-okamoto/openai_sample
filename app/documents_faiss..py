import os
from dotenv import load_dotenv
# 事前に.envファイルに"OPENAI_API_KEY"の環境変数を設定しておく
load_dotenv()

from llama_index import (SimpleDirectoryReader, GPTVectorStoreIndex,
                         StorageContext, load_index_from_storage)
import faiss
from llama_index.vector_stores.faiss import FaissVectorStore

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

        # Faissパッケージのインデックスを作成(L2ノルム(ユークリッド距離)の1536次元ベクトル)
        faiss_index = faiss.IndexFlatL2(1536)
        vector_store = FaissVectorStore(faiss_index=faiss_index)
        storage_context = StorageContext.from_defaults(
            vector_store=vector_store
        )

        # documents をもとに Embbeddings API を通信してベクター取得し GPTVectorStoreIndex を生成
        index = GPTVectorStoreIndex.from_documents(
            documents=documents,
            storage_context=storage_context
        )

        # # 作成したインデックスをディスクに保存
        index.storage_context.persist(persist_dir=index_json)
    else:
        # 作成済みのインデックスを読み込み
        index = load_from_storage()

    # プロンプト
    query_engine = index.as_query_engine()
    qry = ""

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


def query(query_engine, query: str) -> str:
    """
    クエリを投げた結果を返す関数
    """
    response = query_engine.query(query)
    return response


if __name__ == '__main__':
    main()
