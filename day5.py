def smart_iter(lst):
    i = 0
    while True:
        try:
            yield lst[i]
            i += 1
        except:
            break

with open('input.txt', 'r+') as fp:
    response = fp.read().strip().split('\n\n')
seeds = response[0].split(' ')[1:]
ratios = [res.split('\n') for res in response[1:]]
dic = {_map[0]: [[int(i) for i in ranges.split(' ')] for ranges in _map[1:]] for _map in ratios}
for k,v in dic.items():
    for idx, sub_v in enumerate(v):
        l2, l1, max_val = sub_v
        dic[k][idx] = {'pos': (l1, l1+max_val-1), 'resp': (l2, l2+max_val-1), 'max_val': max_val}
for k,v in dic.items():
    dic[k] = sorted(v, key=lambda x: x['pos'][0])
int_seeds = [int(i) for i in seeds]
seed_range = list(zip(int_seeds[::2], int_seeds[1::2]))
for idx, lmnt in enumerate(seed_range):
    seed_range[idx] = (lmnt[0], lmnt[0]-1+lmnt[1])
dic_keys = list(dic.keys())
dic['seeds'] = {int(s): {k: 0 for k in dic.keys()} for s in seeds}
seed_range_dic = {'seeds': seed_range} | {_map: list() for _map in dic_keys}
problematic = {k: list() for k in seed_range_dic.keys()}

for s, v in dic['seeds'].items():
    position_idx = s
    for route, num in v.items():
        for mapping in dic[route]:
            if mapping['pos'][0] <= position_idx < mapping['pos'][1]:
                out =  position_idx - mapping['pos'][0] + mapping['resp'][0]
                dic['seeds'][s][route] = out
                position_idx = out
                break
        else:
            dic['seeds'][s][route] = position_idx
print(min([z['humidity-to-location map:'] for k,z in dic['seeds'].items()]))

for idx, sv in enumerate(seed_range_dic.items()):
    k, v = sv
    if idx == 7:
        break
    mapping = dic_keys[idx]
    for lower, upper in smart_iter(v):
        for _map in dic[mapping]:
            if _map['pos'][0] <= lower <= _map['pos'][1]:
                if upper <= _map['pos'][1]:
                    new_lower = lower - _map['pos'][0] + _map['resp'][0]
                    new_upper = upper - _map['pos'][0] + _map['resp'][0]
                    seed_range_dic[mapping].append((new_lower, new_upper))
                    break
                elif upper > _map['pos'][1]:
                    new_lower = lower - _map['pos'][0] + _map['resp'][0]
                    new_upper = _map['resp'][1]
                    seed_range_dic[mapping].append((new_lower, new_upper))
                    v.append((_map['pos'][1]+1, upper))
                    break
        else:
            seed_range_dic[mapping].append((lower, upper))
print(sorted(seed_range_dic['humidity-to-location map:'], key=lambda x: x[0])[0][0])