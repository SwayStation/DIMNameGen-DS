# DIM Name Gen DS
A utility to generate Bandai Vital Bracelet compatible name sprites.

There are two fonts available at this time:

    1.  DigiScript - a font created by me based on the English stage names on the VB
    2.  Official Bandai font - used in the localized versions of the DIMS

Running the utility by itself will bring up a prompt to type a name. Type in a name and hit enter or click submit. The generated name in the chosen font will be saved into an output folder created on the desktop.

This utility was written in python and converted to a stand-alone macOS app with py2app. If using the standalone macOS app, Python3 and all its required libs are bundled. If you are running the script directly, you will need Python3 and Pillow installed.

To use the python script:

1. Click the green Code button towards the top followed by Download ZIP. Extract the files to any folder.
2. You will need an install of python3. Either from https://www.python.org/ or from the Windows Store.
3. Once python is installed you will need to install the Pillow dependency by opening terminal/command prompt and typing `pip install Pillow` or `pip3 install Pillow`.
4. Once Pillow is installed you can run the script from terminal/command prompt. CD to DIMNameGen-DS_v1.2.0 folder and run the script with `python DIMNameGenDS.py` or `python3 DIMNameGenDS.py`.

<br />
<br />

## **v1.2.0**
Added a font menu that allows you to choose between using the DigiScript font or the Official Bandai Font. 
Changed output folder to ~desktop/DIMNameGenDS_output for easier access.

Future updates:
- ~~Add a simple GUI~~
- ~~Add multi-font system: DigiScript & Official Bandai Font~~
- Text file drag and drop for bulk creating names (Win & macOS)
- Sprite previews

<br />

## **v1.1.0**
Added a simple GUI.

Future updates:
- ~~Add a simple GUI~~
- Add multi-font system: DigiScript & Official Bandai Font
- Text file drag and drop for bulk creating names (Win & macOS)
- Sprite previews

<br />

## **v1.0.1** 
Added a while loop to the main code so you can generate name after name without having to relaunch the app.

Future updates:
- Add a simple GUI

<br />

## **v1.0.0** 
Removed the uppercase only font with a new original font called DigiScript.
DigiScript has both uppecase and lowercase inputs and DIM Name Gen will now output whatever you type with case-sensitivity.

Future Updates:
- Add a simple GUI
