# -*- coding: utf-8 -*
import web
import random

urls = (
    '/', 'indexhandler',
    '/index', 'indexhandler',
    '/next(.*)', 'next',
    '/login','login',
    '/favicon.ico', 'icons',
)
app = web.application(urls, globals())
render = web.template.render('templates/')

vocas=[]


def load_voca():
    global vocas;
    with open('materia/voca.txt','rb') as fb:
        voca_row=fb.read().replace('\r','')
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
        return render.test(vvv, uid, 30*1000)

    this_index=random.randint(0,len(user_info[uid]['unfin'])-1)
    this_var=user_info[uid]['unfin'][this_index]
    user_info[uid]['on_learn'].append(this_var)
    user_info[uid]['unfin'].remove(this_var)
    return render.learn(vocas[this_var], 10*1000, uid);



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



class next:
    def GET(self,name):
        print(name)
        data = web.input()

        print(data['uid'],data['voca_item'])

        for val in data:
            print(type(val), val, data[val])

        
        return learn(data['uid'])


    def POST(self,name):
        print('in post function name=',name)
        data=web.input();

        print(data['uid'])
        user_info[data['uid']]['fin']+=user_info[data['uid']]['on_learn'];
        del user_info[data['uid']]['on_learn'][:];

        print('heeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
        print(user_info[data['uid']])

        return render.backward(vocas[random.randint(0,len(vocas)-1)], data['uid']);


class confirm:
    def GET(self):
        return render.confirm();

class icons:
	def GET(self,name=None):
		return web.seeother('/static/favicon.ico')
	def POST(self,name=None):
		return web.seeother('/static/favicon.ico')

def main():
    app.run()
    pass


if __name__ == '__main__':
    main()
