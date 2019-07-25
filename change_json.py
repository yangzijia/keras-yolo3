import json

delete_key = ["box", "UID"]
change_key = ["x1", "x2", "y1", "y2"]

def resolveJson(path):
    file = open(path, "rb")
    fileJson = json.load(file)
    frames = fileJson["frames"]
    return frames

def output():
    new_frames = {}
    frames = resolveJson(path)
    for i, key in enumerate(frames):
        cell_list = []
        for cell in frames[key]:
            # delete key
            for n in delete_key:
                if n in cell:
                    del cell[n]
            # change value
            for c in change_key:
                if c in cell:
                    cell[c] = int(cell[c])
            print(cell)
        new_frames[i] = frames[key]

    # final_str = str(new_frames).replace("\'", "\"")
    with open("testaaa.json", 'a+') as f:
        f.write(json.dumps(new_frames,ensure_ascii = False))



path = r"F:/engyne_work/abnormal_classification_detect/image/20190624_new_sample/绍梦贞/营业厅标注/smz.json"
output()