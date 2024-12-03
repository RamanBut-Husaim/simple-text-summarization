from news_parser import NewsParser
from news_tokenizer import NewsTokenizer
from news_summarizer import NewsSummarizer
from news_entry import NewsEntry

FILE_PATH: str = 'data/news.xml'

def display(news: list[NewsEntry]):
    for news_entry in news:
        print(f'HEADER: {news_entry.header}')
        text = '\n'.join(news_entry.sentences)
        print(f'TEXT: {text}')
        print()

def read_file(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

if __name__ == '__main__':
    file_content = read_file(FILE_PATH)

    news_parser = NewsParser()
    news = news_parser.parse(file_content)

    tokenizer = NewsTokenizer()
    tokenizer.initialize()
    tokenized_news = tokenizer.tokenize(news)

    summarizer = NewsSummarizer()
    summarized_news = summarizer.summarize(tokenized_news)

    display(summarized_news)
