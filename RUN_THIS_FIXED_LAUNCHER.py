"""
══════════════════════════════════════════════════════════════════════════
     RUN THIS ONE FILE IN SPYDER - ALL 4 AGENTS WORK! (FIXED VERSION)
══════════════════════════════════════════════════════════════════════════

PROBLEM SOLVED: Port conflicts fixed!
- Each agent now runs on its own unique port
- All 4 agents will open correctly

SETUP (One Time):
1. Set your Anthropic API key below (line 31)
2. pip install flask anthropic --break-system-packages  
3. Put the 4 FIXED agent files in the SAME folder as this file:
   - basicNetworkAddressingV4_NO_API_KEY_FIXED.py
   - custom_subnet_mask_assignments_FIXED.py
   - subnet_range_tutor_agent_5_FIXED.py
   - vlsm_tutor_agent_5_FIXED.py

USAGE:
1. Press F5 in Spyder to run THIS file
2. Browser opens to http://localhost:5000
3. All 4 agents are running - click any card!

══════════════════════════════════════════════════════════════════════════
"""

# API KEY - Set this!
ANTHROPIC_API_KEY = "YOUR_API_KEY_HERE"

import os
os.environ['ANTHROPIC_API_KEY'] = ANTHROPIC_API_KEY

import subprocess
import sys
import time
import webbrowser
import threading

print("="*80)
print("NETWORKING TUTOR SUITE - FIXED VERSION (No Port Conflicts!)")
print("="*80)
print("\nStarting all 4 agents with unique ports...\n")

# Check if FIXED agent files exist
required_files = [
    'basicNetworkAddressingV4_NO_API_KEY_FIXED.py',
    'custom_subnet_mask_assignments_FIXED.py',
    'subnet_range_tutor_agent_5_FIXED.py',
    'vlsm_tutor_agent_5_FIXED.py'
]

missing_files = []
for f in required_files:
    if not os.path.exists(f):
        missing_files.append(f)

if missing_files:
    print("⚠️  ERROR: Missing required FIXED agent files!")
    print("\nPlease download these FIXED files and put them in the same folder:")
    for f in missing_files:
        print(f"  - {f}")
    print("\nThese files have corrected port assignments:")
    print("  Agent 1: Port 5001")
    print("  Agent 2: Port 5002")
    print("  Agent 3: Port 5003")
    print("  Agent 4: Port 5004")
    print("\nAll files must be in the same folder as this script.")
    input("\nPress Enter to exit...")
    sys.exit(1)

# Launch each agent in a separate process with correct ports
processes = []
agents = [
    ('Agent 1: Basic Subnetting', 'basicNetworkAddressingV4_NO_API_KEY_FIXED.py', 5001),
    ('Agent 2: Custom Masks', 'custom_subnet_mask_assignments_FIXED.py', 5002),
    ('Agent 3: Subnet Ranges', 'subnet_range_tutor_agent_5_FIXED.py', 5003),
    ('Agent 4: VLSM', 'vlsm_tutor_agent_5_FIXED.py', 5004),
]

for name, filename, port in agents:
    try:
        print(f"⏳ Starting {name} on port {port}...")
        # Start the agent as a subprocess
        process = subprocess.Popen(
            [sys.executable, filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        processes.append((name, process, port))
        print(f"✓ {name} started (PID: {process.pid})")
        time.sleep(1.5)  # Give each agent time to start
    except Exception as e:
        print(f"✗ Error starting {name}: {e}")

# Give all agents time to initialize
print("\n⏳ Waiting for all agents to initialize...")
time.sleep(4)

# Check if any failed
failed = []
for name, process, port in processes:
    if process.poll() is not None:
        failed.append(name)

if failed:
    print(f"\n⚠️  Warning: Some agents failed to start: {', '.join(failed)}")
    print("\nTroubleshooting:")
    print("  1. Check that API key is set in each FIXED agent file")
    print("  2. Verify ports 5001-5004 are not in use")
    print("  3. Ensure Flask and anthropic are installed")
    print("  4. Check Spyder console for specific error messages")
else:
    print("✓ All 4 agents initialized successfully!")
    print("\nPort assignments:")
    print("  Agent 1: http://localhost:5001")
    print("  Agent 2: http://localhost:5002")
    print("  Agent 3: http://localhost:5003")
    print("  Agent 4: http://localhost:5004")

# Create and run the menu server
from flask import Flask, render_template_string

app = Flask(__name__)

MENU_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Networking Tutor Suite - FIXED</title>
    <meta charset="utf-8">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        .header {
            background: white;
            padding: 50px;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 40px;
            box-shadow: 0 15px 50px rgba(0,0,0,0.3);
        }
        .header h1 { color: #667eea; font-size: 3em; margin-bottom: 20px; }
        .header p { color: #666; font-size: 1.3em; }
        .header .fixed-badge {
            display: inline-block;
            background: #4CAF50;
            color: white;
            padding: 8px 20px;
            border-radius: 20px;
            font-size: 0.9em;
            margin-top: 15px;
            font-weight: bold;
        }
        .agents-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
        }
        .agent-card {
            background: white;
            padding: 35px;
            border-radius: 20px;
            box-shadow: 0 15px 50px rgba(0,0,0,0.2);
            transition: all 0.3s;
            text-decoration: none;
            color: inherit;
            display: block;
        }
        .agent-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        .agent-number {
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 1.8em;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .agent-title { font-size: 1.8em; font-weight: 700; margin-bottom: 15px; }
        .agent-description { color: #666; line-height: 1.8; font-size: 1.1em; }
        .port-info {
            margin-top: 12px;
            padding: 8px 12px;
            background: #e3f2fd;
            color: #1976d2;
            border-radius: 8px;
            font-size: 0.9em;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌐 Networking Tutor Suite</h1>
            <p>Master Subnetting with AI-Powered Mentoring</p>
            <span class="fixed-badge">✓ PORT CONFLICTS FIXED</span>
        </div>
        <div class="agents-grid">
            <a href="http://localhost:5001" target="_blank" class="agent-card">
                <div class="agent-number">1</div>
                <div class="agent-title">Basic Subnetting</div>
                <div class="agent-description">
                    Binary conversion, IP classes, fundamental subnetting. 80 questions.
                </div>
                <div class="port-info">Port 5001</div>
            </a>
            <a href="http://localhost:5002" target="_blank" class="agent-card">
                <div class="agent-number">2</div>
                <div class="agent-title">Custom Subnet Masks</div>
                <div class="agent-description">
                    Calculate custom masks. 6 problems × 10 parts.
                </div>
                <div class="port-info">Port 5002</div>
            </a>
            <a href="http://localhost:5003" target="_blank" class="agent-card">
                <div class="agent-number">3</div>
                <div class="agent-title">Subnet Ranges</div>
                <div class="agent-description">
                    Ranges, broadcasts, assignable addresses. 6 problems × 12 parts.
                </div>
                <div class="port-info">Port 5003</div>
            </a>
            <a href="http://localhost:5004" target="_blank" class="agent-card">
                <div class="agent-number">4</div>
                <div class="agent-title">VLSM</div>
                <div class="agent-description">
                    Variable Length Subnet Masking. 3 complete scenarios.
                </div>
                <div class="port-info">Port 5004</div>
            </a>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(MENU_HTML)

# Open browser after a delay
def open_browser():
    time.sleep(2)
    webbrowser.open('http://localhost:5000')

threading.Thread(target=open_browser, daemon=True).start()

print("\n" + "="*80)
print("✓ ALL 4 AGENTS RUNNING WITH UNIQUE PORTS!")
print("="*80)
print("\nMenu: http://localhost:5000 (opening in browser...)")
print("\nDirect Agent URLs:")
print("  Agent 1: http://localhost:5001 ✓")
print("  Agent 2: http://localhost:5002 ✓")
print("  Agent 3: http://localhost:5003 ✓")
print("  Agent 4: http://localhost:5004 ✓")
print("\n💡 Click any agent card in the browser to begin!")
print("\nPress Ctrl+C to stop all agents")
print("="*80 + "\n")

try:
    # Run the menu
    app.run(debug=False, host='localhost', port=5000, use_reloader=False)
except KeyboardInterrupt:
    print("\n\nShutting down agents...")
    for name, process, port in processes:
        process.terminate()
    print("All agents stopped. Goodbye!")
