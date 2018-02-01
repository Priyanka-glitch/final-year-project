import cv2
import pickle
import numpy as np
import pyautogui as gui

def top(collection, key, n):
    collection = sorted(collection, key = key, reverse = True)
    returnable = []
    for i in range(n):
        returnable.append(collection[i])
    return returnable

def get_keys(frame_width, frame_height):
	"""
	this function is used to design the keyboard.
	it returns the 4 parameter that are needed to design the keys.
	they are key label, top right corner coordinate, bottom left corner coordinate, and center coordinate
	"""
	max_keys_in_a_row = 11						# max number of keys in any row is 10 i.e the first row which contains 1234567890'backspace'
	key_width = int(frame_width/max_keys_in_a_row)	# width of one key. width is divided by 10 as the max number of keys in a single row is 11.
	
	row0_key_width = key_width * 11			# width of zeroth or numeric row of keys
	row1_key_width = key_width * 10			# width of first row
	row2_key_width = key_width * 9			# width of second row
	row3_key_width = key_width * 7			# width of third row
	row4_key_width = key_width * 5			# width of space
	row_keys = []							# stores the keys along with its 2 corner coordinates and the center coordinate

	# for the zeroth row
	x1, y1 = 0, int((frame_height - key_width * 5) / 2)	# 5 is due to the fact that we will have 5 rows. y1 is set such that the whole keyboard has equal margin on both top and bottom
	x2, y2 = key_width + x1, key_width + y1
	c1, c2 = x1, y1					# copying x1, x2, y1 and y2
	keys = "1 2 3 4 5 6 7 8 9 0 <-"
	keys = keys.split(" ")
	for key in keys:
		if key == "<-":
			row_keys.append([key, (x1, y1), (x2, y2), (int((x2+x1)/2) - 25, int((y2+y1)/2) + 10)])
		else:
			row_keys.append([key, (x1, y1), (x2, y2), (int((x2+x1)/2) - 5, int((y2+y1)/2) + 10)])
		x1 += key_width
		x2 += key_width
	x1, y1 = c1, c2					# copying back from c1, c2, c3 and c4

	# for the first row
	x1, y1 = int((row0_key_width - row1_key_width) / 2) + x1, y1 + key_width	
	x2, y2 = key_width + x1, key_width + y1
	c1, c2 = x1, y1					# copying x1, x2, y1 and y2
	keys = "qwertyuiop"
	for key in keys:
		row_keys.append([key, (x1, y1), (x2, y2), (int((x2+x1)/2) - 5, int((y2+y1)/2) + 10)])
		x1 += key_width
		x2 += key_width
	x1, y1 = c1, c2					# copying back from c1, c2, c3 and c4

	# for second row
	x1, y1 = int((row1_key_width - row2_key_width) / 2) + x1, y1 + key_width   # x1 is set such that it leaves equal margin on both left and right side
	x2, y2 = key_width + x1, key_width + y1
	c1, c2 = x1, y1
	keys = "asdfghjkl"
	for key in keys:
		row_keys.append([key, (x1, y1), (x2, y2), (int((x2+x1)/2) - 5, int((y2+y1)/2) + 10)])
		x1 += key_width
		x2 += key_width
	x1, y1 = c1, c2

	# for third row
	x1, y1 = int((row2_key_width - row3_key_width) / 2) + x1, y1 + key_width
	x2, y2 = key_width + x1, key_width + y1	
	c1, c2 = x1, y1	
	keys = "zxcvbnm"
	for key in keys:
		row_keys.append([key, (x1, y1), (x2, y2), (int((x2+x1)/2) - 5, int((y2+y1)/2) + 10)])
		x1 += key_width
		x2 += key_width
	x1, y1 = c1, c2

	# for the space bar
	x1, y1 = int((row3_key_width - row4_key_width) / 2) + x1, y1 + key_width
	x2, y2 = 5 * key_width + x1, key_width + y1	
	c1, c2 = x1, y1	
	keys = " "
	for key in keys:
		row_keys.append([key, (x1, y1), (x2, y2), (int((x2+x1)/2) - 5, int((y2+y1)/2) + 10)])
		x1 += key_width
		x2 += key_width
	x1, y1 = c1, c2

	return row_keys


def do_keypress(img, center, row_keys_points):
	# this fuction presses a key and marks the pressed key with blue color
	for row in row_keys_points:
		arr1 = list(np.int0(np.array(center) >= np.array(row[1])))			# center of the contour has greater value than the top left corner point of a key 
		arr2 = list(np.int0(np.array(center) <= np.array(row[2])))			# center of the contour has less value than the bottom right corner point of a key 
		if arr1 == [1, 1] and arr2 == [1, 1]:
			if row[0] == '<-':
				gui.press('backspace')
			else:
				gui.press(row[0])
			cv2.fillConvexPoly(img, np.array([np.array(row[1]), \
												np.array([row[1][0], row[2][1]]), \
												np.array(row[2]), \
												np.array([row[2][0], row[1][1]])]), \
												(255, 0, 0))
	return img

def start_virtual_mouse():
	from modules.virtual_mouse.virtual_mouse import start_mouse
	start_mouse()

def start_keyboard():
	cam = cv2.VideoCapture(1)
	width = 640	# width of video captured by the webcam
	height = 480	# height of the video captured by the webcam
	cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
	cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
	with open("range.pickle", "rb") as f:		# range.pickle is generated by range-detector.py
	    t = pickle.load(f)
	hsv_lower = np.array([t[0], t[1], t[2]])	
	hsv_upper = np.array([t[3], t[4], t[5]])
	row_keys_points = get_keys(width, height)
	new_area, old_area = 0, 0
	count_frame_area, count_frame_center = 0, 0		# count_frame_area stores the number of iterations for calculating the difference b/w present area and previous area
													# count_frame_center stores the number of iterations for calculating the difference b/w present center and previous center
	flag_keypress = False							# if a key is pressed then this flag is True
	no_finger_count_frame = 0
	flag_start_mouse = False

	while True:
		img = cam.read()[1]
		img = cv2.flip(img, 1)
		imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		mask = cv2.inRange(imgHSV, hsv_lower, hsv_upper)
		blur = cv2.medianBlur(mask, 15)
		blur = cv2.GaussianBlur(blur , (5,5), 0)
		thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
		contours = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[1]

		if len(contours) >= 2:
			no_finger_count_frame = 0
			c1, c2 = top(contours, cv2.contourArea, 2)
			if cv2.contourArea(c1) > 350 and cv2.contourArea(c2) > 350:
				# start virtual mouse
				flag_start_mouse = True
				break
				
				
		elif len(contours) >= 1:
			no_finger_count_frame = 0
			cnt = max(contours, key = cv2.contourArea)
			
			if cv2.contourArea(cnt) > 350:
				# draw a rectangle and a center 
				rect = cv2.minAreaRect(cnt)
				center = list(rect[0])
				box = cv2.boxPoints(rect)
				box = np.int0(box)
				cv2.circle(img, tuple(np.int0(center)), 2, (0, 255, 0), 2)
				cv2.drawContours(img,[box],0,(0,0,255),2)
				
				# calculation of difference of area and center
				new_area = cv2.contourArea(cnt)
				new_center = np.int0(center)
				
				if count_frame_area == 0:
					old_area = new_area
				count_frame_area += 1
				diff_area = 0
				if count_frame_area > 3:								# after every 3rd iteration difference of area is calculated
					diff_area = new_area - old_area
					count_frame_area = 0
				if count_frame_center == 0:
					old_center = new_center
				count_frame_center += 1
				diff_center = np.array([0, 0])
				if count_frame_center > 5:								# after every 5th iteration difference of center is claculated
					diff_center = new_center - old_center
					count_frame_center = 0

				
				# setting some thresholds
				center_threshold = 10
				area_threshold = 150
				if abs(diff_center[0]) < center_threshold or abs(diff_center[1]) < center_threshold:
					print(diff_area)
					if diff_area > area_threshold and flag_keypress == False:
						img = do_keypress(img, new_center, row_keys_points)
						flag_keypress = True
					elif diff_area < -(area_threshold) and flag_keypress == True:
						flag_keypress = False
			else:
				flag_keypress = False
		
		elif len(contours) == 0:
			flag_keypress = False

			# if no finger is found for next 100 frames stop the keyboard 
			if no_finger_count_frame != 100:
				no_finger_count_frame += 1
			else:
				break

		# displaying the keyboard
		for key in row_keys_points:
			cv2.putText(img, key[0], key[3], cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255))
			cv2.rectangle(img, key[1], key[2], (0, 0, 255), thickness = 2)

		cv2.imshow("Virtual Keyboard", img)
		
		if cv2.waitKey(1) == ord('q'):
			break

	cam.release()
	cv2.destroyAllWindows()

	if flag_start_mouse:
		start_virtual_mouse()