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

* Download LSTM models: (may have to rename or move the original)
eng (-en), bul ... etc.
https://github.com/tesseract-ocr/tessdata/tree/main
https://github.com/tesseract-ocr/tessdata/blob/main/bul.traineddata

Save to the dir: (or elsewhere and provide the path)

C:\Program Files\Tesseract-OCR>"C:\Program Files\Tesseract-OCR\tesseract.exe" --tessdata-dir "C:\Program Files\Tesseract-OCR\tessdata" --oem 1 -l bul z:/i2.jpg stdout

--oem 0 legacy
--oem 1 LSTM
--oem 2 what's available

...
https://github.com/tesseract-ocr/tessdata_fast

...
* GOT, OCR-2 tested in Colab T4
Recognizes a lot of doom-like game tests (more pixelated etc.) 

https://huggingface.co/stepfun-ai/GOT-OCR2_0

https://github.com/Ucas-HaoranWei/GOT-OCR2.0/blob/main/GOT-OCR-2.0-paper.pdf
