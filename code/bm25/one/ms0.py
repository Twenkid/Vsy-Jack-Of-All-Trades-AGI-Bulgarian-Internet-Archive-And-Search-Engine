#ms0.py
#Vsy Twenkid
from pathlib import Path
import bm25s
import Stemmer
from f1 import save_to_file

def main(save_dir="datasets", index_dir="bm25s_indices/", dataset="nq", num_docs=1000): #10000):
    index_dir = Path(index_dir) / dataset
    index_dir.mkdir(parents=True, exist_ok=True)
    
    print("Downloading the dataset...")
    bm25s.utils.beir.download_dataset(dataset, save_dir=save_dir)
    print("Loading the corpus...")
    corpus = bm25s.utils.beir.load_corpus(dataset, save_dir=save_dir)
    
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

if __name__ == "__main__":
    num = 0 #all
    #main(dataset='msmarco', num_docs=10000)  # Index only 10k documents
    #main(dataset='msmarco', num_docs=num)  # Index only 10k documents
    main(dataset='msmarco') #, num_docs=num)  # Index only 10k documents
