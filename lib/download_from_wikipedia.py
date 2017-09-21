import wikipedia
import requests
import pandas as pd
import re


def generate_query(category):
    '''
    Format an api call for requests
    '''
    category = re.sub('\s','+',category)
    
    base_url = 'http://en.wikipedia.org/w/api.php?'
    act = 'action=query&'
    frmt = 'format=json&'
    lst = 'list=categorymembers&'
    cmtitle = 'cmtitle=Category:'
    cmlimit = '&cmlimit=max'
    
    query = base_url + act + frmt + lst + cmtitle + category + cmlimit

    return query


def execute_category_query(category):
    '''
    Executes a category qeury and returns a 
    DataFrame of the category members
    '''
    
    r = requests.get(generate_query(category))
    response = r.json()
    
    return pd.DataFrame(response['query']['categorymembers'])


def get_all_pages_rec(category, sub_cat_level=2, depth=0):

    category_df = execute_category_query(category)
    pages_list = []
    sub_cat_mask = category_df['title'].str.contains('Category:')
    pages_df = category_df[~sub_cat_mask]
    pages_list.append(pages_df)
    sub_cats = category_df[sub_cat_mask]['title'].str.replace('Category:','').tolist()
    if (len(sub_cats) > 0) and (depth+1 <= sub_cat_level):
        for cat in sub_cats:
            if len(execute_category_query(cat)) > 0:
                pages_list.append(get_all_pages_rec(cat, sub_cat_level=sub_cat_level, depth=depth+1))

    pages_df = pd.concat(pages_list)
    pages_df.reset_index()
    
    return pages_df


def get_whole_category(category, sub_cat_level=2):
    
    df = get_all_pages_rec(category, sub_cat_level)
    df = df.drop_duplicates(subset='title').reset_index(drop=True)
    df['category'] = category
    
    return df


def get_articles(category, sub_cat_level=2):
    
    try:
        wikipedia.WikipediaPage('Category:{}'.format(category))
        df = get_whole_category(category, sub_cat_level=sub_cat_level)
        print('There are {} articles under category "{}" (subcategory depth = {})'.format(len(df), category, sub_cat_level))
        print('Enter "y" to download all articles. Otherwise, enter "n" and change the category and/or subcategory depth.')
        keyboard_input = input()
        if keyboard_input == 'y':
            contents_list = []
            for index, row in df.iterrows():
                try:
                    wiki_page = wikipedia.WikipediaPage(row['title'])
                    contents_list.append(wiki_page.content)
                except:
                    contents_list.append('NO CONTENT')
                if (index+1) % 200 == 0:
                    print('downloaded {} articles so far...'.format(index+1))

            print('{} articles downloaded successfully!'.format(index+1))
            df['content'] = contents_list

            return df
        else:
            pass
    except:
        print('No wikipedia category named {}'.format(category))
        return None

    
def get_article_content(url):
    page_title = url.split('/wiki/')[1]
    try:
        article_content = wikipedia.WikipediaPage(page_title).content
        return article_content
    except:
        print('Incorrect Wikipedia URL')
        return None