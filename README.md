# DIM Name Gen DS

A utility to generate Bandai Vital Bracelet compatible name sprites.

There are three fonts available at this time:
1. DigiScript - a reconstructed font created by me, based off of the official English stage names on the VB
2. Official Bandai font - used in the localized versions of the DIMS
3. Agero - a font used in English name sprites in the Digimon Link project for the VB

Running the utility will bring up a prompt to type a name. Type in a name and hit enter or click submit. The generated name in the chosen font will be saved into an output folder created on the Desktop. (For Windows users who have their Desktop synced with OneDrive, the output folder will appear in the local Desktop located at C:/Users/~/Desktop.)

This utility was written in python and compiled into a stand-alone Windows .exe app with pyinstaller and into a stand-alone macOS app with py2app. If using the standalone apps, Python3 and all its required libs are bundled. If you are running the script directly, you will need Python3, Pillow, and tkinterdnd2 installed.

<br/>

## To use the python script:

1. Download the DIMNameGen-DS_v1.x.x.zip from the releases page. Extract the files to any folder.
2. You will need an install of python3, either from https://www.python.org/, from the Windows Store, or using homebrew (macOS).
3. Once python is installed you will need to install the Pillow and tkinterdnd2 dependencies. 
    - On Windows, open Command Prompt and type `pip install Pillow` and `pip install tkinterdnd2`. 
    - On macOS, open Terminal and type `pip3 install Pillow` and `pip3 install tkinterdnd2`.
4. Once Pillow and tkinterdnd2 are installed you can run the script from Command Prompt/Terminal. CD to DIMNameGen-DS_v1.x.x folder and run the script with `python DIMNameGenDS.py` (Win) or `python3 DIMNameGenDS.py` (macOS).

<br />

## To compile:
Download v1.x.x.zip and extract the files anywhere.
- On Windows, cd to DimNameGen-DS_v.1.x.x folder and type `pyinstaller DIMNameGenDS.spec`.
- On macOS, cd to DimNameGen-DS_v.1.x.x folder and type `python3 setup.py py2app`. You may get a "Cannot sign bundle" error. Sign the app with `codesign --force --deep --sign - "dist/DIMNameGen DS.app"`

<br />
<br />

## **Release Notes:**

### **--v1.4.0--**
Added the Agero font to the font options. Added a preview feature that shows both a static preview name and a scrolling preview name.

Future updates:

- Update GUI, buttons and font, etc.
- ~~Add a simple GUI~~
- ~~Add multi-font system: DigiScript & Official Bandai fonts~~
- ~~Text file drag and drop for bulk creating names (Win & macOS)~~
- ~~Sprite previews~~
- ~~Add Agero font to font system~~

<br />

### **--v1.3.2--**
Reverted the size of the DigiScript font while maintaining the top margin. Also fixed some spacing issues with the lowercase "g" letter. Generated names in DigiScript are back to the original font size.

Future updates:
- Add Agero font to font system
- Update GUI buttons, etc.
- Sprite previews
- ~~Add a simple GUI~~
- ~~Add multi-font system: DigiScript & Official Bandai fonts~~
- ~~Text file drag and drop for bulk creating names (Win & macOS)~~

<br />

### **--v1.3.1--**
Fixed the the upper margin for the DigiScript font as well as some spacing issues with the lowercase "g" letter. Generated names in DigiScript are slightly smaller font size but still legible.

Future updates:
- Add Agero font to font system
- Update GUI buttons, etc.
- Sprite previews
- ~~Add a simple GUI~~
- ~~Add multi-font system: DigiScript & Official Bandai fonts~~
- ~~Text file drag and drop for bulk creating names (Win & macOS)~~

<br />

### **--v1.3.0--**
Updated font menu to show actual font lettering. Added a drag and drop text feature for bulk name generating, supporting both .txt and .rtf formats. Added a "show output folder" button.

Future updates:
- Add Agero font to font system
- Update GUI buttons, etc.
- Sprite previews
- ~~Add a simple GUI~~
- ~~Add multi-font system: DigiScript & Official Bandai fonts~~
- ~~Text file drag and drop for bulk creating names (Win & macOS)~~

<br />

### **--v1.2.0--**
Added a font menu that allows you to choose between using the DigiScript font or the Official Bandai font. Changed output folder to ~desktop/DIMNameGenDS_output for easier access.

Future updates:
- Text file drag and drop for bulk creating names (Win & macOS)
- Sprite previews
- ~~Add a simple GUI~~
- ~~Add multi-font system: DigiScript & Official Bandai fonts~~

<br />

### **--v1.1.0--**
Added a simple GUI.

Future updates:
- Add multi-font system: DigiScript & Official Bandai fonts
- Text file drag and drop for bulk creating names (Win & macOS)
- Sprite previews
- ~~Add a simple GUI~~

<br />

### **--v1.0.1--**
Added a while loop to the main code so you can generate name after name without having to relaunch the app.

Future updates:
- Add a simple GUI

<br />

### **--v1.0.0--**
Removed the uppercase only font with a new original font called DigiScript.
DigiScript has both uppecase and lowercase inputs and DIM Name Gen will now generate whatever you type with case-sensitivity.

Future Updates:
- Add a simple GUI
