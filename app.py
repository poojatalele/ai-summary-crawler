from flask import Flask, render_template, request
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urldefrag
from collections import deque
import requests
import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

def extract_text(html):
    soup = BeautifulSoup(html, 'html.parser')
    for script in soup(['script', 'style']):
        script.decompose()
    return soup.get_text(separator=' ', strip=True)

def summarize_text_with_gpt(text, url):
    prompt = f"""
    You are an expert web content summarizer. Your goal is to read the following webpage content and produce a concise, readable summary in 5–7 sentences.

    URL: {url}

    Instructions:
    - Capture the main purpose of the webpage.
    - Highlight key services, ideas, or features mentioned.
    - Omit repetitive, promotional, or legal content.
    - Avoid listing navigation/menu items or unrelated side info.
    - Use clear, human-like language.

    Webpage Content:
    {text[:3000]}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful summarizer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=300
        )
        # print(response)
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"GPT error for {url}: {e}")
        return None

def crawl_and_summarize(start_url, max_pages=10):
    visited = set()
    queue = deque([start_url])
    results = {}
    error_message = None

    while queue and len(visited) < max_pages:
        url = queue.popleft()
        url = urldefrag(url)[0].rstrip('/')

        if url in visited:
            continue

        try:
            print(f" Crawling: {url}")
            response = requests.get(url, timeout=8)
            if response.status_code != 200:
                print(f" Skipping {url} as it is not accessible due to status code {response.status_code}")
                continue

            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.title.string.strip() if soup.title else "Untitled"
            text = extract_text(html)
            summary = summarize_text_with_gpt(text, url)

            if summary:
                results[url] = {
                    "title": title,
                    "summary": summary
                }

            for link in soup.find_all('a', href=True):
                full_url = urljoin(url, link['href'])
                full_url = urldefrag(full_url)[0].rstrip('/')
                if full_url not in visited:
                    queue.append(full_url)

            visited.add(url)

        except Exception as e:
            error_message = f" Error crawling {url}: {e}"
            print(error_message)

    if not results:
        error_message = error_message or "No pages could be crawled. The site may block bots or be JavaScript-only."

    return results, error_message

@app.route('/', methods=['GET', 'POST'])
def home():
    summaries = {}
    error = None

    if request.method == 'POST':
        start_url = request.form.get('url')
        max_pages = int(request.form.get('max_pages', 10))
        summaries, error = crawl_and_summarize(start_url, max_pages)

        with open('page_summaries.json', 'w', encoding='utf-8') as f:
            json.dump(summaries, f, indent=2, ensure_ascii=False)

    return render_template('index.html', summaries=summaries, error=error)

if __name__ == '__main__':
    app.run(debug=True)
