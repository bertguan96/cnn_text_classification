import numpy as np
import paddle.fluid as fluid
from valid_model_acc import get_acc
import os

# 创建执行器，请用GPU进行预测。
# place = fluid.CUDAPlace(0)
place = fluid.CPUPlace()
exe = fluid.Executor(place)
exe.run(fluid.default_startup_program())
# 保存预测模型路径
save_path = 'infer_model/'

save_result_path = 'datasets\\'


# 从模型中获取预测程序、输入数据名称列表、分类器
[infer_program, feeded_var_names, target_var] = fluid.io.load_inference_model(dirname=save_path, executor=exe)
# 获取数据
def get_data(sentence):
    # 读取数据字典
    with open(save_result_path + 'dict_txt_all.txt', 'r', encoding='utf-8') as f_data:
        dict_txt = eval(f_data.readlines()[0])
    dict_txt = dict(dict_txt)
    # 把字符串数据转换成列表数据
    keys = dict_txt.keys()
    data = []
    strs_list = str(sentence).split()
    for s in strs_list:
        # 判断是否存在未知字符
        if not s in keys:
            s = '<unk>'
        data.append(int(dict_txt[s]))
    return np.array(data, dtype=np.int64)
data = []
for strs in open(save_result_path + 'valid.txt'):
    data1 = get_data(strs)
    data.append(data1)
# 获取每句话的单词数量
base_shape = [[len(c) for c in data]]
# 生成预测数据
tensor_words = fluid.create_lod_tensor(data, base_shape, place)
# 执行预测
result = exe.run(program=infer_program,
                 feed={feeded_var_names[0]: tensor_words},
                 fetch_list=target_var)

# 分类名称

names = ['0','1', '2', '3', '4', '5',

         '6', '7', '8', '9']

res = open(save_result_path + "result.txt","w")

# 获取结果概率最大的label
for i in range(len(data)):
    lab = np.argsort(result)[0][i][-1]
    res.write(str(lab) + "\n")
    res.flush()
    print('预测结果标签为：%d， 名称为：%s， 概率为：%f' % (lab, names[lab], result[0][i][lab]))

# 获得准确率
get_acc()
