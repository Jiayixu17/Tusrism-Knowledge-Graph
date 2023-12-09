import os
import pickle
import tensorflow as tf
from utils import create_model, get_logger
from model import Model
from loader import input_from_line
from train import FLAGS, load_config
import pandas as pd
path='data.xlsx'#批量出来的文件路径
def main(_):
    dfr=pd.read_excel(path)
    lines=dfr['text'].values.tolist()
    results=[]
    config = load_config(FLAGS.config_file)
    logger = get_logger(FLAGS.log_file)
    # limit GPU memory
    tf_config = tf.ConfigProto()
    tf_config.gpu_options.allow_growth = True
    with open(FLAGS.map_file, "rb") as f:
        tag_to_id, id_to_tag = pickle.load(f)
    keys=tag_to_id.keys()
    print(keys)
    labels=['Attraction','Food','City','Service','Accommodation','Country','Shopping','Transportation','Entertainment']
    mapidtolabel={}
    i=0
    while i<len(labels):
        mapidtolabel[i]=[]
        i=i+1

    with tf.Session(config=tf_config) as sess:
        model = create_model(sess, Model, FLAGS.ckpt_path, config, logger)
        for line in lines:
            line=line.strip()
            print(line)
            result = model.evaluate_line(sess, input_from_line(line, FLAGS.max_seq_len, tag_to_id), id_to_tag)
            for label in labels:
                id=labels.index(label)
                labeldata=[]
                for r in result['entities']:
                    if r['type']==label:
                        labeldata.append(r['word'])

                mapidtolabel[id].append(';'.join(labeldata))

            results.append(result['entities'])
            print(result['entities'])
    df=pd.DataFrame()
    df['text']=lines
    i=0
    while i<len(labels):
        df[labels[i]]=mapidtolabel[i]
        i=i+1
    df.to_excel('bert实体抽取结果.xlsx',index=False,encoding='utf-8')
    print('抽取结束，请查看bert实体抽取结果.xlsx！')
if __name__ == '__main__':
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'
    tf.app.run(main)