import unittest
import zipfly
import os
import string
import random

def rs(N):
    return ''.join(random.SystemRandom().choice(
                    string.ascii_uppercase + \
                    string.ascii_lowercase + \
                    string.digits) for _ in range(N))

def pick_n():
    return int(''.join(random.SystemRandom().choice(string.digits) for _ in range(3)))

p1 = os.getcwd()
p2 = p1
p3 = p1

"""
idx1 = p1.rfind("/zipfly")
p1 = p1[0:idx1]
p1 = p1+"/dist/"

idx2 = p2.rfind("/zipfly")
p2 = p2[0:idx2]
p2 = p2+"/zipfly.egg-info/"

idx3 = p3.rfind("/zipfly")
p3 = p3[0:idx3]
p3 = p3+"/examples/"

"""
p1 = p1+"/dist/"
p2 = p2+"/zipfly.egg-info/"
p3 = p3+"/examples/"

paths1 = []

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
        paths1.append(
            {
                'fs':'{}{}'.format(p2,f),
                'n':'{}{}'.format(p2,f),
            }
        )

for dirpath, dnames, fnames in os.walk(p3):
    for f in fnames:
        paths1.append(
            {
                'fs':'{}{}'.format(p3,f),
                'n':'{}{}'.format(p3,f),
            }
        )    

class TestBufferPredictionSize(unittest.TestCase):

    def test_buffer_prediction_size(self):

        print (
            """
            TEST IF REAL ZIP SIZE IS EQUAL TO PREDICTION SIZE
            # # # # # # # # # # # # # # # # # # # # # # # # #
            """
        )

        for test_n in range(1, 50):

            with self.subTest(i=test_n):
            
                storesize = 0
                for path in paths1:
                    f = open(path['fs'], 'rb')
                    storesize += os.fstat(f.fileno()).st_size
                    f.close()

                zfly = zipfly.ZipFly( paths = paths1, storesize = storesize )

                zfly.set_comment(rs(pick_n()))

                # zip size before creating it in bytes
                ps = zfly.buffer_prediction_size()

                with open("test{}.zip".format(test_n), "wb") as f:
                    for i in zfly.generator():
                        f.write(i)

                f = open("test{}.zip".format(test_n), 'rb')
                zs = os.fstat(f.fileno()).st_size
                f.close()

                print (
                    "test-{}.zip ->".format(test_n),
                    "{} KB".format(round(zs/1024,2)),
                    "({} bytes)".format(zs),
                    (" ---- OK" if zs==ps else " ---- FAIL")
                )

                self.assertEqual(zs,ps)    
              
                     
if __name__ == '__main__':
    
    unittest.main()

