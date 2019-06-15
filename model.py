#!/usr/bin/env python
#-*- coding:utf8 -*-
# Power by GJT

import paddle.fluid as fluid


"""
    多模型学习，暂时还没完成。。有空再修改
"""
class model():

    def __init__(self,class_dim_1,class_dim_2,data,label):
        # 少类别CNN
        self.label1_cnn = cnn_net(data,label,class_dim_1)
        # 多类别CNN
        self.label2_cnn = cnn_net(data,label,class_dim_2)
        # 模型合并
        concat_list = [self.label1_cnn,self.label2_cnn]
        # 模型连接
        self.model = fluid.layers.concat(input=concat_list)
        self.prediction = fluid.layers.fc(self.model,size=10)

        return self.prediction


    def cnn_net(self,data,
                label,
                dict_dim,
                class_dim,
                emb_dim=128,
                hid_dim=128,
                hid_dim2=128,
                win_size=3,
                is_infer=False):
        # embedding layer
        emb = fluid.layers.embedding(input=data, size=[dict_dim, emb_dim])
        # convolution layer
        conv_3 = fluid.nets.sequence_conv_pool(
            input=emb,
            num_filters=hid_dim,
            filter_size=win_size,
            act="relu",
            pool_type="max")
        # full connect layer
        fc_1 = fluid.layers.fc(input=[conv_3], size=hid_dim2)
        param_attrs = fluid.ParamAttr(name="fc_weight",
                            regularizer=fluid.regularizer.L2DecayRegularizer(0.1))
        # softmax layer
        prediction = fluid.layers.fc(input=[fc_1], size=class_dim, act="softmax",param_attr=param_attrs)

        return prediction