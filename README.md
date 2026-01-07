In this project i made an Agentic AI that uses gemini as its mind.

In counterbot.py we have is it counts how many  question the user asks and when the count
reaches 5 it randomly pick one of those 5 questions randomly and creates a quiz question 
from that and then reset the counter and continue again.

How to run this code?
run this in terminal
//streamlit run counterbot.py  

We have a veery important function here in the code which tries the request, if server fails
it wiats  and tries again and if iit still fails it returns a clean message.


IN timebot.py
The code stores the query text and the exact time in format 
Example- pending_queries = [
   {"text": "What is AI?", "time": 1700000000.0}
]


Then it waits for 10 seconds and creates a quiz from the exact query and shows it 
automatically to the user.

How to run this code?
run this in terminal
//streamlit run timebot.py

