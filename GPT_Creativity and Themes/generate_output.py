import os.path
import time
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

import urllib



#change the value in return to set the single color need, in hsl format.
def grey_color_func(word, font_size, position,orientation,random_state=None, **kwargs):
    return "black"




# define drawing of the words and links separately.
def plot_main_topics(sorted_dict_topics):

    color=["#E73E55","#D5667F","#DF7F95","#E999AB","#F4B3C2"] #Change this values to select the 7 colours of Topics

    

    px = 1/plt.rcParams['figure.dpi']
    
    fig = plt.figure(figsize=(1280*px, 2000*px))
    plt.clf()
    
    i = 0
    for key in sorted_dict_topics:
       
        
        plt.text(0.5,0.9-i*0.2, key[0], ha="center", va="center",size=80, color = color[i], weight ='bold')

        i = i+1
        
    plt.axis('off')
    
    # Change the TOPICS background colour here
    fig.patch.set_facecolor('#FFFFFF')
    
    plt.savefig('main_topics.png')



def plot_categories(str_scale, str_rating):
    i=0
    px = 1/plt.rcParams['figure.dpi']
    
    fig = plt.figure(figsize=(640*px, 480*px))
 
    # creating the bar plot
    bar = plt.barh(str_scale,str_rating, color ='blacK')
    

     # Add counts above the two bar graphs
    for rect in bar:
        width = rect.get_width()
     
        
        
        
        plt.text(width+0.5,rect.get_y()+rect.get_height()/2, f'{str_rating[i]}', ha='center', va='bottom',color = 'black', size=20)
        #plt.text(rect.get_x() + rect.get_width() /2, 0.08, f'{str_topic[i]}', ha='center', va='bottom',rotation = 90,color = 'white', size=15)
        i=i+1
    plt.xlim(0,10) 
    plt.axvline(x = 10, color = 'black', label = 'axvline - full height',lw=10)
    plt.xticks([])
    plt.tight_layout()
    plt.savefig('categories.png')
  


def plot_text(text,filename,variant):
    
    px = 1/plt.rcParams['figure.dpi']

    fig = plt.figure(figsize=(2000*px, 1200*px)) 	#uncomment for Haiku
    #fig = plt.figure(figsize=(1200*px, 1600*px))  	#uncomment for Summary
    if variant == 'summary':

        #bbox_props = dict(boxstyle='round,pad=0', ec='black', lw=1, fc='white')
        plt.text(-0.1, 0.6, text, family='serif', size=40, wrap=True, color='red') #CHANGE SUMMARY TEXT COLOUR HERE 
        #plt.tight_layout(pad=0)
        #plt.subplots_adjust(left=0.1)


    if variant == 'haiku':

        plt.text(0.1,0.5, text, family='serif',size=80, wrap=True, linespacing=2, multialignment='center',style='italic', color='white',) #CHANGE HAIKU TEXT COLOUR HERE


    plt.xticks([])
    #plt.tight_layout()
    plt.axis('off')
    
    # Change the HAIKU and SUMMARY background colour here
    fig.patch.set_facecolor('#AB4F98') 
    
    plt.savefig(filename)


def generate_image(img_url):
    file_name = "image.png"
    urllib.request.urlretrieve(image_url,file_name)
