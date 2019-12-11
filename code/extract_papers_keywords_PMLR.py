#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 10:19:52 2019

extract intersting papers from a CVF open repository site 

@author: feng.559
"""
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd

############## Specify your conference and keywords here #######################
######## This script only works for ICML and other PMLR listed conferences #####
conf_list = ['ICML 2016']
keywords = ['unsupervise','self-supervise']
combine_method = 'or'
################################################################################


url_input = 'http://proceedings.mlr.press/'
r = requests.get(url_input)
html_content = r.text

soup = BeautifulSoup(html_content)
links = soup.find_all('li')

all_vol_url = [s.find('a').get('href') for s in links if s.find('a') is not None]
all_vol_text = [s.get_text() for s in links if s.find('a') is not None]


for this_conf in conf_list:
    this_conf_subpage = all_vol_url[[ind for ind, s in enumerate(all_vol_text) if this_conf in s][0]]
    url_input = 'http://proceedings.mlr.press/%s/' % this_conf_subpage
    url_root = url_input
    r = requests.get(url_input)
    html_content = r.text
    
    soup = BeautifulSoup(html_content)

    
    # get urls for all the papers (this is the url for each paper where you will see 
    # titles, authors, abstract, pdf download url, etc. )
    papers = soup.find_all('div',class_='paper')
    titles_url = [s.find('a').get('href') for s in papers] # in PMLR the first  <a> tag is for the page link to the paper
    
    # iterate through all papers to extract the title, abstract, authors and pdf url
    paper_dict_list = []
    for this_title_url in titles_url:
        print('processing %s' % this_title_url)
        try:
            this_title_url_full = this_title_url
            
            r = requests.get(this_title_url_full)
            html_content = r.text
            this_soup = BeautifulSoup(html_content)
            
            # extract title 
            this_paper_title = this_soup.find('meta',attrs={'name':'citation_title'})['content']
            # extract authors
            this_paper_authors = [s['content'] for s in this_soup.find_all('meta',attrs={'name':'citation_author'})]
            # extract pdf url
            this_paper_pdfurl = this_soup.find('meta',attrs={'name':'citation_pdf_url'})['content']
            # extract publication year and conference
            this_paper_year = this_soup.find('meta',attrs={'name':'citation_publication_date'})['content']
            this_paper_conf = this_soup.find('meta',attrs={'name':'citation_conference_title'})['content']
            # extract abstract
            this_paper_abstract = this_soup.find('div',id='abstract').get_text()
            
            paper_dict = {}
            paper_dict['title'] = this_paper_title
            paper_dict['authors'] = this_paper_authors
            paper_dict['pdf_url'] = this_paper_pdfurl
            paper_dict['abstract'] = this_paper_abstract
            paper_dict['conference'] = this_paper_conf
            paper_dict['year'] = this_paper_year
            
            paper_dict_list.append(paper_dict)
        except:
            print('failed')
    
    # keyword
    save_dir = '../result/%s' % this_conf.replace(' ','')
#    keywords = ['unsupervise','self-supervise']
#    combine_method = 'or'
    folder_name = save_dir+'-'+('-'+combine_method+'-').join(keywords)
    if not os.path.isdir(folder_name):
        os.makedirs(folder_name)
    
    summary_dir = folder_name+'/summary.xlsx'
    
    target_dict_list = []
    for this_paper_dict in paper_dict_list:
        this_title = this_paper_dict['title']
        this_abstract = this_paper_dict['abstract']
        this_url = this_paper_dict['pdf_url']
        this_year = this_paper_dict['year']
        this_conf = this_paper_dict['conference']
    
        this_authors_list = this_paper_dict['authors']
        this_authors_list_reformate = [' '.join(s.split(', ')[::-1]) for s in this_authors_list]
        this_authors = '; '.join(this_authors_list_reformate)
        
        keyword_in_title = [s.upper() in this_title.upper() for s in keywords]
        keyword_in_abstract = [s.upper() in this_abstract.upper() for s in keywords]
        
        if combine_method == 'and':
            target_state = all(keyword_in_title) or all(keyword_in_abstract)
        elif combine_method == 'or':
            target_state = any(keyword_in_title) or any(keyword_in_abstract)
    
        if target_state:
            path, filename = os.path.split(this_url)
    
            pdf_req = requests.get(this_url)
            with open('/'.join([folder_name,this_title.replace(' ','_')+'.pdf']),'wb') as f:
                f.write(pdf_req.content)
    
            # write the paper meta data to a summary csv
            target_dict_list.append(this_paper_dict)
    
    df = pd.DataFrame(target_dict_list)
    writer = pd.ExcelWriter(summary_dir, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    workbook  = writer.book
    worksheet = writer.sheets['Sheet1']
    format = workbook.add_format({'text_wrap': True})
    worksheet.set_column('A:E', None, format)
    writer.save()




