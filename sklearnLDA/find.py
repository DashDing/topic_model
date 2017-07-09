#coding:utf-8
import os
if __name__ == '__main__':
    filename = 'topic--'
    path = '/home/ding/Desktop/LDAModel/'
    keywordsList = [
    #['gun','weapon'],['gun','ammo'],['btc','bitcoin'],
    #['sex','girls'],['search','engine'],['tor','onion'],['drug','heroin'],
    #['hosted','hosting'],['gun','price'],['drug','price','weapon','ammo'],['porn','drug','gun'],
    #['hacker','hacking'],['buy','want']
    ['gun','bullet'],#gun
    ['weapon','ammo'],#weapon
    ['drug','heroin'],#drug
    ['porn','drug','weapon','market'],#forum
    ['hosting','hosted'],#host
    ['search','engine'],#search engine
    ['sex','girl'],#porn
    ['buy','want','market'],#market
    ['hacker','hacking'],#hacking
    ['file','folder'],#file share
    ['mail','message'],#mail
    ['vid','pic'],#media
    ['fake','counterfeit']
    ]
    result = []
    unt = [['host','search'],['piece','gun'],['hack','piece'],
    ['counterfeit','mail']]
    for root, dirs, files in os.walk(path):
        for name in files :
            if 'topic--' in name:
                f = open(path + name)
                lines = f.readlines()
                returnlist = []
                descore = []
                for line in lines:
                    for keywords in keywordsList:
                        localbool = True
                        for keyword in keywords:
                            if keyword not in line:
                                localbool = False
                        if localbool and keywords not in returnlist:
                            returnlist.append(keywords)

                    for keywords in unt:
                        num = 0
                        for keyword in keywords:
                            if keyword  in line:
                                num += 1
                        if num > 1 and keywords not in descore:
                            descore.append(keywords)
                
                if len(returnlist) >0:
                    topicNum = int(name.split('--')[1])
                    score = len(returnlist)-len(descore)
                    #if 10<=topicNum<=20:
                    #    score += 1
                    result.append([name,len(returnlist),len(descore),returnlist,descore,score])
    result = sorted(result, key = lambda x:x[1])
    
    for [id,li,ld,returnlist,des,score] in result:
        print 'No.:{0} inscore:{1} descore:{2} score:{5}\n{3}\n{4}\n'.format(id,li,ld,returnlist,des,score)