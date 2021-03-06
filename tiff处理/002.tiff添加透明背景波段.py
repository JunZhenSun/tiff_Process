import gdal
import numpy as np


def readTif(fileName):
    dataset = gdal.Open(fileName)
    if dataset == None:
        print(fileName + "文件无法打开")
        return
    im_width = dataset.RasterXSize  # 栅格矩阵的列数
    im_height = dataset.RasterYSize  # 栅格矩阵的行数
    im_bands = dataset.RasterCount  # 波段数
    im_data = dataset.ReadAsArray(0, 0, im_width, im_height)  # 获取数据
    im_geotrans = dataset.GetGeoTransform()  # 获取仿射矩阵信息
    im_proj = dataset.GetProjection()  # 获取投影信息
    im_blueBand = im_data[0, 0:im_height, 0:im_width]  # 获取蓝波段
    im_greenBand = im_data[1, 0:im_height, 0:im_width]  # 获取绿波段
    im_redBand = im_data[2, 0:im_height, 0:im_width]  # 获取红波段

    a = im_blueBand + im_greenBand + im_redBand
    a = ((1 - np.equal(a, 0)) * 255).astype(np.uint16)
    b = np.sum(a)
    new_im_data = np.stack([im_blueBand, im_greenBand, im_redBand, a], axis=0)
    writeTiff(new_im_data, im_width, im_height, im_bands + 1, im_geotrans, im_proj, path="C:/Users/dell/Desktop/3.tif")


def writeTiff(im_data, im_width, im_height, im_bands, im_geotrans, im_proj, path):
    if 'int8' in im_data.dtype.name:
        datatype = gdal.GDT_Byte
    elif 'int16' in im_data.dtype.name:
        datatype = gdal.GDT_UInt16
    else:
        datatype = gdal.GDT_Float32

    if len(im_data.shape) == 3:
        im_bands, im_height, im_width = im_data.shape
    elif len(im_data.shape) == 2:
        im_data = np.array([im_data])
    else:
        im_bands, (im_height, im_width) = 1, im_data.shape
        # 创建文件
    driver = gdal.GetDriverByName("GTiff")
    dataset = driver.Create(path, im_width, im_height, im_bands, datatype)
    if (dataset != None):
        dataset.SetGeoTransform(im_geotrans)  # 写入仿射变换参数
        dataset.SetProjection(im_proj)  # 写入投影
    for i in range(im_bands):
        dataset.GetRasterBand(i + 1).WriteArray(im_data[i])
    del dataset


readTif("D:/data/ndvi/Image20200410-1.tif")
