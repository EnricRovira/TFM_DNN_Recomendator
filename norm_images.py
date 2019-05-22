
import numpy as np
import pandas as pd
from keras.preprocessing import image
from keras.applications.imagenet_utils import preprocess_input

def prepareImages(data, step, batch_size = 128, idx = 'id'):
    errors = []

    X_train = np.zeros((batch_size, 100, 100, 3))
    count = 0
    
    for fig in data[idx].loc[(step):(step + batch_size)]:
        count += 1
        try:
            #load images into images of size 100x100x3
            img = image.load_img(path_images + fig + '.jpg', target_size=(100, 100, 3))
            x = image.img_to_array(img)

            X_train[count] = x
            
        except:
            errors.append(fig)
            pass
    
    return X_train

def normalize(data):
    data = data / 255
    return data

def append_text(idx):
    return idx + '.jpg'

def batch_loader(train_df, BATCH_SIZE):
    #BATCH_SIZE = 256
    STEP_SIZE = train_df.shape[0]//BATCH_SIZE
    #GLOBAL_EPOCHS = 2
    total = 0

    print(f'Loading images in {STEP_SIZE} steps..')
        
    total = 0   
    
    """
    for STEP in range(0, STEP_SIZE):
        
        X_data = prepareImages(train_df, total, BATCH_SIZE)
        X_data = normalize(X_data)
        
        autoencoder.fit(X_data, X_data, epochs = 1, batch_size = BATCH_SIZE, 
                callbacks = None, verbose = 0, shuffle=False )
        
        total += BATCH_SIZE
        print(f'Step: {STEP}, Total: {total}')
    """