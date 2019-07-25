import numpy as np

def txt2boxes(filename):
    # 打开文件
    f = open(filename, 'r')
    dataSet = []
    # 读取文件
    for line in f:
        infos = line.split(" ")
        length = len(infos)
        # infons[0] 为图片的名称
        for i in range(1, length):
            class_id = infos[i].split(",")[4]
            if class_id != "2":
                continue
            # 获取文件的宽和高
            width = int(infos[i].split(",")[2]) - \
                int(infos[i].split(",")[0])
            height = int(infos[i].split(",")[3]) - \
                int(infos[i].split(",")[1])
            dataSet.append([width, height])
    result = np.array(dataSet)
    f.close()
    return result

def main():
    path = "20190624/voc_train.txt"
    result = txt2boxes(path)
    print(len(result))
    temp_list = []
    for r in result:
        if len(temp_list) == 0:
            temp_list.append(r)
        else:
            flag = True
            for tt in temp_list:
                if (r == tt).all():
                    flag = False
                    break
            if flag:
                temp_list.append(r)

            

    print(len(temp_list))

if __name__ == "__main__":
    main()