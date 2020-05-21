import unittest
import zipfly
import os

directory = os.getcwd()
list1 = []

p1 = os.getcwd()
p2 = os.getcwd()
p3 = os.getcwd()


idx1 = p1.rfind("/zipfly")
p1 = p1[0:idx1]
p1 = p1+"/dist/"

idx2 = p2.rfind("/zipfly")
p2 = p2[0:idx2]
p2 = p2+"/zipfly.egg-info/"

idx3 = p3.rfind("/zipfly")
p3 = p3[0:idx3]
p3 = p3+"/examples/"

paths1 = []
paths2 = []
paths3 = []

for dirpath, dnames, fnames in os.walk(p1):
    for f in fnames:
        paths1.append(
            {
                'fs':'{}{}'.format(p1,f),
                'n':'{}{}'.format(p1,f),
            }
        )

for dirpath, dnames, fnames in os.walk(p2):
    for f in fnames:
        paths2.append(
            {
                'fs':'{}{}'.format(p2,f),
                'n':'{}{}'.format(p2,f),
            }
        )

for dirpath, dnames, fnames in os.walk(p3):
    for f in fnames:
        paths3.append(
            {
                'fs':'{}{}'.format(p3,f),
                'n':'{}{}'.format(p3,f),
            }
        )    




class TestBufferPredictionSize(unittest.TestCase):

    def test_paths1(self):

        for test_n in range(1, 5):

            with self.subTest(i=test_n):
            
                storesize = 0
                for path in paths1:
                    f = open(path['fs'], 'rb')
                    storesize += os.fstat(f.fileno()).st_size
                    f.close()

                zfly = zipfly.ZipFly( paths = paths1, storesize = storesize )

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

    def test_paths2(self):

        for test_n in range(1, 5):

            with self.subTest(i=test_n):
            
                storesize = 0
                for path in paths2:
                    f = open(path['fs'], 'rb')
                    storesize += os.fstat(f.fileno()).st_size
                    f.close()

                zfly = zipfly.ZipFly( paths = paths2, storesize = storesize )

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

    def test_paths3(self):

        for test_n in range(1, 5):

            with self.subTest(i=test_n):
            
                storesize = 0
                for path in paths3:
                    f = open(path['fs'], 'rb')
                    storesize += os.fstat(f.fileno()).st_size
                    f.close()

                zfly = zipfly.ZipFly( paths = paths3, storesize = storesize )

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

