from PIL import Image
import requests
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
import imageio
import ast #allows to deal with string as dictionary
import requests
import pandas as pd
import time
import os

def available_datasets_by_time(channel):
    """
    for a given GOES16 channel, retrieves all datasets currently available
    on the RealEarth API
    """

    abi_band2_list = []
    base_url = "https://realearth.ssec.wisc.edu/api/times?products="
    #url = requests.get(base_url + str(channel))
    url = base_url + channel
    r = requests.get(url)
    list_text = ast.literal_eval(r.text)
    for val in list_text.values():
        if val not in abi_band2_list:
            abi_band2_list.append(val)
    return abi_band2_list

def url_list(list_of_times):

    '''
    collects urls using realearth api. simply replaces timestamp using predefined list of times.
    '''

    url_output_list = []
    base_url = "https://realearth.ssec.wisc.edu/api/image?products=G16-ABI-CONUS-BAND02&time="
    #note that retrieved url is for an asymmetrical image, which allows for trimming of the realearth logo.
    end_url = "&center=37.77,-122.41&zoom=9&width=60&height=140"
    for i in list_of_times:
        url_output_list.append(base_url + i + end_url)
    return url_output_list

def reformat_times_raw(input_list):
    '''
    takes as input a time_stamp in format: 20180805.213725, as from unique_time_stamps()
    '''
    output_list = []
    for i in input_list[0]:
        output_list.append(i[0:4] + "-" + i[4:6] + "-" + i[6:8] + "+" + i[9:11] + ":" + i[11:13])

    return output_list

#retrieve a defined set of pngs:

def retrieve_png_from_url(input_url):
    """Given an input url, retrieves a png file as a np array from that url.
    Note that the url is then trimmed to remove the GOES logo, which will allow
    for easier downstream processing"""

    response = requests.get(input_url)
    if response.status_code == 200:
        input_png = Image.open(BytesIO(response.content))
        as_array = np.array(input_png)[:,:,0]
        #trim the realearth logo off:
        new_array = as_array[30:90, :60]
    return new_array

#example GIF construction:

channel = "G16-ABI-CONUS-BAND02"
all_datasets = available_datasets_by_time(channel)
image_times = reformat_times_raw(all_datasets)
input_urls = url_list(image_times)
png_urls = input_urls[230:330]

png_arrays = []
for png in png_urls:
    pic = retrieve_png_from_url(png)
    png_arrays.append(pic)

#save copies of all pngs:

images = []
for image in png_arrays:
    images.append(image)
imageio.mimsave('png_list/test.gif', images)
