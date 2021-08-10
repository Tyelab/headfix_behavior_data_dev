import glob
import numpy as np
import os
import re
import sys
import zarr
from skimage import io

#path to image directory
base_path = os.path.abspath(sys.argv[1])

#load images
images = glob.glob(os.path.join(base_path, '*.tif'))

#sort order
images.sort(key=lambda f: int(re.sub('\D', '', f)))

raw = []

#load images and append
for i in images:
    print('loading image %s'%i)
    raw.append(io.imread(i))

#convert to array

print('converting to numpy array...')
raw = np.array(raw)

#create output zarr (or n5)
f_out = zarr.open(sys.argv[2], 'w')

ds_out = f_out.create_dataset(
            name='volumes/raw',
            data=raw,
            compressor=zarr.get_codec({
                'id': 'gzip',
                'level': 5}))

#set meta data - example voxel size
# z,y,x for zarr
# x,y,z for n5
ds_out.attrs['resolution'] = [12,12,12]
ds_out.attrs['offset'] = [0,0,0]



