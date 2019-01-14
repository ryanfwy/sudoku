'''Pre-processing image.'''

import cv2

import recognition
import solution

_WIDTH = 500

def _cut_img(img, bbox):
    '''Crop an image.'''
    x, y, w, h = bbox
    return img[y:y+h, x:x+w]

def _find_larger_cells(img, thresh=0):
    '''Find larger cells.'''
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    _, img_gray = cv2.threshold(img_gray, thresh, 255, cv2.THRESH_BINARY)
    _, contours, _ = cv2.findContours(img_gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    img_cut = []

    for contour in reversed(contours):
        area = cv2.contourArea(contour)
        if not 100 < area < 50000:
            continue # Too large or too small

        bbox = cv2.boundingRect(contour)
        x, y, w, h = bbox
        x, y, w, h = x+2, y+2, w-2, h-2 # Reduce the frame
        if not 0.95 < w / h < 1.05:
            continue # Not rentangle

        img_cut += [_cut_img(img, bbox)]

    return img_cut

def _find_smaller_cells(img, thresh=190):
    '''Find cells in a larger cell.'''
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    _, img_gray = cv2.threshold(img_gray, thresh, 255, cv2.THRESH_BINARY)
    _, contours, _ = cv2.findContours(img_gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    height, width = img_gray.shape
    height_each, width_each = height // 3, width // 3

    img_cut = [None] * 9

    for contour in reversed(contours):
        area = cv2.contourArea(contour)
        if not 100 < area < 1000:
            continue # Too small or too large

        bbox = cv2.boundingRect(contour)
        x, y, w, h = bbox
        x, y, w, h = x-2, y-2, w+2, h+2 # Larger the frame
        if not 0.5*height_each < h < height_each:
            continue # Not a number

        idx = y // height_each * 3 + x // width_each
        img_cut[idx] = _cut_img(img, bbox)

    return img_cut

def run(img_path):
    '''Transfer an image to a sudoku matrix using recognition model.

    Args:
        img_path: The path of the Sudoku image.

    Returns:
        A matrix of sudoku.
    '''
    # Resize
    img = cv2.imread(img_path)
    height, width, _ = img.shape
    img = cv2.resize(img, (_WIDTH, int(_WIDTH*(height/width))))

    # Find cells
    cells_larger = _find_larger_cells(img)

    # Load model
    recognition.load('./model/model.h5')

    mat = [[None] * 9 for _ in range(9)]
    for index_larger, cells in enumerate(cells_larger):
        # Find smaller cells
        cells_smaller = _find_smaller_cells(cells)

        for index_smaller, num in enumerate(cells_smaller):
            row = index_larger // 3 * 3 + index_smaller // 3
            col = index_larger % 3 * 3 + index_smaller % 3
            mat[row][col] = recognition.predict(num)

    return mat

def show(mat, tips=False, answer=False):
    '''Show tips or answer from a sudoku matrix.

    Args:
        mat: A matrix of sudoku.
        tips: Show tips or not.
        answer: Show answer or not.

    Returns:
        None.
    '''
    if tips:
        solution.get_tips(mat)
    if answer:
        solution.get_answer(mat)
    if not tips and not answer:
        solution.print_result(mat)

if __name__ == '__main__':
    run('./assets/demo.png')
