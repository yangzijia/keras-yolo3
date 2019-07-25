import operator

class Frame(object):
    # 不做识别
    CLASSIFY_STATUS_SKIP = 1
    # 识别完成
    CLASSIFY_STATUS_DONE = 5

    def __init__(self, uuid=0):

        self.id = uuid

        self.classify_status = Frame.CLASSIFY_STATUS_SKIP


class Department:  # 自定义的元素
    def __init__(self, id, value):
        self.id = id
        self.value = value


def __rescale_list(input_list, size):
    skip = len(input_list) // size
    output = [input_list[i] for i in range(0, len(input_list), skip)]

    rest = len(output) % size
    real_list = []
    if rest > 0:
        rest_skip = len(output) // rest
        index_list = [i for i in range(0, len(output)+1, rest_skip)][1:]
        for i, val in enumerate(output):
            if i+1 not in index_list:
                real_list.append(val)
    else:
        real_list = output

    return real_list


def rescale_list(input_list, size):
    if len(input_list) <= size or size <= 0:
        return input_list

    # 先把raw list 转化为字典
    skip_list = []
    final_done_list = []
    done_list = []
    result_list = []
    for i, frame in enumerate(input_list):
        if frame.classify_status == Frame.CLASSIFY_STATUS_DONE:
            done_list.append(Department(i, frame))
            final_done_list.append(frame)
        elif frame.classify_status == Frame.CLASSIFY_STATUS_SKIP:
            skip_list.append(Department(i, frame))

    done_len = len(final_done_list)
    if done_len == size:
        return final_done_list
    elif done_len > size:
        return __rescale_list(final_done_list, size)
    elif done_len < size:
        diff_len = size - done_len
        skip_list = __rescale_list(skip_list, diff_len)
        final_list = skip_list + done_list
        cmpfun = operator.attrgetter('id')#参数为排序依据的属性，可以有多个，这里优先id，使用时按需求改换参数即可
        final_list.sort(key=cmpfun)#使用时改变列表名即可

        for depart in final_list:
            result_list.append(depart.value)
        
        return result_list
        

aa = []

for i in range(12, 19):
    frame = Frame(i) 
    if i%5 == 0:
        frame.classify_status = Frame.CLASSIFY_STATUS_DONE
    else:
        frame.classify_status = Frame.CLASSIFY_STATUS_SKIP
    aa.append(frame)

bb = rescale_list(aa, 25)

for b in bb:
    print(b.id, b.classify_status)
