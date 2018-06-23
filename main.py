#encoding=utf-8

import threading
import web
import random
import time
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')

urls = (
    '/', 'indexhandler',
    '/index', 'indexhandler',
    '/next(.*)', 'next',
    '/login', 'login',
    '/favicon.ico', 'icons',
    '/rest', 'rest',
    '/finished', '_finished',
    '/qa(.*)', 'qahandler'
)
app = web.application(urls, globals())
render = web.template.render('templates/')

vocas = []
mutex = threading.Lock()

player_num=2


def load_voca():
    global vocas;
    with open('materia/voca.txt', 'rb') as fb:
        voca_row = fb.read().encode("utf-8").replace('\r', '')
        _vocas = voca_row.split('\n')
        for voca in _vocas:
            each_item = voca.split('----');
            vocas.append(each_item)
            # print(each_item)
        print('DEBUG INFO: ---------------loading vocabulary------------------')



def dump_to_file(file_path='result/dump.txt'):
    mutex.acquire()
    with open(file_path, 'wb') as f:
        f.write('%d\n' % (len(group)));
        for var in group:
            f.write(str(len(var['uid'])) + '&&&-')
            for user in var['uid']:
                f.write(user + '|')
            f.write('&&&-')
            for voca in var['voca']:
                f.write(str(voca) + '|')
            f.write('&&&-')
            for visiable in var['visiable']:
                f.write(visiable + '|')
            f.write('&&&-%d\n' % var['fin_num'])

            for uid in var['uid']:
                user = user_info[uid]
                for v in user['info']:
                    f.write(v)
                    f.write('|')
                f.write('&&&-')
                for v in user['fin']:
                    f.write(str(v) + '|')
                f.write('&&&-')

                for v in user['unfin']:
                    f.write(str(v) + '|')
                f.write('&&&-')

                for v in user['on_learn']:
                    f.write(str(v) + '|')
                f.write('&&&-')

                for v in user['correct']:
                    f.write(str(v) + '|')
                f.write('&&&-')

                for v in user['time_cost']:
                    f.write(str(v) + '|')
                f.write('&&&-%d&&&-%d\n' % (user['group'], user['last_active']))
    mutex.release()

    # g,u=load_from_dump()

    print '\n\n-----------------------------------------DEBUG INFO Compare group:-------------------------------'
    # print g
    print group
    print '************************************************************************************'
    # print u
    #print user_info
    for user_item in user_info:
            print '  ',user_item,'-------',user_info[user_item]
    print '------------------------------------------------------Compare done------------------------------------\n\n'


def load_from_dump(file_path='result/dump.txt'):
    mutex.acquire()
    _group = [{}]
    _user_info = {}

    with open(file_path, 'rb') as f:
        group_num = int(f.readline())
        if group_num == 0:
            mutex.release()
            return _group, _user_info

        for index in range(0, group_num):
            new_gr = {}
            cur = f.readline().strip('\n')
            u_num, uid, voca, visiable, fin_num = cur.split('&&&-')

            visiable=visiable.split('|')
            while '' in visiable:
                visiable.remove('')
            new_gr['visiable'] = visiable

            uid = uid.split('|')
            while '' in uid:
                uid.remove('')
            new_gr['uid'] = uid

            voca = voca.split('|')
            while '' in voca:
                voca.remove('')

            new_gr['voca'] = [int(var) for var in voca]
            new_gr['fin_num'] = int(fin_num)

            _group[index] = new_gr

            for uid in new_gr['uid']:
                cur = f.readline().strip('\n')

                new_uid = {}

                record = cur.split('&&&-')

                new_info = []
                for item in record:
                    item = item.split('|')
                    while '' in item:
                        item.remove('')
                    new_info.append(item)

                label = ['info', 'fin', 'unfin', 'on_learn', 'correct', 'time_cost', 'group', 'last_active']

                for index in range(0, len(label) - 2):
                    new_uid[label[index]] = new_info[index]

                new_uid['group'] = int(new_info[len(label) - 2][0])
                new_uid['last_active'] = int(new_info[len(label) - 1][0])

                for lab in ['fin', 'unfin', 'on_learn', 'correct', 'time_cost']:
                    new_uid[lab] = [int(var) for var in new_uid[lab]]

                _user_info[uid] = new_uid

    mutex.release()
    return _group, _user_info


load_voca()

# user_info={};#info:[],fin:[],unfin:[],on_learn:[],correct:[],time_cost:[],group:int
# group=[{}];
group, user_info = load_from_dump()


# in each group: {uid:[],voca:[],fin_num:int}
# each group contains/selected lot of vocas

def check_time_out():
    cur_timestap=int(time.time())

    user_offline=[]
    for one_group in group:

        if one_group.has_key('uid'):
            for uid in one_group['uid']:
                if cur_timestap - user_info[uid]['last_active']>60:
                    user_offline.append(True)
                else:
                    user_offline.append(False)

    if len(user_offline)>0 and not (False in user_offline):
        dump_to_file()
        for uid in group[0]['uid']:
            user_info.pop(uid)

        group[0] = {}

        print 'time out and dump_to_file'

        os.rename('result/dump.txt', 'result/dump.' + str(cur_timestap) + '.fin.txt')
        with open('result/dump.txt', 'w') as f:
            f.write('0')
    pass


def batched_voca(nums=20):
    all_nums = len(vocas)
    selected_num = 0
    batch_ = []

    if all_nums == 0 or nums <= 0:
        return []
    
    if all_nums < nums or nums<5:
        print ('system error in loading vocabulary, you need add more vocabulary before loading...')
    nums -= nums%5

    while selected_num < nums:
        var = random.randint(0, all_nums - 1)
        if var not in batch_:
            batch_.append(var)
            selected_num += 1
    return batch_


def check_and_add_user(user_id):

    available=False
    if len(group) == 0 or user_info[user_id]['group'] == -1:
        if not group[-1].has_key('uid'):
            group[-1]['uid'] = [user_id]
            group[-1]['voca'] = batched_voca();
            group[-1]['fin_num'] = 0
            group[-1]['visiable'] = []
            index = 0
            available=True
            for v in group[-1]['voca']:
                index += 1
        elif ((user_id not in group[-1]['uid']) and (len(group[-1]['uid']) < player_num)):
            group[-1]['uid'].append(user_id)
            available=True
            if len(group[-1]['uid']) == player_num:
                group[-1]['visiable']=[var for var in group[-1]['uid']]
                while len(group[-1]['visiable'])*2 > len(group[-1]['uid']):
                    group[-1]['visiable'].pop(random.randint(0,len(group[-1]['visiable'])-1))
                    pass
        #dump_to_file()

    return available, 0


def learn(uid,time_cost=-1):
    if len(user_info[uid]['on_learn']) == 0 and \
            len(user_info[uid]['unfin']) == 0 and \
            len(user_info[uid]['fin']) >= 0:
        finished(uid)
        return render.finished(uid,10)
        #return web.seeother('/')
    if time_cost>0:
        user_info[uid]['time_cost'].append(time_cost)

    if len(user_info[uid]['on_learn']) == 5:
        vvv = []
        for var in user_info[uid]['on_learn']:
            vvv.append(vocas[var])
        dump_to_file()

        return render.test(vvv, uid, 30)

    this_index = random.randint(0, len(user_info[uid]['unfin']) - 1)
    this_var = user_info[uid]['unfin'][this_index]
    user_info[uid]['on_learn'].append(this_var)
    user_info[uid]['unfin'].remove(this_var)
    dump_to_file()
    return render.learn(vocas[this_var], 10, uid);


def unillegal(data={}):
    if (not data.has_key('uid')) or \
            (data['uid'] is None) or \
            len(data['uid']) == 0 or \
            (not user_info.has_key(data['uid'])):
        return True
    cur_timestap = int(time.time())
    gid = user_info[data['uid']]['group']

    some_one_has_dead = False
    for uid in group[gid]['uid']:
        print cur_timestap - user_info[uid]['last_active']
        if cur_timestap - user_info[uid]['last_active'] > 100:
            # default time-out is 3 min.
            some_one_has_dead = True
            break;

    if some_one_has_dead:
        for uid in group[gid]['uid']:
            user_info.pop(uid)

        group[gid] = {}

        print group
        #print user_info
        for user_item in user_info:
            print ('  ',user_item,'-------',user_info[user_item])

        os.rename('result/dump.txt', 'result/dump.' + str(cur_timestap) + '.failed.txt')
        with open('result/dump.txt', 'w') as f:
            f.write('0')

        return True

    print group
    print user_info

    user_info[data['uid']]['last_active'] = int(time.time())
    dump_to_file()
    return False


def finished(uid):
    gid = user_info[uid]['group']

    group[gid]['fin_num'] += 1
    dump_to_file()
    if group[gid]['fin_num'] == player_num:
        os.rename('result/dump.txt', 'result/dump.' + str(int(time.time())) + '.fin.txt')
        with open('result/dump.txt', 'w') as f:
            f.write('0')
        for uid in group[gid]['uid']:
            user_info.pop(uid)
        group[gid] = {}

    print group
    print user_info


class login:
    global user_info;

    def GET(self, name=None):
        # print('not interested in ...')
        return web.seeother('/');
        pass

    def POST(self, name=None):
        check_time_out()

        data = web.input();

        if user_info.has_key(data['uid']):
            return ('already in recorded, choose another username...')
        else:
            user_info[data['uid']] = {
                'info': [data['uid'], data['maj'], data['age'], data['grad'], data['gend']],
                'fin': [], 'unfin': [], 'on_learn': [], 'correct': [], 'time_cost': [], 'group': -1,
                'last_active': int(time.time())
            }
        res, gid = check_and_add_user(data['uid'])
        if res:
            user_info[data['uid']]['group'] = gid
            user_info[data['uid']]['unfin'] += group[gid]['voca']
            user_info[data['uid']]['last_active'] = int(time.time())
            dump_to_file()
            return learn(data['uid']);
        user_info.pop(data['uid'])
        #dump_to_file()
        return 'this batch is fulled, please wait for next batch!'
        pass


class indexhandler:
    def GET(self):
        return render.login()

    def POST(self):
        return render.index()
        pass

class qahandler:
    def GET(self,name='Nothing'):
        print 'in qa', name
        return render.qa(None,'yy',100)
    def POST(self,name='test'):
        print 'in qa post', name
        data = web.input()
        print data
        return render.qa(None,'yy',100)

def score(L=[0, 0, 0, 0, 0], last_round=5):
    total_score = 0
    current_score = 0
    for a in L:
        total_score += a
    r = -1
    for a in range(0, last_round):
        current_score += L[r]
        r -= 1
    return total_score, current_score


class rest:
    def GET(self, name=None):
        return web.seeother('/');

    def POST(self, name=None):
        data = web.input()

        if unillegal(data):
            # print('unillegal user info')
            return render.login()

        # print data['uid']
        user_group = group[user_info[data['uid']]['group']]['uid']
        # print user_group

        if len(user_group) < player_num:
            return render.rest([[1, 2], [2, 3], [3, 4], [5, 6], [6, 7]], data['uid'], 10);
            pass

        jueged = len(user_info[data['uid']]['correct'])
        score_all = []

        for var in user_group:
            if jueged != len(user_info[var]['correct']):
                return render.rest([[1, 2], [2, 3], [3, 4], [5, 6], [6, 7]], data['uid'], 3);
            total_score, current_score = score(user_info[var]['correct'])
            total_time, current_time = score(user_info[var]['time_cost'])
            score_all.append([var, current_score, total_score, current_time, total_time])

        # print score_all

        rank_info = '['
        index = 1
        while len(score_all) != 0:
            min_score = -1
            last_one = None
            for x in score_all:
                if min_score < x[2]:
                    last_one = x
                    min_score = x[2]
                    # find max one

            rank_info += '[' + str(index) + ',' + "'" + last_one[0] + "'," + str(last_one[1]) + ',' + str(
                last_one[2]) +  ',' + str(last_one[3]) +',' + str(last_one[4]) +'],'
            index += 1
            score_all.remove(last_one)
        # rank_info=str(rank_info)
        rank_info = rank_info[:-1] + ']'

        # print rank_info
        if data['uid'] not in group[user_info[data['uid']]['group']]['visiable']:
            total_score, current_score = score(user_info[data['uid']]['correct'])
            total_time, current_time = score(user_info[data['uid']]['time_cost'])
            rank_info="[['unseen','"+data['uid'] + "','" +str(current_score) + "','" + str(total_score) + "','" + str(current_time) + "','" + str(current_time) + "']]"

        return render.backward('nothing', rank_info, data['uid'], 15);


class next:
    def GET(self, name):
        # print(name)
        data = web.input()

        if unillegal(data):
            # print('unillegal user info')
            return render.login()

        # print(data['uid'],data['voca_item'])
        for val in data:
            print(type(val), val, data[val])

        time_cost=-1
        if 'time_cost' in data:
            time_cost=int(data['time_cost'])

        return learn(data['uid'],time_cost)

    def POST(self, name):  # special work for test
        # print('in post function name=',name)
        data = web.input();

        if unillegal(data):
            # print('unillegal user info')
            return render.login()

        # print type(data['voc_1'].encode("utf-8")), data['voc_1'],'-----', vocas[user_info[data['uid']]['on_learn'][0]]
        # print type(data['voc_1'].encode("utf-8")), data['voc_2'],'-----', vocas[user_info[data['uid']]['on_learn'][1]]
        # print type(data['voc_1'].encode("utf-8")), data['voc_3'],'-----', vocas[user_info[data['uid']]['on_learn'][2]]
        # print type(data['voc_1'].encode("utf-8")), data['voc_4'],'-----', vocas[user_info[data['uid']]['on_learn'][3]]
        # print type(data['voc_1'].encode("utf-8")), data['voc_5'],'-----', vocas[user_info[data['uid']]['on_learn'][4]]

        # print(data['uid'].encode("utf-8"))

        current_score = 0
        if data['voc_1'] == vocas[user_info[data['uid']]['on_learn'][0]][0]:
            user_info[data['uid']]['correct'].append(1)
            current_score += 1
        else:
            user_info[data['uid']]['correct'].append(0)

        if data['voc_2'] == vocas[user_info[data['uid']]['on_learn'][1]][0]:
            user_info[data['uid']]['correct'].append(1)
            current_score += 1
        else:
            user_info[data['uid']]['correct'].append(0)

        if data['voc_3'] == vocas[user_info[data['uid']]['on_learn'][2]][0]:
            user_info[data['uid']]['correct'].append(1)
            current_score += 1
        else:
            user_info[data['uid']]['correct'].append(0)

        if data['voc_4'] == vocas[user_info[data['uid']]['on_learn'][3]][0]:
            user_info[data['uid']]['correct'].append(1)
            current_score += 1
        else:
            user_info[data['uid']]['correct'].append(0)

        if data['voc_5'] == vocas[user_info[data['uid']]['on_learn'][4]][0]:
            user_info[data['uid']]['correct'].append(1)
            current_score += 1
        else:
            user_info[data['uid']]['correct'].append(0)

        total_score = 0
        for var in user_info[data['uid']]['correct']:
            total_score += var

        # print current_score,'-----', total_score

        voca_id = user_info[data['uid']]['on_learn'][-1];

        user_info[data['uid']]['fin'] += user_info[data['uid']]['on_learn'];
        del user_info[data['uid']]['on_learn'][:];

        # print(user_info[data['uid']])

        dump_to_file()

        return render.rest([[1, 2], [2, 3], [3, 4], [5, 6], [6, 7]], data['uid'], 2)


class icons:
    def GET(self, name=None):
        return web.seeother('/static/favicon.ico')

    def POST(self, name=None):
        return web.seeother('/static/favicon.ico')

class _finished:
    def GET(self, name=None):
        return render.finished('test',10)
    def POST(self, name=None):
        return seeother('/')

def main():
    print '...............................start................................................\n\n'
    app.run()
    pass


if __name__ == '__main__':
    main()
