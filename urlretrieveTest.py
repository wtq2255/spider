import urllib
import os

def reporthook(blocks_read, block_size, total_size):

    if not blocks_read:
        print 'Connection opened'
        return
    if total_size < 0:
        print 'Read %d blocks (%d bytes)' % (blocks_read, blocks_read * block_size)
    else:
        amount_read = blocks_read * block_size
        print 'Read %d blocks, or %d/%d' % (blocks_read, amount_read, total_size)
    return


try:
    filename, msg = urllib.urlretrieve(
        'http://ubmcmm.baidustatic.com/media/v1/0f000nSU81POIIpl8HC4tf.png',
        '/Users/weitianqi/Programs/python/1.png',
        reporthook = reporthook)
    print
    print 'File:', filename
    print 'Headers:'
    print msg
    print 'File exists before cleanup:', os.path.exists(filename)
except Exception, e:
    raise e
finally:
    urllib.urlcleanup()
    print 'File still exists:', os.path.exists(filename)