# 🏠 Airbnb Search Assistant

A Streamlit-based chatbot application that helps users find their perfect accommodation using AI-powered search capabilities. The assistant can search for properties worldwide, filter by amenities, and provide personalized recommendations.

![Airbnb Search Assistant](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0%2B-orange)

## ✨ Features

- 🎨 Beautiful, Airbnb-inspired UI with custom styling
- 🔍 AI-powered property search and recommendations
- 🌍 Worldwide property search capabilities
- 🏡 Filter by amenities and preferences
- 💬 Interactive chat interface
- 🔄 Automatic fallback to basic chat mode if MCP connection fails
- 📱 Responsive design for all devices

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Node.js (for MCP server)
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install MCP server:
```bash
npm install -g @openbnb/mcp-server-airbnb
```

4. Create a `.env` file in the examples directory with your API keys:
```env
OPENAI_API_KEY=your_openai_api_key
```

### Running the Application

1. Start the Streamlit app:
```bash
streamlit run chatbot.py
```

2. Open your browser and navigate to:
```
http://localhost:8501
```

## 💡 Usage

1. Enter your search query in the chat input, for example:
   - "Find me a beachfront villa in Bali for 4 people"
   - "Show luxury apartments in Paris with Eiffel Tower views"
   - "Search for pet-friendly houses in London with a garden"

2. The assistant will provide detailed responses about properties, including:
   - Amenities
   - Location benefits
   - Pricing information
   - Reviews and ratings

3. Use the "Clear Chat" button to start a new conversation

## 🛠️ Technical Details

### Architecture

- Frontend: Streamlit
- Backend: Python with LangChain
- AI Model: GPT-4o-mini
- MCP Integration: Airbnb MCP Server

### Key Components

- `chatbot.py`: Main application file
- `airbnb_mcp.json`: MCP server configuration
- Custom CSS styling for Airbnb-like interface
- Error handling and fallback mechanisms

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Special thanks to [openbnb-org/mcp-server-airbnb](https://github.com/openbnb-org/mcp-server-airbnb) for the MCP server
- OpenAI for the GPT models
- Streamlit for the web framework

## 📞 Support

For support, please open an issue in the repository or contact the maintainers.

---

Made with ❤️ by [Your Abhishek Kumar] 
