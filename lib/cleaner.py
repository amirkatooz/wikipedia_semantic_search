import re

def df_cleaner(df):
    
    no_content_mask = (df['article_content'] == 'NO CONTENT') | (df['article_content'] == '')
    user_page_mask = df['article_title'].str.contains('User:')
    template_page_mask = df['article_title'].str.contains('Template:')
    file_page_mask = df['article_title'].str.contains('File:')
    
    df = df[~(no_content_mask | user_page_mask)]
    
    return df.reset_index(drop=True)


def text_cleaner(lemmatized_text):
    
    text = re.sub('\W', ' ', lemmatized_text)
    text = re.sub('_', ' ', text)
    text = re.sub('[0-9]', ' ', text)
    text = re.sub('displaystyle', '', text)

    match = bool(re.search(' . ', text))
    while match:
        text = re.sub(' . ', ' ', text)
        match = bool(re.search(' . ', text))

    clean_text = re.sub('\s+', ' ', text)
    
    return clean_text


def title_cleaner(title):
    
    return title.replace("'", "''")