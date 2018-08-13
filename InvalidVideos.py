# -*- coding:utf-8 -*-
import sys
import requests
import re
import json

agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'

fav_list = []
fav_name_list = []
output_index = 1     


#entry point, parse command line args
def run():
    if len(sys.argv) < 2:
        print('Error: Please enter Bilibili user id.')
        return
    user_id = int(sys.argv[1])
    if user_id <= 0:
        print('Error: Please enter a valid Bilibili user id.')
        return
    get_fav_videos_from_user(user_id)


#main function flow:    get all fav folders 
#                       -> loop through fav folder id
#                       -> loop through page in that folder id
#                       -> loop all video info to find invalid ones and record them
#                       -> write to output file
#                       -> done
def get_fav_videos_from_user(uid):
    get_fav_folder_list(uid)  #get all fav folders, id store to fav_list, names store to fav_name_list
    output = ''
    for i in range(0, len(fav_list)):                                        #loop all fav folders
        s = process_fav_folder(uid, i)                            #current fav folder jObject, constain all video infos 
        output += s 

    write_output(output)

#find all fav folders ids and names.
def get_fav_folder_list(uid):
    global fav_list

    url = 'https://api.bilibili.com/x/space/fav/nav?mid={userid}&jsonp=jsonp'.format(userid=uid)
    resp = get_HTML_text(url, agent)
    responed_jobject = json.loads(resp)
    archive = responed_jobject['data']['archive']
    
    for i in range(0, len(archive)):
        fav_folder_obj = archive[i]
        fav_folder_id = fav_folder_obj['fid']
        fav_folder_name = fav_folder_obj['name']
        fav_list.append(fav_folder_id)
        fav_name_list.append(fav_folder_name)
    print('mid={user} has fav folders: {folder}'.format(user=uid, folder=fav_name_list))


#given a fav folder id, find pages and parse videos info
def process_fav_folder(uid, fav_list_index):
    global fav_list

    fav_folder_content = ''
    url = 'https://api.bilibili.com/x/space/fav/arc?vmid={userid}&ps=30&fid={favid}&tid=0&keyword=&pn=1&order=fav_time&jsonp=jsonp'.format(userid=uid, favid=fav_list[fav_list_index])
    resp = get_HTML_text(url, agent)
    responed_jobject = json.loads(resp)
    page_count = responed_jobject['data']['pagecount']
    print('{favid} has {page} pages.'.format(id=uid,favid=fav_name_list[fav_list_index],page=page_count))

    video_jobject = responed_jobject['data']['archives']
    fav_folder_content += handle_jobject_per_page(video_jobject, fav_list_index, 1)

    for i in range(2, page_count + 1):
        url = 'https://api.bilibili.com/x/space/fav/arc?vmid={userid}&ps=30&fid={favid}&tid=0&keyword=&pn={page_index}&order=fav_time&jsonp=jsonp'.format(userid=uid, favid=fav_list[fav_list_index], page_index=i)
        resp = get_HTML_text(url, agent)
        responed_jobject = json.loads(resp)
        video_jobject = responed_jobject['data']['archives']
        fav_folder_content += handle_jobject_per_page(video_jobject, fav_list_index, i)
    
    return fav_folder_content

#each page contains 30 videos, I tried passing 1000, do NOT work. :(
#parse videos in give page, write individual video info to output. 
#here you can custom what info you want, and the format you want. For avaliable elements, print 'jObject.Keys'
def handle_jobject_per_page(page_jobjects, fav_list_index, page_index):
    global output_index
    global fav_name_list

    page_info = ''
    valid_count = 0
    invalid_count = 0
    for i in range(0, len(page_jobjects)):
        jObject = page_jobjects[i]
        if int(jObject['state']) >= 0:
            valid_count += 1
            continue
        invalid_count += 1
        s = '#{number}{title}\n'.format(number=output_index, title=jObject['title'])
        s += 'AV{vid} 收藏夹:{favFolder},Page:{page},Index:{num}\n'.format(vid=jObject['aid'], favFolder=fav_name_list[fav_list_index], page=page_index, num=i)
        s += 'UP主:{up}<space.bilibili.com/{mid}>\n'.format(up=jObject['owner']['name'], mid=jObject['owner']['mid'])
        s += '注释:\n{desc}\n\n\n'.format(desc=jObject['desc'])    
        page_info += s 
        output_index += 1
    print('    {}:Page {} has {} valid videos and {} invalid videos, index reach to \'{}\'. '.format(fav_name_list[fav_list_index], page_index, valid_count, invalid_count, output_index))
    return page_info

#write infos to output file
def write_output(info):
    file = open('invalidFavVideos.txt', 'w', encoding='utf-8')  
    file.write(info)
    file.close()
    print("\nDone! Outputing invalid {} videos. Happy holding and have a nice day~ \[T] /\n".format(output_index))

def get_HTML_text(url, agent):
    try:
        headers = {'User-Agent': agent}
        r = requests.get(url, timeout=30, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ('Error: Unable to query Bilibili server!')


run()
