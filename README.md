# 🕸️ AI-Powered Web Crawler with GPT Summarization

A web crawler that automatically extracts and summarizes webpage content using OpenAI’s GPT-3.5. Built with Flask, this project lets users input a URL and receive concise summaries of linked pages — like a tiny, intelligent search engine.

## 🚀 Features

- 🌐 **Web Crawler (BFS)**: Crawls a website up to a specified number of pages.
- 🧠 **AI Summarization**: Uses GPT-3.5 to summarize content in human-like language.
- 💾 **JSON Export**: Stores results locally in `page_summaries.json`.
- 🖥️ **Flask UI**: Simple form interface with live summary output.

### 🔗 Live Demo & Video

🚀 **Live App:**  
[AI Summary Crawler](https://ai-summary-crawler.onrender.com)

🎥 **Demo Video:**  
[Demo Video](https://drive.google.com/file/d/1Q70PP0Ne6YOEd7urHjIANEoCVXbfTAIo/view?usp=sharing)

## ⚙️ Setup Instructions

1. **Clone the repo**

```bash
git clone https://github.com/poojatalele/ai-summary-crawler.git
cd ai-summary-crawler
```

1. **Install Dependencies**
   
```bash
pip install -r requirements.txt
```

3. **Create a .env file and add**
   
```bash
OPENAI_API_KEY=your-api-key-here
```

4. **Run the flask app**
```bash
python app.py
```
