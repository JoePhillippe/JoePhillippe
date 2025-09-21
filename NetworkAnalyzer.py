from flask import Flask, render_template_string, request, jsonify
import anthropic
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

app = Flask(__name__)

def network_address_validator(message):
    """NetworkValidator 2.0 - Your comprehensive network address study buddy"""
    system_prompt = """
    PERSONA: You are NetworkValidator, an enthusiastic network student who helps classmates validate and understand network addresses.
    
    PURPOSE: Help students identify and validate MAC addresses, IPv4 addresses, and IPv6 addresses. For each input:
    
    1. IDENTIFY what type of address it appears to be (MAC, IPv4, or IPv6)
    2. VALIDATE if it's correctly formatted
    3. If INVALID, explain what's wrong and what it looks like it was trying to be
    4. If VALID, confirm it and explain key characteristics
    
    VALIDATION RULES:
    - MAC Address: 12 hexadecimal digits (0-9, A-F), usually separated by colons, hyphens, or dots
      Format examples: 00:1A:2B:3C:4D:5E, 00-1A-2B-3C-4D-5E, 001A.2B3C.4D5E
    - IPv4: 4 decimal numbers (0-255) separated by dots
      Format: xxx.xxx.xxx.xxx (each xxx must be 0-255)
    - IPv6: 8 groups of 4 hexadecimal digits separated by colons, allows compression with ::
      Format examples: 2001:0db8:85a3:0000:0000:8a2e:0370:7334, 2001:db8::1
    
    RESPONSE STYLE:
    - Be encouraging and educational
    - Clearly state what type of address it is (or appears to be)
    - If invalid, suggest what might have been intended
    - Give brief explanations of formatting rules
    - Use examples to illustrate correct formats
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
    <title>NetworkValidator Bot - Address Validation Tool</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .header {
            text-align: center;
            margin-bottom: 25px;
            padding-bottom: 20px;
            border-bottom: 3px solid #667eea;
        }
        .header h1 {
            color: #333;
            margin-bottom: 10px;
        }
        .header p {
            color: #666;
            font-size: 16px;
        }
        .chat-box {
            height: 450px;
            overflow-y: auto;
            border: 2px solid #e0e0e0;
            padding: 20px;
            margin-bottom: 20px;
            background-color: #fafafa;
            border-radius: 10px;
        }
        .message {
            margin-bottom: 15px;
            padding: 12px;
            border-radius: 8px;
            line-height: 1.5;
        }
        .user-message {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            text-align: right;
            margin-left: 60px;
        }
        .bot-message {
            background-color: #f0f0f0;
            color: #333;
            margin-right: 60px;
            border-left: 4px solid #667eea;
        }
        .input-area {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        #user-input {
            flex: 1;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        #user-input:focus {
            border-color: #667eea;
            outline: none;
        }
        #send-btn {
            padding: 12px 24px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            transition: transform 0.2s;
        }
        #send-btn:hover {
            transform: translateY(-1px);
        }
        #send-btn:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }
        .loading {
            display: none;
            color: #667eea;
            font-style: italic;
            text-align: center;
            padding: 10px;
        }
        .examples {
            margin-top: 20px;
            padding: 20px;
            background: linear-gradient(135deg, #e3f2fd, #f3e5f5);
            border-radius: 10px;
            border: 1px solid #e0e0e0;
        }
        .examples h3 {
            margin-top: 0;
            color: #333;
            text-align: center;
        }
        .example-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }
        .example-category {
            background: white;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #ddd;
        }
        .example-category h4 {
            margin: 0 0 10px 0;
            color: #667eea;
            font-size: 14px;
            font-weight: bold;
        }
        .example {
            cursor: pointer;
            color: #0066cc;
            text-decoration: underline;
            margin: 5px 0;
            font-size: 13px;
            display: block;
            padding: 3px;
            border-radius: 3px;
            transition: background-color 0.2s;
        }
        .example:hover {
            background-color: #f0f8ff;
            color: #0052a3;
        }
        .stats {
            display: flex;
            justify-content: space-around;
            margin: 20px 0;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
        }
        .stat {
            text-align: center;
        }
        .stat-number {
            font-size: 24px;
            font-weight: bold;
            color: #667eea;
        }
        .stat-label {
            font-size: 12px;
            color: #666;
            text-transform: uppercase;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌐 NetworkValidator Bot</h1>
            <p>Validate MAC, IPv4, and IPv6 addresses with instant feedback and learning tips!</p>
        </div>
        
        <div class="stats">
            <div class="stat">
                <div class="stat-number" id="mac-count">0</div>
                <div class="stat-label">MAC Tests</div>
            </div>
            <div class="stat">
                <div class="stat-number" id="ipv4-count">0</div>
                <div class="stat-label">IPv4 Tests</div>
            </div>
            <div class="stat">
                <div class="stat-number" id="ipv6-count">0</div>
                <div class="stat-label">IPv6 Tests</div>
            </div>
        </div>
        
        <div id="chat-box" class="chat-box">
            <div class="message bot-message">
                <strong>NetworkValidator:</strong> Hello! I'm here to help you validate network addresses. Send me any MAC address, IPv4 address, or IPv6 address and I'll tell you if it's valid, what type it is, and help you understand any errors. Try the examples below to get started!
            </div>
        </div>
        
        <div class="loading" id="loading">🤖 NetworkValidator is analyzing your address...</div>
        
        <div class="input-area">
            <input type="text" id="user-input" placeholder="Enter a MAC, IPv4, or IPv6 address..." onkeypress="handleKeyPress(event)">
            <button id="send-btn" onclick="sendMessage()">Validate</button>
        </div>
        
        <div class="examples">
            <h3>Try These Examples</h3>
            <div class="example-grid">
                <div class="example-category">
                    <h4>✅ Valid MAC Addresses</h4>
                    <span class="example" onclick="setInput('00:1A:2B:3C:4D:5E')">00:1A:2B:3C:4D:5E</span>
                    <span class="example" onclick="setInput('E0-73-E7-11-DC-2A')">E0-73-E7-11-DC-2A</span>
                    <span class="example" onclick="setInput('001A.2B3C.4D5E')">001A.2B3C.4D5E</span>
                </div>
                
                <div class="example-category">
                    <h4>❌ Invalid MAC Addresses</h4>
                    <span class="example" onclick="setInput('XY:ZZ:11:22:33:44')">XY:ZZ:11:22:33:44</span>
                    <span class="example" onclick="setInput('00:1A:2B:3C:4D')">00:1A:2B:3C:4D</span>
                    <span class="example" onclick="setInput('GG:HH:II:JJ:KK:LL')">GG:HH:II:JJ:KK:LL</span>
                </div>
                
                <div class="example-category">
                    <h4>✅ Valid IPv4 Addresses</h4>
                    <span class="example" onclick="setInput('192.168.1.1')">192.168.1.1</span>
                    <span class="example" onclick="setInput('10.0.0.255')">10.0.0.255</span>
                    <span class="example" onclick="setInput('172.16.254.1')">172.16.254.1</span>
                </div>
                
                <div class="example-category">
                    <h4>❌ Invalid IPv4 Addresses</h4>
                    <span class="example" onclick="setInput('192.168.1.256')">192.168.1.256</span>
                    <span class="example" onclick="setInput('10.0.0')">10.0.0</span>
                    <span class="example" onclick="setInput('999.999.999.999')">999.999.999.999</span>
                </div>
                
                <div class="example-category">
                    <h4>✅ Valid IPv6 Addresses</h4>
                    <span class="example" onclick="setInput('2001:0db8:85a3:0000:0000:8a2e:0370:7334')">2001:0db8:85a3::8a2e:0370:7334</span>
                    <span class="example" onclick="setInput('2001:db8::1')">2001:db8::1</span>
                    <span class="example" onclick="setInput('::1')">::1</span>
                </div>
                
                <div class="example-category">
                    <h4>❌ Invalid IPv6 Addresses</h4>
                    <span class="example" onclick="setInput('2001:0db8:85a3::8a2e::7334')">2001:0db8:85a3::8a2e::7334</span>
                    <span class="example" onclick="setInput('gggg::1')">gggg::1</span>
                    <span class="example" onclick="setInput('2001:db8:85a3:0000:0000:8a2e:0370:7334:extra')">...too many groups</span>
                </div>
            </div>
        </div>
    </div>

    <script>
        let messageCount = 0;
        let macCount = 0;
        let ipv4Count = 0;
        let ipv6Count = 0;

        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        function setInput(text) {
            document.getElementById('user-input').value = text;
            document.getElementById('user-input').focus();
        }

        function updateStats(message) {
            // Simple heuristic to categorize the message
            if (message.includes(':') && (message.includes('::') || message.split(':').length > 4)) {
                ipv6Count++;
                document.getElementById('ipv6-count').textContent = ipv6Count;
            } else if (message.includes('.') && message.split('.').length === 4) {
                ipv4Count++;
                document.getElementById('ipv4-count').textContent = ipv4Count;
            } else if (message.includes(':') || message.includes('-')) {
                macCount++;
                document.getElementById('mac-count').textContent = macCount;
            }
        }

        function addMessage(message, isUser) {
            const chatBox = document.getElementById('chat-box');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message ' + (isUser ? 'user-message' : 'bot-message');
            
            const timestamp = new Date().toLocaleTimeString();
            
            if (isUser) {
                messageDiv.innerHTML = '<strong>You [' + timestamp + ']:</strong> ' + message;
                updateStats(message);
            } else {
                messageDiv.innerHTML = '<strong>NetworkValidator [' + timestamp + ']:</strong> ' + message.replace(/\\n/g, '<br>');
            }
            
            chatBox.appendChild(messageDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
            messageCount++;
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
            
            // Focus back on input
            document.getElementById('user-input').focus();
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
        bot_response = network_address_validator(message)
        
        return jsonify({'response': bot_response})
        
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    print("🚀 Starting NetworkValidator Web Interface...")
    print("🌐 Validates MAC, IPv4, and IPv6 addresses")
    print("🔍 Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='localhost', port=5001)

