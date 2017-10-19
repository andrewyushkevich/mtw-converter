from os.path import basename
import subprocess
from gdalconst import *
import os
import errno
# import sys


def way_of_converting(mtw_path, formats):
    path_to_save = convert_to_gtiff(mtw_path)
    if formats == '.stl':
        gtiff_to_stl(path_to_save)
    elif formats == '.raw':
        gtiff_to_raw(path_to_save)
    elif formats == '.tif':
        pass
    else:
        print "EXIT"


def convert_to_gtiff(mtw_path):
    path_to_save = get_path(mtw_path)
    mtw_to_float32(mtw_path, path_to_save)
    float32_to_gtiff(path_to_save)

    return path_to_save


def get_path(mtw_path):
    print "Getting path"
    result_path, mtw_name = os.path.split(mtw_path)
    mtw_name = '/' + os.path.splitext(mtw_name)[0]
    result_path = os.path.dirname(mtw_path) + '/convresult' + mtw_name

    try:
        os.makedirs(result_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    return result_path


def mtw_to_float32(mtw_path, path_to_save):
    print "Converting .mtw to float32"
    subprocess.call('gdal_translate -ot Float32 ' +
                    mtw_path + ' ' + path_to_save, shell=True)


def float32_to_gtiff(path_to_save):
    print "Converting float32 to gtiff"
    formats = 'GTiff'
    subprocess.call('gdal_translate -of ' + formats + ' ' +
                    path_to_save + ' ' + path_to_save + '.tiff', shell=True)


def gtiff_to_stl(path_to_save):
    print "Converting gtiff to stl"
    subprocess.call('python phstl.py ' + path_to_save +
                    '.tiff ' + path_to_save + '.stl', shell=True)


def gtiff_to_raw(path_to_save):
    print "Converting gtiff to raw"
    subprocess.call('gdal_translate -ot UInt16 -scale -of ENVI -outsize 257 257 ' +
                    path_to_save + '.tiff ' + path_to_save + '.raw', shell=True)
