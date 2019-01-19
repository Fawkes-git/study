#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2

aruco = cv2.aruco #arucoライブラリ
dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

def arReader():

    img = cv2.imread("test.png")

    corners, ids, rejectedImgPoints = aruco.detectMarkers(img, dictionary) #マーカを検出

    aruco.drawDetectedMarkers(img, corners, ids, (0,255,0)) #検出したマーカに描画する

    cv2.imshow('drawDetectedMarkers', img) #マーカが描画された画像を表示

    cv2.waitKey(0) #キーボード入力の受付


arReader()
