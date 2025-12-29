import lancedb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
db = lancedb.connect("./lancedb")
TABLE = "notes"

def build_semantic_index(chunks):
    vectors = model.encode(chunks, convert_to_numpy=True)

    data = [
        {"id": i, "text": chunks[i], "vector": vectors[i]}
        for i in range(len(chunks))
    ]

    if TABLE in db.table_names():
        db.drop_table(TABLE)

    db.create_table(TABLE, data=data, mode="overwrite")

def semantic_search(query, k=5):
    table = db.open_table(TABLE)
    q_vec = model.encode(query).tolist()

    results = table.search(q_vec).limit(k).to_list()
    return [r["text"] for r in results]
