def Detect(fname):
    from skimage.io import imread
    from skimage.filters import threshold_otsu
    import matplotlib.pyplot as plt
    import os
    from os import listdir
    filename='./'+fname
    #dir_path=r"C:\Users\Arpit\Desktop\arpit\MachineLearning\License plate detection"
    #if filename in listdir(dir_path):
        #filename='./'+fname
        #if fname.endswith('.png'): 
            #filename='./'+fname
        #elif fname.endswith('.jpg'):
            #filename='./'+fname
        #elif fname.endswith('.jpeg'):
            #filename='./'+fname       
        #form=cgi.FieldStorage()
    #fileitem = form['filename']
    #if fileitem.fileitem:
    #fn=os.path.basename(fileitem.fileitem)
    #open('C:/arpit/MachineLearning/License plate detection/'+fn,'wb').write(fileitem.file.read())

    import cv2
    car_image = imread(filename, as_gray=True)


    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.imshow(car_image, cmap="gray")
    threshold_value = threshold_otsu(car_image)
    binary_car_image = car_image > threshold_value
    ax2.imshow(binary_car_image, cmap="gray")


    from skimage import measure
    from skimage.measure import regionprops
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches

    # this gets all the connected regions and groups them together
    label_image = measure.label(binary_car_image)


    plate_dimensions = (0.03*label_image.shape[0], 0.08*label_image.shape[0], 0.15*label_image.shape[1], 0.3*label_image.shape[1])
    plate_dimensions2 = (0.08*label_image.shape[0], 0.25*label_image.shape[0], 0.15*label_image.shape[1], 0.45*label_image.shape[1])
    min_height, max_height, min_width, max_width = plate_dimensions
    plate_objects_cordinates = []
    plate_like_objects = []

    fig, (ax1) = plt.subplots(1)
    ax1.imshow(car_image, cmap="gray")
    flag =0

    for region in regionprops(label_image):

        if region.area < 50:
            continue

    min_row, min_col, max_row, max_col = region.bbox

    region_height = max_row - min_row
    region_width = max_col - min_col

    if region_height >= min_height and region_height <= max_height and region_width >= min_width and region_width <= max_width and region_width > region_height:
        flag = 1
        plate_like_objects.append(binary_car_image[min_row:max_row,
                                  min_col:max_col])
        plate_objects_cordinates.append((min_row, min_col,
                                         max_row, max_col))
        rectBorder = patches.Rectangle((min_col, min_row), max_col - min_col, max_row - min_row, edgecolor="red",
                                       linewidth=2, fill=False)
        ax1.add_patch(rectBorder)


    if(flag == 1):
        pass
        #plt.show()

    if(flag==0):
        min_height, max_height, min_width, max_width = plate_dimensions2
    plate_objects_cordinates = []
    plate_like_objects = []

    fig, (ax1) = plt.subplots(1)
    ax1.imshow(car_image, cmap="gray")
    for region in regionprops(label_image):
        if region.area < 150:
            continue
        min_row, min_col, max_row, max_col = region.bbox
        rt=max_row-min_row
        rh=max_col-min_col
        #if region_height >= min_height and region_height <= max_height and region_width >= min_width and region_width <= max_width and region_width > region_height:
        if rt >= min_height and rt <= max_height and rh >= min_width and rh <= max_width and rh > 1.3*rt :
            plate_like_objects.append(binary_car_image[min_row:max_row,
                                      min_col:max_col])
            plate_objects_cordinates.append((min_row, min_col,
                                             max_row, max_col))
            rectBorder = patches.Rectangle((min_col, min_row), rh, rt, edgecolor="red",
                                           linewidth=2, fill=False)
            ax1.add_patch(rectBorder)
    #plt.show()

    import numpy as np
    from skimage.transform import resize
    from skimage import measure
    from skimage.measure import regionprops
    import matplotlib.patches as patches
    import matplotlib.pyplot as plt
    import DetectPlate
    flag=False
    for i in range(len(plate_like_objects)):
        if flag==False:    
            license_plate = np.invert(plate_like_objects[i])

            labelled_plate = measure.label(license_plate)

            fig, ax1 = plt.subplots(1)
            ax1.imshow(license_plate, cmap="gray")

            character_dimensions = (0.35*license_plate.shape[0], 0.60*license_plate.shape[0], 0.05*license_plate.shape[1], 0.15*license_plate.shape[1])
            min_height, max_height, min_width, max_width = character_dimensions

            characters = []
            counter=0
            column_list = []
            for regions in regionprops(labelled_plate):
                y0, x0, y1, x1 = regions.bbox
                region_height = y1 - y0
                region_width = x1 - x0

            if region_height > min_height and region_height < max_height and region_width > min_width and region_width < max_width:
                roi = license_plate[y0:y1, x0:x1]

                rect_border = patches.Rectangle((x0, y0), x1 - x0, y1 - y0, edgecolor="red",
                                            linewidth=2, fill=False)
                ax1.add_patch(rect_border)

                # resize the characters to 20X20 and then append each character into the characters list
                resized_char = resize(roi, (20, 20))
                characters.append(resized_char)
                flag=True

        #plt.show()

    import pickle
    print("Loading model")
    filename = './trainedModel.sav'
    model = pickle.load(open(filename, 'rb'))
    plate_string=''

    for each_character in characters:
        each_character = each_character.reshape(1, -1)
        result = model.predict(each_character)
        plate_string+=result[0]
    return plate_string
    #print('Predicted license plate')
    #print(plate_string)
