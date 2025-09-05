from flask import Flask, render_template_string, request, jsonify
import anthropic
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

app = Flask(__name__)

def mac_mentor_bot(message):
    """MACMentor 1.0 - Your network study buddy"""
    system_prompt = """
    PERSONA: You are MACMentor, a fellow student in Network 101 class who's really enthusiastic about network addressing.
    
    PURPOSE: Help other students understand and validate Media Access Control (MAC) addresses and hexadecimal numbers.
    
    Always check if given strings are valid MAC addresses (12 hex digits) and explain your reasoning clearly.
    """
    
    response = client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=1000,
        system=system_prompt,
        messages=[
            {"role": "user", "content": message}
        ]
    )
    return response.content[0].text

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MACMentor Bot - Web Interface</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .chat-box {
            height: 400px;
            overflow-y: auto;
            border: 1px solid #ddd;
            padding: 15px;
            margin-bottom: 20px;
            background-color: #fafafa;
            border-radius: 5px;
        }
        .message {
            margin-bottom: 15px;
            padding: 10px;
            border-radius: 5px;
        }
        .user-message {
            background-color: #007bff;
            color: white;
            text-align: right;
            margin-left: 50px;
        }
        .bot-message {
            background-color: #e9ecef;
            color: #333;
            margin-right: 50px;
        }
        .input-area {
            display: flex;
            gap: 10px;
        }
        #user-input {
            flex: 1;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }
        #send-btn {
            padding: 10px 20px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        #send-btn:hover {
            background-color: #0056b3;
        }
        .loading {
            display: none;
            color: #666;
            font-style: italic;
        }
        .examples {
            margin-top: 20px;
            padding: 15px;
            background-color: #e7f3ff;
            border-radius: 5px;
        }
        .example {
            cursor: pointer;
            color: #0066cc;
            text-decoration: underline;
            margin: 5px 0;
        }
        .example:hover {
            color: #0052a3;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🖥️ MACMentor Bot - Web Interface</h1>
        <p>Test your MAC address validation bot in the browser!</p>
        
        <div id="chat-box" class="chat-box">
            <div class="message bot-message">
                <strong>MACMentor:</strong> Hello! I'm here to help you with MAC addresses and hex validation. Send me a MAC address to check!
            </div>
        </div>
        
        <div class="loading" id="loading">MACMentor is thinking...</div>
        
        <div class="input-area">
            <input type="text" id="user-input" placeholder="Enter your message or MAC address..." onkeypress="handleKeyPress(event)">
            <button id="send-btn" onclick="sendMessage()">Send</button>
        </div>
        
        <div class="examples">
            <strong>Try these examples:</strong><br>
            <div class="example" onclick="setInput('Is E0-73-E7-11-DC-2A a valid MAC address?')">Is E0-73-E7-11-DC-2A a valid MAC address?</div>
            <div class="example" onclick="setInput('Check this: 00:1A:2B:3C:4D:5E')">Check this: 00:1A:2B:3C:4D:5E</div>
            <div class="example" onclick="setInput('Is XY-ZZ-11-22-33-44 valid?')">Is XY-ZZ-11-22-33-44 valid?</div>
            <div class="example" onclick="setInput('What makes a valid MAC address?')">What makes a valid MAC address?</div>
        </div>
    </div>

    <script>
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        function setInput(text) {
            document.getElementById('user-input').value = text;
        }

        function addMessage(message, isUser) {
            const chatBox = document.getElementById('chat-box');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message ' + (isUser ? 'user-message' : 'bot-message');
            
            if (isUser) {
                messageDiv.innerHTML = '<strong>You:</strong> ' + message;
            } else {
                messageDiv.innerHTML = '<strong>MACMentor:</strong> ' + message.replace(/\n/g, '<br>');
            }
            
            chatBox.appendChild(messageDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        async function sendMessage() {
            const input = document.getElementById('user-input');
            const message = input.value.trim();
            
            if (!message) return;
            
            // Add user message to chat
            addMessage(message, true);
            input.value = '';
            
            // Show loading
            document.getElementById('loading').style.display = 'block';
            document.getElementById('send-btn').disabled = true;
            
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message }),
                });
                
                const data = await response.json();
                
                if (data.error) {
                    addMessage('Error: ' + data.error, false);
                } else {
                    addMessage(data.response, false);
                }
                
            } catch (error) {
                addMessage('Error connecting to server: ' + error.message, false);
            }
            
            // Hide loading
            document.getElementById('loading').style.display = 'none';
            document.getElementById('send-btn').disabled = false;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'No message provided'})
        
        # Get response from the bot
        bot_response = mac_mentor_bot(message)
        
        return jsonify({'response': bot_response})
        
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    print("Starting MACMentor Web Interface...")
    print("Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='localhost', port=5000)
