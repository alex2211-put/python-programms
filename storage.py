import os
import tempfile
import json
import argparse
from pathlib import Path


storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')

if not os.path.exists(storage_path):
    Path(storage_path).touch()

parser = argparse.ArgumentParser()
parser.add_argument("--key", type=str)
parser.add_argument("--val")
args = parser.parse_args()

if args.val:
    if(os.stat(storage_path).st_size == False):
        d = {args.key: (args.val, )}
        with open(storage_path, "w") as f:
            f.write(json.dumps(d, ensure_ascii=False))
    else:
        with open(storage_path, "r") as f:
            d = json.load(f)
            if d.get(args.key) == None:
                d[args.key] = (args.val, )
            else:
                d[args.key].append(args.val)
        with open(storage_path, "w") as f:
            f.write(json.dumps(d, ensure_ascii=False))

elif args.key:
    if not os.path.exists(storage_path):
        print('None')
    elif os.stat(storage_path).st_size == False:
        print('None')
    else:
        with open(storage_path, "r") as f:
            d = json.load(f)
            if not args.key in d:
                print('None')
            else:
                for i in range(len(d[args.key]) - 1):
                    print(d[args.key][i], end=", ")
                print(d[args.key][len(d[args.key]) - 1])
