#v3.0.1
import unittest
import zipfly
import os


paths = []

for dirpath, dnames, fnames in os.walk("../dist/"):
    for f in fnames:
        paths.append({'fs':f'../dist/{f}'})

for dirpath, dnames, fnames in os.walk("../zipfly.egg-info/"):
    for f in fnames:
        paths.append({'fs':f'../dist/{f}'})

for path in paths:
    path['n'] = path['fs']


class TestBufferPredictionSize(unittest.TestCase):

    def test_size(self):

        storesize = 0
        for path in paths:
            f = open(path['fs'], 'rb')
            storesize += os.fstat(f.fileno()).st_size

        zfly = zipfly.ZipFly( paths = paths, storesize = storesize )

        # zip size before creating it in bytes
        ps = zfly.buffer_prediction_size()

        with open("test.zip", "wb") as f:
            for i in zfly.generator():
                f.write(i)

        f = open('test.zip', 'rb')
        zs = os.fstat(f.fileno()).st_size

        self.assertEqual(zs,ps)    



if __name__ == '__main__':
    unittest.main()

