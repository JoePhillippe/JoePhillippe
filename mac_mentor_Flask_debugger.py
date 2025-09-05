from flask import Flask, render_template_string, request, jsonify
import anthropic
import os
from dotenv import load_dotenv
import traceback
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

print("🔍 DEBUG: Starting Flask app...")
print(f"🔍 DEBUG: API Key exists: {bool(os.getenv('ANTHROPIC_API_KEY'))}")
print(f"🔍 DEBUG: API Key length: {len(os.getenv('ANTHROPIC_API_KEY', '')) if os.getenv('ANTHROPIC_API_KEY') else 0}")

# Get API key from environment variable
try:
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    print("✅ DEBUG: Anthropic client created successfully")
except Exception as e:
    print(f"❌ DEBUG: Error creating Anthropic client: {e}")
    client = None

app = Flask(__name__)

def mac_mentor_bot(message):
    """MACMentor 1.0 - Your network study buddy"""
    print(f"🔍 DEBUG: Received message: {message}")
    
    if not client:
        raise Exception("Anthropic client not initialized")
    
    system_prompt = """
    PERSONA: You are MACMentor, a fellow student in Network 101 class who's really enthusiastic about network addressing.
    
    PURPOSE: Help other students understand and validate Media Access Control (MAC) addresses and hexadecimal numbers.
    
    Always check if given strings are valid MAC addresses (12 hex digits) and explain your reasoning clearly.
    """
    
    print("🔍 DEBUG: Making API call to Anthropic...")
    
    response = client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=1000,
        system=system_prompt,
        messages=[
            {"role": "user", "content": message}
        ]
    )
    
    print("✅ DEBUG: API call successful")
    result = response.content[0].text
    print(f"🔍 DEBUG: Response length: {len(result)} characters")
    
    return result

# HTML template with better error display
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MACMentor Bot - Debug Version</title>
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
        .error-message {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
            margin-right: 50px;
        }
        .debug-message {
            background-color: #fff3cd;
            color: #856404;
            border: 1px solid #ffeaa7;
            margin-right: 50px;
            font-family: monospace;
            font-size: 12px;
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
        #send-btn:disabled {
            background-color: #6c757d;
            cursor: not-allowed;
        }
        .loading {
            display: none;
            color: #666;
            font-style: italic;
        }
        .test-buttons {
            margin-bottom: 20px;
        }
        .test-btn {
            margin: 5px;
            padding: 8px 12px;
            background-color: #28a745;
            color: white;
            border: none;
            border-radius: 3px;
            cursor: pointer;
        }
        .test-btn:hover {
            background-color: #218838;
        }
        .status {
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 5px;
            font-weight: bold;
        }
        .status.ok {
            background-color: #d4edda;
            color: #155724;
        }
        .status.error {
            background-color: #f8d7da;
            color: #721c24;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🖥️ MACMentor Bot - Debug Version</h1>
        
        <div id="status" class="status">🔍 Checking connection...</div>
        
        <div class="test-buttons">
            <button class="test-btn" onclick="testConnection()">🔧 Test API Connection</button>
            <button class="test-btn" onclick="testInput('Is E0-73-E7-11-DC-2A valid?')">🧪 Test MAC Question</button>
            <button class="test-btn" onclick="clearChat()">🗑️ Clear Chat</button>
        </div>
        
        <div id="chat-box" class="chat-box">
            <div class="message bot-message">
                <strong>MACMentor:</strong> Hello! I'm ready to help with MAC address validation. Click "Test API Connection" first to verify everything is working.
            </div>
        </div>
        
        <div class="loading" id="loading">🤖 MACMentor is thinking...</div>
        
        <div class="input-area">
            <input type="text" id="user-input" placeholder="Enter your message or MAC address..." onkeypress="handleKeyPress(event)">
            <button id="send-btn" onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        let messageCount = 0;

        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        function testInput(text) {
            document.getElementById('user-input').value = text;
            sendMessage();
        }

        function clearChat() {
            document.getElementById('chat-box').innerHTML = `
                <div class="message bot-message">
                    <strong>MACMentor:</strong> Chat cleared. Ready for new questions!
                </div>
            `;
            messageCount = 0;
        }

        function addMessage(message, type) {
            const chatBox = document.getElementById('chat-box');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message ' + type;
            
            const timestamp = new Date().toLocaleTimeString();
            
            switch(type) {
                case 'user-message':
                    messageDiv.innerHTML = `<strong>You [${timestamp}]:</strong> ${message}`;
                    break;
                case 'bot-message':
                    messageDiv.innerHTML = `<strong>MACMentor [${timestamp}]:</strong> ${message.replace(/\n/g, '<br>')}`;
                    break;
                case 'error-message':
                    messageDiv.innerHTML = `<strong>❌ ERROR [${timestamp}]:</strong> ${message}`;
                    break;
                case 'debug-message':
                    messageDiv.innerHTML = `<strong>🔍 DEBUG [${timestamp}]:</strong> ${message}`;
                    break;
            }
            
            chatBox.appendChild(messageDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
            messageCount++;
        }

        async function testConnection() {
            addMessage('Testing API connection...', 'debug-message');
            
            try {
                const response = await fetch('/test', {
                    method: 'GET',
                });
                
                const data = await response.json();
                
                if (data.status === 'ok') {
                    addMessage('✅ API connection successful!', 'debug-message');
                    document.getElementById('status').textContent = '✅ API Connected';
                    document.getElementById('status').className = 'status ok';
                } else {
                    addMessage('❌ API connection failed: ' + data.error, 'error-message');
                    document.getElementById('status').textContent = '❌ API Error';
                    document.getElementById('status').className = 'status error';
                }
                
            } catch (error) {
                addMessage('❌ Network error: ' + error.message, 'error-message');
                document.getElementById('status').textContent = '❌ Network Error';
                document.getElementById('status').className = 'status error';
            }
        }

        async function sendMessage() {
            const input = document.getElementById('user-input');
            const message = input.value.trim();
            
            if (!message) return;
            
            // Add user message to chat
            addMessage(message, 'user-message');
            input.value = '';
            
            // Show loading
            document.getElementById('loading').style.display = 'block';
            document.getElementById('send-btn').disabled = true;
            
            addMessage(`Sending request to server... (Message #${messageCount + 1})`, 'debug-message');
            
            try {
                const startTime = Date.now();
                
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message }),
                });
                
                const endTime = Date.now();
                addMessage(`Server responded in ${endTime - startTime}ms`, 'debug-message');
                
                const data = await response.json();
                
                if (data.error) {
                    addMessage('Server error: ' + data.error, 'error-message');
                } else {
                    addMessage(data.response, 'bot-message');
                    addMessage(`Response received successfully (${data.response.length} characters)`, 'debug-message');
                }
                
            } catch (error) {
                addMessage('❌ Request failed: ' + error.message, 'error-message');
            }
            
            // Hide loading
            document.getElementById('loading').style.display = 'none';
            document.getElementById('send-btn').disabled = false;
        }

        // Test connection on page load
        window.addEventListener('load', function() {
            setTimeout(testConnection, 1000);
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    print("🔍 DEBUG: Home page requested")
    return render_template_string(HTML_TEMPLATE)

@app.route('/test', methods=['GET'])
def test_connection():
    """Test endpoint to verify API connectivity"""
    print("🔍 DEBUG: Test endpoint called")
    
    try:
        if not client:
            return jsonify({'status': 'error', 'error': 'Anthropic client not initialized'})
        
        # Simple test message
        print("🔍 DEBUG: Testing with simple message...")
        response = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=50,
            system="You are a test bot. Respond with exactly: 'Test successful!'",
            messages=[
                {"role": "user", "content": "test"}
            ]
        )
        
        result = response.content[0].text
        print(f"✅ DEBUG: Test response: {result}")
        
        return jsonify({'status': 'ok', 'test_response': result})
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ DEBUG: Test failed: {error_msg}")
        print(f"❌ DEBUG: Full traceback:\n{traceback.format_exc()}")
        return jsonify({'status': 'error', 'error': error_msg})

@app.route('/chat', methods=['POST'])
def chat():
    print("🔍 DEBUG: Chat endpoint called")
    
    try:
        data = request.get_json()
        print(f"🔍 DEBUG: Received data: {data}")
        
        message = data.get('message', '')
        
        if not message:
            print("❌ DEBUG: No message provided")
            return jsonify({'error': 'No message provided'})
        
        print(f"🔍 DEBUG: Processing message: '{message}'")
        
        # Get response from the bot
        bot_response = mac_mentor_bot(message)
        
        print(f"✅ DEBUG: Bot response ready, length: {len(bot_response)}")
        
        return jsonify({'response': bot_response})
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ DEBUG: Chat error: {error_msg}")
        print(f"❌ DEBUG: Full traceback:\n{traceback.format_exc()}")
        return jsonify({'error': error_msg})

if __name__ == '__main__':
    print("🚀 Starting MACMentor Debug Web Interface...")
    print("📍 Open your browser and go to: http://localhost:5000")
    print("🔍 Watch this console for debug messages...")
    app.run(debug=True, host='localhost', port=5000)