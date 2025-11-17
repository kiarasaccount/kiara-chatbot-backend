*PLEASE ALSO SEE THE FRONTEND TO THIS REPOSITORY >> kiarasaccount.github.io

To see the chatbot in action, please visit >> https://kiarasaccount.github.io/ 


Below are the details of this repository, which I used to create a chatbot assistant!

A lightweight FastAPI backend that powers 'Kiara Assistant chatbot'.
It provides a simple /ask endpoint that receives a user question and returns an answer—either from a fixed knowledge base or dynamically using OpenAI’s API.

This backend is deployed on Render and used by the frontend hosted on GitHub Pages.

The features include:

- Fast & lightweight REST API

- /ask endpoint for chatbot responses

- Retrieval-based answers + optional OpenAI-powered responses

- CORS enabled for GitHub Pages

- Fully compatible with any frontend

- Deployed on Render

I set this up using Python, FastAPI, Uvicorn, OpenAI API and Render.

  
How I structured the project?

kiara-chatbot-backend/
│── main.py               # FastAPI app
│── requirements.txt      # Python dependencies
│── start.sh              # Render start script
│── README.md             # Documentation


