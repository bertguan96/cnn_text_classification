import paddle.fluid as fluid


def bilstm_net(data, dict_dim, class_dim, emb_dim=128, hid_dim=128, hid_dim2=96, emb_lr=30.0):
    # embedding layer
    emb = fluid.layers.embedding(input=data,
                                 size=[dict_dim, emb_dim],
                                 param_attr=fluid.ParamAttr(learning_rate=emb_lr))

    # bi-lstm layer
    fc0 = fluid.layers.fc(input=emb, size=hid_dim * 4)

    rfc0 = fluid.layers.fc(input=emb, size=hid_dim * 4)

    lstm_h, c = fluid.layers.dynamic_lstm(input=fc0, size=hid_dim * 4, is_reverse=False)

    rlstm_h, c = fluid.layers.dynamic_lstm(input=rfc0, size=hid_dim * 4, is_reverse=True)

    # extract last layer
    lstm_last = fluid.layers.sequence_last_step(input=lstm_h)
    rlstm_last = fluid.layers.sequence_last_step(input=rlstm_h)

    # concat layer
    lstm_concat = fluid.layers.concat(input=[lstm_last, rlstm_last], axis=1)

    # full connect layer
    fc1 = fluid.layers.fc(input=lstm_concat, size=hid_dim2, act='tanh')
    # softmax layer
    prediction = fluid.layers.fc(input=fc1, size=class_dim, act='softmax')
    return prediction
