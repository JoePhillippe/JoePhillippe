# Cisco Networking Tutoring System

An AI-powered Flask-based educational platform for teaching Cisco networking concepts through four specialized tutoring agents. Each agent provides interactive learning experiences with progressive AI hints powered by Anthropic's Claude API.

## Overview

This system consists of four independent Flask applications that work together to teach different aspects of Cisco networking:

1. **Basic Subnetting Agent** (Port 5001)
   - Binary to decimal conversion
   - IP address classes
   - Fundamental subnetting concepts

2. **Custom Subnet Masks Agent** (Port 5002)
   - Structured problem sets
   - Custom subnet mask calculations
   - Practice with varying network requirements

3. **Subnet Range Calculations Agent** (Port 5003)
   - Network address calculations
   - Broadcast address determination
   - Usable host range identification

4. **VLSM Agent** (Port 5004)
   - Variable Length Subnet Masking
   - Network diagram generation
   - Efficient IP address allocation

## Features

- **Progressive AI Hints**: Each agent uses Claude API to provide intelligent, context-aware hints
- **Interactive Learning**: Step-by-step guidance through complex networking concepts
- **Unified Launcher**: Single script to start all four agents simultaneously
- **Spyder IDE Compatible**: Designed to run seamlessly in the Spyder development environment

## Requirements

- Python 3.7+
- Flask
- Anthropic API key
- Required Python packages (see installation)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/cisco-tutoring-system.git
cd cisco-tutoring-system
```

2. Install required packages:
```bash
pip install flask anthropic
```

3. Set up your Anthropic API key:
   - Create an account at https://www.anthropic.com
   - Generate an API key
   - Add your API key to each agent's configuration file

## Usage

### Running All Agents (Recommended)

Use the unified launcher script to start all four agents at once:

```bash
python launcher.py
```

This will start all agents on their designated ports:
- Agent 1 (Basic Subnetting): http://localhost:5001
- Agent 2 (Custom Subnet Masks): http://localhost:5002
- Agent 3 (Subnet Range Calculations): http://localhost:5003
- Agent 4 (VLSM): http://localhost:5004

### Running Individual Agents

You can also run agents individually if needed:

```bash
python agent1_basic_subnetting.py
python agent2_custom_masks.py
python agent3_subnet_ranges.py
python agent4_vlsm.py
```

**Note**: Ensure each agent uses its unique port to avoid conflicts.

## Project Structure

```
cisco-tutoring-system/
│
├── launcher.py                    # Unified launcher for all agents
├── agent1_basic_subnetting.py    # Basic subnetting concepts
├── agent2_custom_masks.py        # Custom subnet mask problems
├── agent3_subnet_ranges.py       # Subnet range calculations
├── agent4_vlsm.py                # VLSM assignments
├── README.md                      # This file
├── PROMPTS.md                     # System prompts documentation
└── requirements.txt               # Python dependencies
```

## Configuration

Each agent requires an Anthropic API key. Update the API key in each agent file:

```python
client = anthropic.Anthropic(api_key="your-api-key-here")
```

### Port Configuration

The system uses the following port assignments:
- Agent 1: Port 5001
- Agent 2: Port 5002
- Agent 3: Port 5003
- Agent 4: Port 5004

These ports are configured in both the individual agent files and the launcher script.

## Development Notes

### Known Issues and Solutions

1. **Port Conflicts**: Original versions had overlapping port assignments causing silent failures. Current version assigns unique ports to each agent.

2. **File Version Management**: Always ensure you're running the latest version of each file. Using outdated versions can perpetuate resolved issues.

3. **Spyder IDE Compatibility**: The launcher script is designed to work within Spyder's environment and manages all processes centrally.

## Educational Content

Each agent focuses on specific Cisco networking concepts:

- **Agent 1**: Foundation concepts including binary conversion and IP address classes
- **Agent 2**: Practical application of custom subnet masks with structured exercises
- **Agent 3**: Detailed calculations for network ranges and host addresses
- **Agent 4**: Advanced VLSM techniques with visual network diagrams

## API Integration

The system integrates with Anthropic's Claude API to provide:
- Context-aware hints based on student progress
- Progressive difficulty levels
- Natural language explanations of networking concepts
- Interactive problem-solving guidance

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

[Your chosen license]

## Acknowledgments

- Built with Flask web framework
- Powered by Anthropic's Claude API
- Designed for Cisco networking education

## Support

For issues or questions, please open an issue on GitHub or contact [your contact information].

---

**Note**: This project is designed for educational purposes to help students learn Cisco networking concepts through interactive AI-powered tutoring.
