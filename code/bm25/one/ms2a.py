#LOAD CLAUDE 4.5 #29.10.2025 - earlier experiments, Wikipedia etc. Colab?
#VSY - Twenkid 
#https://github.com/Twenkid/Vsy-Jack-Of-All-Trades-AGI-Bulgarian-Internet-Archive-And-Search-Engine/
#ms1.py
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
    
    
    #CLAUDE BEGIN
    
    # Load queries
    queries = {}
    queries_path = Path("datasets") / "msmarco" / "queries.jsonl"
    
    with open(queries_path, 'r') as f:
        for line in f:
            if line.strip():
                query_obj = json.loads(line)
                queries[query_obj['_id']] = query_obj['text']
    
    print(f"Loaded {len(queries)} queries")
    
    # Load qrels (query-document relevance judgments)
    # This tells you which documents are relevant for each query
    qrels = {}
    qrels_path = Path("datasets") / "msmarco" / "qrels" / "test.tsv"
    
    if qrels_path.exists():
        with open(qrels_path, 'r') as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 3:
                    query_id, doc_id = parts[0], parts[2]
                    
                    #+
                    #d_id, q_id = query_id, doc_id
                    #dmap[d_id] = q_id  -- there could be several
                    
                    if query_id not in qrels:
                        qrels[query_id] = []
                    qrels[query_id].append(doc_id)
        print(f"Loaded qrels for {len(qrels)} queries")
    
    
    
    # Load queries #17-1-2026
    queries = {}
    queries_path = Path("datasets") / "msmarco" / "queries.jsonl"

    with open(queries_path, 'r') as f:
            for line in f:
                        if line.strip():
                            query_obj = json.loads(line)
                            queries[query_obj['_id']] = query_obj['text']                                                                                                                                                          
                            print(f"Loaded {len(queries)} queries")
							# Load qrels and create reverse mapping: doc_id -> list of query_ids
    
    doc_to_queries = {}  # Maps document IDs to list of query IDs that consider them relevant
    qrels_path = Path("datasets") / "msmarco" / "qrels" / "test.tsv"
    n=0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
    if qrels_path.exists():
      with open(qrels_path, 'r') as f:
         for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 3:
               query_id, doc_id = parts[0], parts[2]
               print(query_id, doc_id)
               if doc_id not in doc_to_queries:
                   doc_to_queries[doc_id] = []                                                                                                                                                                                                                                                                                                                    
               doc_to_queries[doc_id].append(query_id)                                                                                                                                                                                                                                                                                                                                           
               #print(queries[query_id]) ##     
               #print(doc[doc_id][0:100]) ##  It is not retrieved yet!
         #if n%1000==0: #
         print(n, doc_to_queries[doc_id])
         n+=1
         #print(doc_to_queries[doc_id].append(query_id)                                                                                                                                                                                                                                                                                                                                           )     
    ###print(queries.keys[n])
    ####print(queries.valuess[n]) 		                                                                                                                                                                                                                                                                                                                             
               
    print(f"Loaded reverse qrels mapping for {len(doc_to_queries)} documents")                                                                                                                                                                                                                                                                                                                            
				
    #CLAUDE END
        
    #################
    #print(q_map['6854'])
    print( list(q_map.keys())[0:100]) #['6854'])
    
    while True:
        user_input = input("Enter your query: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Exiting...")
            break
        
        if not user_input:
            continue
            
        #Check if input is a query ID from the dataset
        query_text = None
        query_id = None
        
        if user_input in queries:
            query_id = user_input
            query_text = queries[user_input]
            print(f"Using query from dataset: {query_text}")
        else:
            query_text = user_input
        
        ## Tokenize query
        #query_tokens = tokenizer.tokenize([query], return_as="tuple")
        # Tokenize query
        query_tokens = tokenizer.tokenize([query_text], return_as="tuple")
        
        # Retrieve top-k documents
        results, scores = retriever.retrieve(query_tokens, corpus=corpus_records, k=top_k)
        
        print(f"\n{'='*80}")
        print(f"Query: {query_text}")
        if query_id:
            print(f"Query ID: {query_id}")
            if query_id in qrels:
                print(f"Ground truth relevant docs: {qrels[query_id]}")
        print(f"{'='*80}\n")
        
        # Print retrieved documents
        for i in range(len(results[0])):
            doc = results[0][i]
            score = scores[0, i]
            
            is_relevant = ""
            if query_id and query_id in qrels and doc['id'] in qrels[query_id]:
                is_relevant = " ✓ RELEVANT"
            
            print(f"Rank {i+1} (Score: {score:.4f}){is_relevant}")
            print(f"Doc ID: {doc['id']}")
            print(f"Title: {doc['title']}")
            print(f"Text: {doc['text'][:500]}...") #:1000
            print(f"{'-'*80}\n")
            #print(doc['id'], 
            
            #Sholl relevant queries
            if doc['id'] in doc_to_queries:                
               associated_query_ids = doc_to_queries[doc['id']]
               print(f" This document is relevant to {len(associated_query_ids)} queries;")
               print(f"{'-'*80}")
               for idx, q_id in enumerate(associated_query_ids[:10],1): 
                 if q_id in queries:
                    is_current = "--< your query" if q_id == query_id else ""
                    print(f" {idx}. Query ID: {q_id}{is_current}")
                    print(f"  Query Text: {queries[q_id]}")
                 else:
                     print(f"  {idx}. Query ID: {q_id} (query text not found)")
                 print()
                 
               if len(associated_query_ids) > 10:
                  print(f" ... and {len(associated_query_ids) - 10} more queries")
               else:
                   print(f" No ground truth queries found for this document")
               print(f"{'='*80}\n")                                                                                                                                            
            else: print("No  if doc['id'] in doc_to_queries:   ")
                  
            save_to_file(doc, i, score)
            
            
        """
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
        """


if __name__ == "__main__":
    # First time: index and save
    # main(dataset='msmarco', num_docs=10000)
    
    # Subsequent times: just load and query
    #pre_index(save_dir="datasets", index_dir="bm25s_indices/", dataset="msmarco", num_docs=1000000) #10000, 100000 
    
    #pre_index(save_dir="datasets", index_dir="bm25s_indices/", dataset="msmarco", num_docs=0) #10000, 100000 
    #already indexed all - just load , 15.1.2026
    load_and_query(index_dir="bm25s_indices/msmarco")
