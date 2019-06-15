#!/usr/bin/env python
#-*- coding:utf8 -*-
# Power by GJT


import net
import paddle.fluid as fluid
import os
import shutil
import paddle
import create_data_utils as create_data
import text_reader


BATCH_SIZE = 256

root_path = "datasets\\"


# 定义输入数据， lod_level不为0指定输入数据为序列数据
words = fluid.layers.data(name='words', shape=[1], dtype='int64', lod_level=1)
label = fluid.layers.data(name='label', shape=[1], dtype='int64')

# 获取数据字典长度
dict_dim = create_data.get_dict_len(root_path + 'dict_txt_all.txt')


model = net.cnn_net(words,label,dict_dim)


# 获取损失函数和准确率
cost = fluid.layers.cross_entropy(input=model, label=label)
avg_cost = fluid.layers.mean(cost)
acc = fluid.layers.accuracy(input=model, label=label)

# 获取预测程序
test_program = fluid.default_main_program().clone(for_test=True)

# 定义优化方法 
optimizer = fluid.optimizer.AdamOptimizer(learning_rate=0.001)


# optimizer = fluid.optimizer.AdamOptimizer(learning_rate=0.001,
#                          regularization=fluid.regularizer.L2DecayRegularizer(
#                          regularization_coeff=0.01))
opt = optimizer.minimize(avg_cost)
# 创建一个执行器，CPU训练速度比较慢
# place = fluid.CPUPlace()
# 请用GPU进行计算，CPU运算结果不佳。
place = fluid.CUDAPlace(0)
exe = fluid.Executor(place)

# 进行参数初始化
exe.run(fluid.default_startup_program())

# 获取训练和预测数据   
train_reader = paddle.batch(reader=text_reader.train_reader(root_path +'train_list_end.txt'), batch_size=BATCH_SIZE)
test_reader = paddle.batch(reader=text_reader.test_reader(root_path + 'valid_list_end.txt'), batch_size=BATCH_SIZE)


# 定义输入数据的维度
feeder = fluid.DataFeeder(place=place, feed_list=[words, label])

# 开始训练
# 修改模型迭代次数
for pass_id in range(10):
    # 进行训练
    for batch_id, data in enumerate(train_reader()):
        train_cost, train_acc = exe.run(program=fluid.default_main_program(),
                             feed=feeder.feed(data),
                             fetch_list=[avg_cost, acc])
        
        if batch_id % 40 == 0:
            print('Pass:%d, Batch:%d, Cost:%0.5f, Acc:%0.5f' % (pass_id, batch_id, train_cost[0], train_acc[0]))
           
            # 进行测试
            test_costs = []
            test_accs = []
            for batch_id, data in enumerate(test_reader()):
                test_cost, test_acc = exe.run(program=test_program,
                                              feed=feeder.feed(data),
                                              fetch_list=[avg_cost, acc])
                test_costs.append(test_cost[0])
                test_accs.append(test_acc[0])
            
            # 计算平均预测损失在和准确率
            test_cost = (sum(test_costs) / len(test_costs))
            test_acc = (sum(test_accs) / len(test_accs))
            print('Test:%d, Cost:%0.5f, ACC:%0.5f' % (pass_id, test_cost, test_acc))

    # 保存预测模型
    save_path = 'infer_model/'

    # 删除旧的模型文件
    shutil.rmtree(save_path, ignore_errors=True)

    # 创建保持模型文件目录
    os.makedirs(save_path)

    # 保存预测模型
    fluid.io.save_inference_model(save_path, feeded_var_names=[words.name], target_vars=[model], executor=exe)