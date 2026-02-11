#LOAD CLAUDE 4.5 #29.10.2025
#ms1.py
#Vsy Twenkid
from pathlib import Path
import bm25s
import Stemmer
import json
from f1 import save_to_file

top_k = 10 #30-10-2025; was k=5


def pre_index(save_dir="datasets", index_dir="bm25s_indices/", dataset="nq", num_docs=100000): #10000):
    index_dir = Path(index_dir) / dataset
    index_dir.mkdir(parents=True, exist_ok=True)
    
    #Already downloaded
    #print("Downloading the dataset...")
    #bm25s.utils.beir.download_dataset(dataset, save_dir=save_dir)
    #print("Loading the corpus...")
    #corpus = bm25s.utils.beir.load_corpus(dataset, save_dir=save_dir)
    
    
    corpus = bm25s.utils.beir.load_corpus(dataset, save_dir=save_dir)

    #dataset = "nfcorpus"  # Or "msmarco", "scifact", etc.
    #save_dir = "./data"   # Your saved dir

    # Skip if already downloaded
    # download_dataset(dataset, save_dir=save_dir)
    
    print(f"Loaded {len(corpus):,} documents")
    print("Sample:", list(corpus.items())[:1])  # {doc_id: Document(id='...', title='...', body='...')}    
    # Index only part of the documents
    if num_docs!=0:
        corpus_records = [
            {"id": k, "title": v["title"], "text": v["text"]}         
            for k, v in list(corpus.items())[:num_docs]  # Take only first num_docs
        ]        
    else:
          corpus_records = [
            {"id": k, "title": v["title"], "text": v["text"]}         
            for k, v in list(corpus.items())  # Index All
        ]
    corpus_lst = [r["title"] + " " + r["text"] for r in corpus_records]
    
    print(f"Indexing {len(corpus_records)} documents...")
    
    stemmer = Stemmer.Stemmer("english")
    tokenizer = bm25s.tokenization.Tokenizer(stemmer=stemmer)
    corpus_tokens = tokenizer.tokenize(corpus_lst, return_as="tuple")
    
    retriever = bm25s.BM25()
    retriever.index(corpus_tokens)
    
    retriever.save(index_dir, corpus=corpus_records)
    tokenizer.save_vocab(index_dir)
    tokenizer.save_stopwords(index_dir)
    print(f"Saved the index to {index_dir}.")
    
    # get memory usage
    mem_use = bm25s.utils.benchmark.get_max_memory_usage()
    print(f"Peak memory usage: {mem_use:.2f} GB")
    
    # Query loop
    print("\n" + "="*80)
    print("Ready for queries! Type 'quit' or 'exit' to stop.")
    print("="*80 + "\n")

   
    
    while True:
        query = input("Enter your query: ").strip()
        
        if query.lower() in ['quit', 'exit', 'q']:
            print("Exiting...")
            break
        
        if not query:
            continue
        
        # Tokenize query
        query_tokens = tokenizer.tokenize([query], return_as="tuple")
        
        # Retrieve top-k documents
        results, scores = retriever.retrieve(query_tokens, corpus=corpus_records, k=5)
        
        print(f"\n{'='*80}")
        print(f"Query: {query}")
        print(f"{'='*80}\n")

        # Print retrieved documents
        # results[0] is a list of documents for the first query
        for i in range(len(results[0])):
            doc = results[0][i]  # This is already the document dict
            score = scores[0, i]
            
            print(f"Rank {i+1} (Score: {score:.4f})")
            print(f"ID: {doc['id']}")
            print(f"Title: {doc['title']}")
            print(f"Text: {doc['text'][:600]}...")  # Print first 300 chars
            print(f"{'-'*80}\n")
            save_to_file(doc,i,score)

        """
        # Print retrieved documents
        for i in range(results.shape[1]):
            doc_idx = results[0, i]
            score = scores[0, i]
            doc = corpus_records[doc_idx]
            
            print(f"Rank {i+1} (Score: {score:.4f})")
            print(f"ID: {doc['id']}")
            print(f"Title: {doc['title']}")
            print(f"Text: {doc['text'][:300]}...")  # Print first 300 chars
            print(f"{'-'*80}\n")
        """
        
def load_and_query(index_dir="bm25s_indices/msmarco"):
    index_dir = Path(index_dir)
    
    print(f"Loading index from {index_dir}...")
    
    # Load the saved index with corpus
    retriever = bm25s.BM25.load(index_dir, load_corpus=True)
    corpus_records = retriever.corpus
    
    # Load tokenizer
    stemmer = Stemmer.Stemmer("english")
    tokenizer = bm25s.tokenization.Tokenizer(stemmer=stemmer)
    tokenizer.load_vocab(index_dir)
    tokenizer.load_stopwords(index_dir)
    
    print(f"Loaded {len(corpus_records)} documents.")
    
    # Query loop
    print("\n" + "="*80)
    print("Ready for queries! Type 'quit' or 'exit' to stop.")
    print("="*80 + "\n")

    q_map = {}
    q_list = []
    queries_json = None
    #########
    # Load queries from queries.json
    #queries_path = Path(index_dir) / "datasets" / "queries.jsonl"
    queries_path = Path("datasets") / "msmarco" / "queries.jsonl"
    if not queries_path.exists():
        #queries_path = Path(index_dir) / "datasets" / "queries.jsonl"
        queries_path = "datasets/msmarco/queries.jsonl"

    n = 0
    # Try JSONL format first (one JSON object per line)
    try:
        with open(queries_path, 'r') as f:
            for line in f:
                if line.strip():
                    query_obj = json.loads(line)
                    if (n<20): print(query_obj)
                    #n = n + 1
                    #if n == 10: break                    
                    #queries[query_obj['_id']] = query_obj['text']
                    #q_map['_id'] = query_obj['text'] #should be the number? just the list ...
                    #q_map[query_obj['_id']] = query_obj['text'] #should be the number? just the list ...
                    #q_map[str(query_obj['_id'])] = query_obj['text'] #should be the number? just the list ...
                    q_map[str(n)] = query_obj['text'] #should be the number? just the list ...
                    q_list.append(query_obj)
                    n = n + 1
                    if n%3000 == 0: print(n,end="; ")
                    if n%99000 == 0: print(n,end="\r\n")
                
    except:
        # Try regular JSON format
        with open(queries_path, 'r') as f:
            queries_json = json.load(f)

    #print(queries_json[0:20]) 
    print(q_list[0:100])
    
    print(f"Loaded {len(q_list)} queries, q_list")
    #################
    #print(q_map['6854'])
    print( list(q_map.keys())[0:100]) #['6854'])
    
    while True:
        query = input("Enter your query: ").strip()
        
        if query.lower() in ['quit', 'exit', 'q']:
            print("Exiting...")
            break
        
        if not query:
            continue
        
        # Tokenize query
        query_tokens = tokenizer.tokenize([query], return_as="tuple")
        
        # Retrieve top-k documents
        results, scores = retriever.retrieve(query_tokens, corpus=corpus_records, k=top_k)
        
        print(f"\n{'='*80}")
        print(f"Query: {query}")
        print(f"{'='*80}\n")

        print(len(q_map))
        # Print retrieved documents
        for i in range(len(results[0])):
            doc = results[0][i]
            score = scores[0, i]
            
            print(f"Rank {i+1} (Score: {score:.4f})")
            try:
              print(f"Query: {q_map[doc['id']]}")
            except:
                   pass
            print(f"ID: {doc['id']}")
            print(f"Title: {doc['title']}")
            print(f"Text: {doc['text'][:1000]}...")
            print(f"{'-'*80}\n")
            save_to_file(doc,i,score)

if __name__ == "__main__":
    # First time: index and save
    # main(dataset='msmarco', num_docs=10000)
    
    # Subsequent times: just load and query
    #pre_index(save_dir="datasets", index_dir="bm25s_indices/", dataset="msmarco", num_docs=1000000) #10000, 100000 
    
    #pre_index(save_dir="datasets", index_dir="bm25s_indices/", dataset="msmarco", num_docs=0) #10000, 100000 
    #already indexed all - just load , 15.1.2026
    load_and_query(index_dir="bm25s_indices/msmarco")
