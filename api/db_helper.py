import psycopg2
import os
import sys

with open( (os.path.join(sys.path[0], 'veri_test_list.txt') ), "r" ) as f:
    content = f.readlines()
names = [x.strip() for x in content] 

with open( (os.path.join(sys.path[0], 'feats_sample.txt') ), "r" ) as f:
    content = f.readlines()
feats = [x.strip() for x in content] 

_feats = []

for feat in feats:
    feat_array = []
    string = feat.strip('[]')
    temp = ''
    for s in string:
        if s == ' ':
            pass
        if s != ',':
            temp += s
        else:
            feat_array.append(float(temp))
            temp = ''
    feat_array.append(float(temp))
    _feats.append(feat_array)


conn = psycopg2.connect("host=localhost dbname=fyp_backend user=postgres password=Pakistan6564!")
cur = conn.cursor()

for i in range(len(names)):
    insert_query = "INSERT INTO api_gallery(name,features) VALUES ('{0}', ARRAY{1})".format(names[i],_feats[i])
    cur.execute(insert_query)
    conn.commit()