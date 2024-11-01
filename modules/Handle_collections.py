import chromadb
import os
base_dir = os.path.dirname(os.path.abspath(__file__))
path = r'chroma_collections'
collection_dir = os.path.join(base_dir, path)


class Chroma_collections:

    def create_ids(self, docs):
        list_id = []
        for i in range(len(docs)):
            list_id.append(f"doc_id - {i}")

        # print(list_id)

        return list_id
    


    def create_chroma_collection(self, docs, collection_name):
        print("In create_chroma_collection")

        ids_list = self.create_ids(docs = docs)
        for i in docs:
            print("*"*10)
            print(i)

        
        Myclient = chromadb.PersistentClient(path=collection_dir)
        try:

            collection = Myclient.create_collection(f"{collection_name}")
            #adding the data in collection
            collection.upsert(
                documents=docs, #list of chunks
                ids=ids_list  #list of id
                )

            print(f"------------Collections created successfully-------------- : {collection_name}")

            return collection_name

        except Exception as e:
            print(e)


    
    def get_items(self, collection_name):

        docs = []
        Myclient = chromadb.PersistentClient(path=collection_dir)

        collection = Myclient.get_collection(f"{collection_name}")
        items = collection.get()
        
        print("len of items >>",len(items['documents']))

        # print(items)

        items = items['documents']

        # return items
        # for i in range(len(items)):
        #     text = items[i]
        #     docs.append(text)

        return items
