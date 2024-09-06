# VSY | ВСЕДЪРЖЕЦ

* 6.9.2024

Tesseract and Pytesseract

https://github.com/UB-Mannheim/tesseract/wiki
https://stackoverflow.com/questions/46140485/tesseract-installation-in-windows

https://github.com/Twenkid/ComputerVision_Pyimagesearch_OpenCV_Dlib_OCR-Tesseract-DL/blob/0c1610f7a522f9f3fae75fa3793f8043e52b7bb8/pyimage/ocr_tesseract/ocr.py
https://raw.githubusercontent.com/Twenkid/ComputerVision_Pyimagesearch_OpenCV_Dlib_OCR-Tesseract-DL/0c1610f7a522f9f3fae75fa3793f8043e52b7bb8/pyimage/ocr_tesseract/ocr_tesseract_read_paths.txt

Adjust:
```
C:\Users\_USERNAME_\AppData\Local\Programs\Python\Python39\Lib\site-packages\pytesseract\pytesseract.py

#tesseract_cmd = 'tesseract'
tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

```

Or add to PATH
(Start->Performance... or import os; os.env. ... )

py39 ocr.py -i z:\i5.jpg
#tesseract_cmd= C:\Program Files\Tesseract-OCR\tesseract.exe
print(...) out.txt ..
