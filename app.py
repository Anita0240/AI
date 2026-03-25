# from flask import Flask,request,render_template
# import numpy as np
# import pandas as pd

# from sklearn.preprocessing import StandardScaler
# from src.pipeline.predict_pipeline import CustomData,PredictPipeline

# application=Flask(__name__)

# app=application

# ## Route for a home page

# @app.route('/')
# def index():
#     return render_template('index.html') 

# @app.route('/predictdata',methods=['GET','POST'])
# def predict_datapoint():
#     if request.method=='GET':
#         return render_template('home.html')
#     else:
#         data=CustomData(
#             gender=request.form.get('gender'),
#             race_ethnicity=request.form.get('ethnicity'),
#             parental_level_of_education=request.form.get('parental_level_of_education'),
#             lunch=request.form.get('lunch'),
#             test_preparation_course=request.form.get('test_preparation_course'),
#             reading_score=float(request.form.get('writing_score')),
#             writing_score=float(request.form.get('reading_score'))

#         )
#         pred_df=data.get_data_as_data_frame()
#         print(pred_df)
#         print("Before Prediction")

#         predict_pipeline=PredictPipeline()
#         print("Mid Prediction")
#         results=predict_pipeline.predict(pred_df)
#         print("after Prediction")
#         return render_template('home.html',results=results[0])
    

# if __name__=="__main__":
#     app.run(host="0.0.0.0", debug=True)       
import os
from flask import Flask, request, jsonify
from google import genai
from dotenv import load_dotenv


load_dotenv()
print("DEBUG API KEY:", os.getenv("GEMINI_API_KEY"))
app = Flask(__name__)


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


@app.route('/')
def home():
   
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>My AI Agent</title>
        <style>
            body { font-family: sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; line-height: 1.6; background-color: #f4f7f6; }
            #chat { border: 1px solid #ddd; height: 400px; overflow-y: scroll; padding: 15px; margin-bottom: 10px; border-radius: 8px; background: white; }
            .user-msg { color: #007bff; margin-bottom: 10px; font-weight: bold; }
            .agent-msg { color: #333; margin-bottom: 20px; background: #e9ecef; padding: 10px; border-radius: 5px; }
            input { width: 70%; padding: 12px; border: 1px solid #ccc; border-radius: 4px; }
            button { padding: 12px 20px; cursor: pointer; background: #28a745; color: white; border: none; border-radius: 4px; }
        </style>
    </head>
    <body>
        <h2>🤖 My Gemini AI Agent</h2>
        <div id="chat"></div>
        <input type="text" id="userInput" placeholder="Type your message...">
        <button onclick="sendMessage()">Send</button>

        <script>
    async function sendMessage() {
        const input = document.getElementById('userInput');
        const chat = document.getElementById('chat');
        const query = input.value;
        if (!query) return;

        // 1. Show your message in the chat
        chat.innerHTML += `<div class="user-msg"><b>You:</b> ${query}</div>`;
        input.value = '';

        try {
            // 2. Send the request to your Flask server
            const response = await fetch('/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: query })
            });

            const data = await response.json();

            // 3. CHECK: If 'response' exists, use it. Otherwise, show the 'error'.
            const agentMessage = data.response || data.error || "No response from AI.";
            chat.innerHTML += `<div class="agent-msg"><b>Agent:</b> ${agentMessage}</div>`;

        } catch (err) {
            chat.innerHTML += `<div class="agent-msg" style="color:red;"><b>Error:</b> Could not connect to server.</div>`;
        }

        // Auto-scroll to the bottom
        chat.scrollTop = chat.scrollHeight;
    }
</script>
    </body>
    </html>
    """
@app.route('/ask', methods=['POST'])
def ask_agent():
    data = request.json
    user_query = data.get("query")
    
    if not user_query:
        return jsonify({"error": "No query"}), 400

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_query
        )
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,debug=False)