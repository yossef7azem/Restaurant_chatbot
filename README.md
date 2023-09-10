# Restaurant_chatbot
A restaurant chatbot using Dialogflow and a backend. The chatbot allows users to order food, track their orders, and get information about the restaurant. I used the following technologies in my project:

1-Dialogflow: A natural language processing (NLP) platform that allows you to build chatbots.

2-FastAPI: A modern, high-performance web framework.

3-MySQL: A relational database management system.



Intents and Contexts in Dialogflow:

Intents are the actions that a chatbot can take. For example, the "order food" intent tells the chatbot to ask the user what they want to order. Contexts are used to track the conversation between the user and the chatbot. For example, the "ongoing-order" context is used to track the user's current order.



Backend:

The backend is responsible for storing and processing the data for the chatbot. I used MySQL to store the user's orders and the chatbot's responses. I used FastAPI to create a RESTful API that the chatbot can use to access the data.



NLP Techniques:

I used a number of NLP techniques in my project, including:

Tokenization: This is the process of breaking down text into individual words or phrases.

Stemming: This is the process of reducing a word to its root form.

Lemmatization: This is the process of grouping together words that have the same meaning.
