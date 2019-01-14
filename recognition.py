'''Number recognition model.'''

from keras.models import model_from_json, Model
from keras.layers import Input, Dense, Dropout, Flatten

import numpy as np
import cv2

class _NumberModel(object):
    '''The recognition model for number 0-9.

    Instance Methods:
        load_model: Load the model.
        predict_number: Prediction.
    '''
    def __init__(self):
        self.__model = None

    @staticmethod
    def __define_model():
        inputs = Input(shape=(28, 28, 1))
        x = Flatten()(inputs)
        x = Dense(512, activation='relu')(x)
        x = Dropout(0.2)(x)
        x = Dense(512, activation='relu')(x)
        x = Dropout(0.2)(x)
        outputs = Dense(11, activation='softmax')(x)
        model = Model(inputs=inputs, outputs=outputs)

        return model

    @staticmethod
    def __resize_image(img):
        h, w = img.shape
        fx, fy = 28.0 / h, 28.0 / w
        fx = fy = min(fx, fy)
        img = cv2.resize(img, None, fx=fx, fy=fy, interpolation=cv2.INTER_CUBIC)
        outimg = np.ones((28, 28), dtype=np.uint8) * 255

        h, w = img.shape
        x, y = (28 - w) // 2, (28 - h) // 2
        outimg[y:y+h, x:x+w] = img

        return outimg

    def load_model(self, weight_path, model_path=None):
        '''Load the model.'''
        # Load model
        if model_path is None:
            self.__model = self.__define_model()
        else:
            print('Loaded model from json.')
            with open(model_path, 'r') as f:
                self.__model = model_from_json(f.read())

        # Load weight
        self.__model.load_weights(weight_path)

        return self.__model

    def predict_number(self, img):
        '''Prediction.'''
        if img is None:
            return None

        img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        _, img_gray = cv2.threshold(img_gray, 200, 255, cv2.THRESH_BINARY)
        kernel = np.ones((3, 3), np.uint8)
        img_gray = cv2.morphologyEx(img_gray, cv2.MORPH_OPEN, kernel)
        img_gray = self.__resize_image(img_gray) # Resizing to 28*28
        img_gray = np.resize(img_gray, (1, 28, 28, 1)) # Expand

        y_pred = self.__model.predict(img_gray)
        y_pred = np.argmax(y_pred)

        return y_pred


_MODEL = _NumberModel()

def load(weight_path, model_path=None):
    '''Load the model.

    Args:
        weight_path: The path of model weight.
        model_path: The path of model json. Pass `None` to build it directly.

    Returns:
        The recognition model.
    '''
    return _MODEL.load_model(weight_path, model_path)

def predict(img):
    '''Prediction.

    Args:
        img: The image of number 0-9.

    Returns:
        The result of recognition.
    '''
    return _MODEL.predict_number(img)

if __name__ == '__main__':
    pass
