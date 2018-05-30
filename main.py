# -*- coding: utf-8 -*
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import web
import random

urls = (
    '/', 'indexhandler',
    '/index', 'indexhandler',
    '/next(.*)', 'next',
    '/login','login',
    '/favicon.ico', 'icons',
    '/rest', 'rest',
)
app = web.application(urls, globals())
render = web.template.render('templates/')

vocas=[]


def load_voca():
    global vocas;
    with open('materia/voca.txt','rb') as fb:
        voca_row=fb.read().encode("utf-8").replace('\r','')
        _vocas=voca_row.split('\n')
        for voca in _vocas:
            each_item=voca.split('----');
            vocas.append(each_item)
            #print(each_item)
        print('\n\n\n----------------------------------\n\n\n')

load_voca()


user_info={};#info:[],fin:[],unfin:[],on_learn:[],correct:[],time_cost:[],group:int
group=[{}];
# in each group: {uid:[],voca:[],fin_num:int}
#each group contains/selected lot of vocas

def batched_voca(nums=20):
    
    all_nums=len(vocas)
    selected_num=0
    batch_=[]

    if all_nums==0 or nums<=0:
        return [];

    while selected_num < nums:
         var = random.randint(0,all_nums-1)
         if var not in batch_:
            batch_.append(var)
            selected_num+=1
    return batch_
        
        


def check_and_add_user(user_id):
    #print user_id
    print user_info[user_id]
    print user_info[user_id]['group']


    if len(group)==0 or user_info[user_id]['group']==-1:
        print('new participant\n\n\n')
        print group[-1]

        if not group[-1].has_key('uid'):
            print('empty')
            group[-1]['uid']=[user_id]
            group[-1]['voca']=batched_voca();
            index =0
            for v in group[-1]['voca']:
                print index,v
                index+=1
        elif user_id not in group[-1]['uid']:
            group[-1]['uid'].append(user_id)
    print group
    return len(group[-1]['uid'])<=10, 0


def learn(uid):

    if len(user_info[uid]['on_learn'])==0 and \
     len(user_info[uid]['unfin'])==0 and \
     len(user_info[uid]['fin'])>=0:
     return web.seeother('/')

    if len(user_info[uid]['on_learn'])==5:
        vvv=[]
        for var in user_info[uid]['on_learn']:
            vvv.append(vocas[var])
        return render.test(vvv, uid, 30)

    this_index=random.randint(0,len(user_info[uid]['unfin'])-1)
    this_var=user_info[uid]['unfin'][this_index]
    user_info[uid]['on_learn'].append(this_var)
    user_info[uid]['unfin'].remove(this_var)
    return render.learn(vocas[this_var], 10, uid);



class login:
    global user_info;

    def GET(self,name=None):
        print('not interested in ...')
        return web.seeother('/');
        pass

    def POST(self,name=None):
        print('in post function name=',name)
        data=web.input();

        print(user_info)

        if user_info.has_key(data['uid']):
            print('already recorded...')
        else:
            user_info[data['uid']]={
                        'info':[data['uid'],data['maj'],data['age'],data['grad'],data['gend']],
                        'fin':[],'unfin':[],'on_learn':[],'correct':[],'time_cost':[],'group':-1
                        }
        print(user_info)
        res,gid=check_and_add_user(data['uid'])
        if res:
            user_info[data['uid']]['group']=gid
            user_info[data['uid']]['unfin']+=group[gid]['voca']
            #print(user_info)
            return learn(data['uid']);
        return 'this batch is fulled, please wait for next batch!'
        pass


class indexhandler:
    def GET(self):
        return render.login()


    def POST(self):
        return render.index()
        pass

def score(L=[0,0,0,0,0],last_round=5):
    total_score=0
    current_score=0
    for a in L:
        total_score+=a
    r=-1
    for a in range(0,last_round):
        current_score+=L[r]
        r-=1
    return total_score, current_score

class rest:
    def GET(self,name=None):
        print 'should not be here anymore.-------------...'
        return 'should not be here anymore.-------------...'

    def POST(self,name=None):
        data = web.input()
        print data['uid']
        user_group = group[user_info[data['uid']]['group']]['uid']
        print user_group

        if len(user_group) < 2 :
            return render.rest([[1,2],[2,3],[3,4],[5,6],[6,7]],data['uid'],60);
            pass

        jueged=len(user_info[user_group[0]]['correct'])
        score_all = []

        for var in user_group:
            if jueged != len(user_info[var]['correct']):
                return render.rest([[1,2],[2,3],[3,4],[5,6],[6,7]],data['uid'],10);
            total_score, current_score = score(user_info[var]['correct'])
            score_all.append([var, current_score, total_score])

        print score_all
        
        rank_info='['
        index=1
        while len(score_all)!=0:
            min_score=-1
            last_one=None
            for x in score_all:
                if min_score < x[2]:
                    last_one=x

            rank_info+='['+str(index)+','+"'"+last_one[0]+"',"+str(last_one[1])+','+str(last_one[2])+'],'
            index+=1
            score_all.remove(last_one)
        #rank_info=str(rank_info)
        rank_info=rank_info[:-1]+']'

        print rank_info

        return render.backward('nothing',rank_info, data['uid'],15);




class next:
    def GET(self,name):
        print(name)
        data = web.input()

        print(data['uid'],data['voca_item'])

        for val in data:
            print(type(val), val, data[val])

        
        return learn(data['uid'])


    def POST(self,name):#special work for test
        print('in post function name=',name)
        data=web.input();

        print type(data['voc_1'].encode("utf-8")), data['voc_1'],'-----', vocas[user_info[data['uid']]['on_learn'][0]]
        print type(data['voc_1'].encode("utf-8")), data['voc_2'],'-----', vocas[user_info[data['uid']]['on_learn'][1]]
        print type(data['voc_1'].encode("utf-8")), data['voc_3'],'-----', vocas[user_info[data['uid']]['on_learn'][2]]
        print type(data['voc_1'].encode("utf-8")), data['voc_4'],'-----', vocas[user_info[data['uid']]['on_learn'][3]]
        print type(data['voc_1'].encode("utf-8")), data['voc_5'],'-----', vocas[user_info[data['uid']]['on_learn'][4]]

        print(data['uid'].encode("utf-8"))

        current_score=0
        if data['voc_1'] == vocas[user_info[data['uid']]['on_learn'][0]][0]:
            user_info[data['uid']]['correct'].append(1)
            current_score+=1
        else :
            user_info[data['uid']]['correct'].append(0)

        if data['voc_2'] == vocas[user_info[data['uid']]['on_learn'][1]][0]:
            user_info[data['uid']]['correct'].append(1)
            current_score+=1
        else :
            user_info[data['uid']]['correct'].append(0)

        if data['voc_3'] == vocas[user_info[data['uid']]['on_learn'][2]][0]:
            user_info[data['uid']]['correct'].append(1)
            current_score+=1
        else :
            user_info[data['uid']]['correct'].append(0)
        
        if data['voc_4'] == vocas[user_info[data['uid']]['on_learn'][3]][0]:
            user_info[data['uid']]['correct'].append(1)
            current_score+=1
        else :
            user_info[data['uid']]['correct'].append(0)
        
        if data['voc_5'] == vocas[user_info[data['uid']]['on_learn'][4]][0]:
            user_info[data['uid']]['correct'].append(1)
            current_score+=1
        else :
            user_info[data['uid']]['correct'].append(0)

        total_score= 0
        for var in user_info[data['uid']]['correct']:
            total_score+=var

        print current_score,'-----', total_score

        voca_id=user_info[data['uid']]['on_learn'][-1];

        user_info[data['uid']]['fin']+=user_info[data['uid']]['on_learn'];
        del user_info[data['uid']]['on_learn'][:];

        print(user_info[data['uid']])

        strr='[[0,\''+data['uid'].encode("utf-8")+'\','+str(current_score)+','+str(total_score)+'],\
                    [2,\'fake-2\',parseInt(5*Math.random()),parseInt(10*Math.random())+1]]';
        print strr


        return render.rest([[1,2],[2,3],[3,4],[5,6],[6,7]],data['uid'],2)
        #return render.backward(vocas[voca_id][0],strr, data['uid'],15);



class icons:
    def GET(self,name=None):
        return web.seeother('/static/favicon.ico')
    def POST(self,name=None):
        return web.seeother('/static/favicon.ico')

def main():
    print 'eeeeeeeeeee'
    app.run()
    pass


if __name__ == '__main__':
    main()
