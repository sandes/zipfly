import unittest
import zipfly
import os


paths = []

for dirpath, dnames, fnames in os.walk("../dist/"):
    for f in fnames:
        paths.append({'fs':'../dist/{}'.format(f)})

for dirpath, dnames, fnames in os.walk("../zipfly.egg-info/"):
    for f in fnames:
        paths.append({'fs':'../zipfly.egg-info/{}'.format(f)})

for dirpath, dnames, fnames in os.walk("../examples/"):
    for f in fnames:
        paths.append({'fs':'../examples/{}'.format(f)})        

for path in paths:
    path['n'] = path['fs']


class TestBufferPredictionSize(unittest.TestCase):

    def test_size(self):

        for test_n in range(1, 100):

            with self.subTest(i=test_n):
            
                storesize = 0
                for path in paths:
                    f = open(path['fs'], 'rb')
                    storesize += os.fstat(f.fileno()).st_size
                    f.close()

                zfly = zipfly.ZipFly( paths = paths, storesize = storesize )

                # zip size before creating it in bytes
                ps = zfly.buffer_prediction_size()

                with open("test{}.zip".format(test_n), "wb") as f:
                    for i in zfly.generator():
                        f.write(i)

                f = open("test{}.zip".format(test_n), 'rb')
                zs = os.fstat(f.fileno()).st_size
                f.close()

                print ("FINAL SIZE vs PREDICTION:", zs, "--", ps, (" ---- OK" if zs==ps else "FAIL"))

                self.assertEqual(zs,ps)    


if __name__ == '__main__':
    
    unittest.main()