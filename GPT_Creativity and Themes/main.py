
import openai
import re
from langchain import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
import configparser
import os.path
import time
import argparse
import os
import logging
import urllib
from provotype.prep import read_text
from provotype.promts_gpt import generate_summarizer,do_summarization,summarize_summarized_texts,create_five_topics,scale_conversation,write_a_haiku,create_image
from provotype.generate_output import plot_main_topics,plot_categories,plot_text,generate_image
import logging
import sys








def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--configfile', default='/home/wordcloud/wordcloud_keys/config.ini',metavar='N', type=str, nargs='+',
                        help='an integer for the accumulator')

    '''parser.add_argument('--configfile', default='config.ini',metavar='N', type=str, nargs='+',
                        help='an integer for the accumulator')'''

    parser.add_argument('--textfile', default = '/home/wordcloud/WordCloud/AzureSpeechCC/content.txt', metavar='N', type=str, nargs='+',
                        help='an integer for the accumulator')
    '''parser.add_argument('--textfile', default = 'content.txt', metavar='N', type=str, nargs='+',
                        help='an integer for the accumulator')'''
    args = parser.parse_args()
    print(args.configfile)
    return args


def parse_config(configfile):
    config = configparser.ConfigParser()   
    config.read(configfile)
    api_key = config['API']['my_api']
    return api_key
   
 


def do_job(text_file):
    
    from time import sleep

    logger.info('starting with summarization')

    split_text,nmb_splits, max_number_tokens = read_text(text_file)
    
    

    if nmb_splits >1:
        text_summarization = do_summarization(split_text,nmb_splits, max_number_tokens)

        text_summarization = " ".join(text_summarization)

        response_summary = summarize_summarized_texts(text_summarization)


    else:

        text_summarization = split_text
        response_summary = summarize_summarized_texts(split_text)
        
    summary = response_summary[0]['content']
    logger.info('summarization done')
    plot_text(summary,'summary.png','summary')

    logger.info('starting with haiku')
    haiku = write_a_haiku(summary)
    plot_text(haiku[0]['content'],'haiku.png','haiku')
    logger.info('haiku done')

    logger.info('starting with image creation')
    image_url=create_image('create a vaporwave art without text for: ' + response_summary[0]['content'])
    file_name = "image.png"
    urllib.request.urlretrieve(image_url,file_name)
    logger.info('image done')

     

    logger.info('starting with top topics')
    sorted_dict_topic  = create_five_topics(summary)
    plot_main_topics(sorted_dict_topic)
    logger.info('top topics done')
    

    '''list_scale, list_rating_scale = scale_conversation(text_summarization)
    plot_categories(list_scale, list_rating_scale)
    print("scale conversation done!\n")'''



def main(args):


   



    logger.info("Program started")



    config = args.configfile
    textfile = args.textfile
    
    if config is not None:
        api_key = parse_config(config)

        openai.api_key = api_key

    
        
        if (textfile is not None) and (os.stat(textfile).st_size != 0):
        
            time.sleep(30)

            while True:
                
                do_job(textfile)

                time.sleep(300)
            
            
         
        else:
            print("no textfile available")
            exit()
        
    



if __name__=='__main__':  

     # instantiate logger
    logger = logging.getLogger(__name__)

    logging.basicConfig(
            #format="%(asctime)s [%(levelname)s]: %(message)s in %(pathname)s:%(lineno)d",
            datefmt = '%m/%d/%Y %I:%M:%S %p',
            filename = 'example.log',
            level=logging.INFO,
            filemode='w',
            #stream=sys.stdout
        )
    logger.setLevel(logging.INFO)

    # define handler and formatter
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")

    # add formatter to handler
    handler.setFormatter(formatter)

    # add handler to logger
    logger.addHandler(handler)


   
    args = get_args()
    main(args)
