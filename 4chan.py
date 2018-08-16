from bs4 import BeautifulSoup
import requests
import os

thread_num_c = []

def generate_colors():
    global thread_num_c
    for style in range(8):
        for fg in range(30,38):
            for bg in range(40,48):
                thread_num_c.append('\x1b['+str(style)+';'+str(fg)+';'+str(bg)+'m')
        #print(len(thread_num_c))

def main_page(thread_list,soup,count):
    generate_colors()
    for thread in soup.find_all('div',class_='thread'):
            for each_title in thread.find_all('div',class_='post op'):
                title= each_title.find('blockquote',class_='postMessage').text
                number = each_title.find('blockquote',class_='postMessage')['id'].replace('m','')
                if 'The /g/ Wiki' not in title:
                    thread_list.append(number)
                    print('==========#'+str(count)+'=============')
                    print('||POST N# '+number+' ||  ')
                    print('\n'+'- OP: '+title.replace('>','')+'\n')
                    count += 1
def fill_array(soup_thread,thread_num):
    for each_answer in soup_thread.find_all('div',class_='postContainer replyContainer'):
            num_thread = each_answer.find('blockquote',class_='postMessage')['id'].replace('m','')
            thread_num.append(num_thread)

def thread_page(query_choice,thread_list,thread_num):
    source_thread = requests.get('http://boards.4chan.org/g/thread/'+thread_list[int(query_choice)]).text
    soup_thread = BeautifulSoup(source_thread,"html5lib")
    title_t_page = soup_thread.find('blockquote', class_='postMessage').text
    number_t_page = soup_thread.find('blockquote', class_='postMessage')['id'].replace('m', '')
    os.system('clear')
    print('N# '+number_t_page+' '+'\x1b[1;31;40m' +'OP'+'\x1b[0m'+' '+'\n')
    print(title_t_page)
    fill_array(soup_thread,thread_num)
    for each_answer in soup_thread.find_all('div',class_='postContainer replyContainer'):            
        answer_text = each_answer.find('blockquote',class_='postMessage').text
        number_answer = each_answer.find('blockquote',class_='postMessage')['id'].replace('m','')

        if number_answer in thread_num:
            number_answer = thread_num_c[thread_num.index(number_answer)]+number_answer+ '\x1b[0m'
        for num in thread_num:
            if num in answer_text:
                answer_text= answer_text.replace(num,thread_num_c[thread_num.index(num)]+num+ '\x1b[0m'+' ')
                break
        print('======================')
        print('||'+number_answer)
        print('||'+answer_text.replace(number_t_page,('\x1b[1;31;40m' +'OP'+'\x1b[0m'+' ')))
    #print(list(set(thread_num)))

def refresh_thread():
    pass


def main():
    source = requests.get('http://boards.4chan.org/g/').text
    soup = BeautifulSoup(source, "html5lib")
    thread_list = []
    thread_num= []
    count = 0
    main_page(thread_list,soup,count)
    query_choice=input('Choose thread: ')
    thread_page(query_choice,thread_list,thread_num)
main()
