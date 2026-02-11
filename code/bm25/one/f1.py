#VSY - Twenkid
#f1.py
#date 
from datetime import datetime
current_time = datetime.now()
print(current_time)
curr = str(current_time).replace(' ', '_')
curr = curr.replace(':', '_')
curr = curr.replace('.', '-')
print(curr)

#f = open("30-10-2025_bm25.txt", "at", encoding="utf-8")
f = open("curr_"+"bm25.txt", "at", encoding="utf-8")
def save_to_file(doc,i=0,score=0,mx=0):
    f.write(f"Rank {i+1} (Score: {score:.4f})\r\n")
    f.write(f"ID: {doc['id']}\r\n")
    f.write(f"Title: {doc['title']}\r\n")
    #f.write(f"Text: {doc['text'][:600]}...")  # Print first 300 chars
    if mx != 0:
      f.write(f"Text: {doc['text'][:mx]}...")  # Print first 300 chars
    else: 
      f.write(f"Text: {doc['text']}...")  # Print first 300 chars
    f.write(f"\r\n{'-'*80}\r\n")
    f.flush()
     
