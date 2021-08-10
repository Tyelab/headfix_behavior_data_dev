from skimage import io
import daisy
import glob
import numpy as np
import os
import sys

#example voxel size
voxel_size = daisy.Coordinate((60, 56, 56))
raw_dir = sys.argv[1]
out_file = sys.argv[2]

def get_total_roi(image_dir):

    # load images
    files = glob.glob(os.path.join(image_dir, '*.png'))

    # sort, get indices
    section_numbers = sorted([ int(f.split('/')[-1][0:5]) for f in files ])

    # get begining, end
    begin = min(section_numbers)
    end = max(section_numbers) + 1

    # get shape of image
    shape_yx = np.array(io.imread(files[0])).shape

    # create roi for image
    roi = daisy.Roi(
        (0, 0, 0),
        voxel_size*(end - begin, shape_yx[0], shape_yx[1]))

    print("Total ROI: %s" % roi)

    return roi, begin

def fill_section(ds, image_dir, block, image_index_offset=0):

    # 0-based image index
    image_index = block.read_roi.get_offset()[0]/ds.voxel_size[0]
    image_index += image_index_offset

    #load image
    image_file = os.path.join(
        image_dir,
        "%05d.png" % image_index)

    print("Copying section %d..." % image_index)

    try:
        #read data as np array
        data = np.array(io.imread(image_file))[np.newaxis,:]

        #write data to block in write roi
        ds[block.write_roi] = data

    except IOError:
        print("Skipping section %d, image file does not exist." % image_index)
        pass

if __name__ == "__main__":

    total_roi, image_index_offset = get_total_roi(raw_dir)

    # prepare output dataset
    # write size = chunk size. here each chunk is equal to one section in z
    raw_ds = daisy.prepare_ds(
        out_file,
        'volumes/raw',
        total_roi=total_roi,
        voxel_size=voxel_size,
        write_size=voxel_size*(1, 256, 256),
        dtype=np.uint8)

    # get section roi
    section_roi = daisy.Roi(
        (0, 0, 0),
        (voxel_size[0],) + total_roi.get_shape()[1:])

    print("Copying in chunks of %s" % section_roi)

    # distribute worker function (fill section) blockwise
    daisy.run_blockwise(
        total_roi=total_roi,
        read_roi=section_roi,
        write_roi=section_roi,
        process_function=lambda b: fill_section(
            raw_ds,
            raw_dir,
            b,
            image_index_offset),
        num_workers=40)
