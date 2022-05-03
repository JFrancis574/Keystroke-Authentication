# Using Keystroke Dynamics to Authenticate a User Based on their Typing

This is the repository for the above project. It involves recording a users keystrokes and being able to ensure that they are who they say they are.


## Requirements and running the program

The project only runs on Windows 10. It has been tested and created on python 3.9 and as such has only been guarenteed to work on this version. The program requires the user to have admin priviliges and as such will not work on university computers.
Inside [Code/Application/dist](Code/Application/dist) is an executable called main.exe which will work without python and is the executable for the project. [Code/Application](Code/Application) contains the source code for the project. In order to run it from the source code simply run the [main.py](Code/Application/main.py) file. In order to do this, the following packages are required.

| Package      | Version |
| ----------- | ----------- |
| fastdtw    | 0.3.4 |
| keyboard   | 0.13.5 |
| numpy      | 1.22.3 |
| pip        | 20.2.3 |
| scipy      | 1.8.0 |
| setuptools | 9.2.1 |
| json | any |

Files under [Code/Test code](Code/Test code) may require further packages and are deprecated.

Inside [Code/Application](Code/Application) there is a make.bat file which can be used to create your own executable. The first step is to delete the build and dist folders along with their contents. This is in order to allow the directory to refresh. In order to do this, install the packages above along with pyinstaller and then run the file. This will output the produced executable inside the dist folder.

When running the program, it will create a folder called Data in which the created word and profile files will be stored in whatever the working directory is.

## Repository map
<pre>
📦jtf10
 ┣ 📂Code
 ┃ ┣ 📂Application
 ┃ ┃ ┣ 📂build
 ┃ ┃ ┃ ┗ 📂main
 ┃ ┃ ┃ ┃ ┣ 📜Analysis-00.toc
 ┃ ┃ ┃ ┃ ┣ 📜EXE-00.toc
 ┃ ┃ ┃ ┃ ┣ 📜PKG-00.toc
 ┃ ┃ ┃ ┃ ┣ 📜PYZ-00.pyz
 ┃ ┃ ┃ ┃ ┣ 📜PYZ-00.toc
 ┃ ┃ ┃ ┃ ┣ 📜Tree-00.toc
 ┃ ┃ ┃ ┃ ┣ 📜Tree-01.toc
 ┃ ┃ ┃ ┃ ┣ 📜Tree-02.toc
 ┃ ┃ ┃ ┃ ┣ 📜base_library.zip
 ┃ ┃ ┃ ┃ ┣ 📜main.exe.manifest
 ┃ ┃ ┃ ┃ ┣ 📜main.pkg
 ┃ ┃ ┃ ┃ ┣ 📜warn-main.txt
 ┃ ┃ ┃ ┃ ┗ 📜xref-main.html
 ┃ ┃ ┣ 📂dist
 ┃ ┃ ┃ ┗ 📜main.exe
 ┃ ┃ ┣ 📜Interval.py
 ┃ ┃ ┣ 📜KeyboardClass.py
 ┃ ┃ ┣ 📜Pause.png
 ┃ ┃ ┣ 📜Play.png
 ┃ ┃ ┣ 📜ProfileError.py
 ┃ ┃ ┣ 📜Training.py
 ┃ ┃ ┣ 📜TrainingText.csv
 ┃ ┃ ┣ 📜Word.py
 ┃ ┃ ┣ 📜Words0.json
 ┃ ┃ ┣ 📜Words1.json
 ┃ ┃ ┣ 📜Words2.json
 ┃ ┃ ┣ 📜Words3.json
 ┃ ┃ ┣ 📜keyboardEvent.py
 ┃ ┃ ┣ 📜main.py
 ┃ ┃ ┣ 📜main.spec
 ┃ ┃ ┣ 📜make.bat
 ┃ ┃ ┣ 📜packagesRequired.txt
 ┃ ┃ ┣ 📜tester.py
 ┃ ┃ ┗ 📜user_profile.py
 ┃ ┣ 📂Demo System
 ┃ ┃ ┣ 📂build
 ┃ ┃ ┃ ┗ 📂main
 ┃ ┃ ┃ ┃ ┣ 📜Analysis-00.toc
 ┃ ┃ ┃ ┃ ┣ 📜EXE-00.toc
 ┃ ┃ ┃ ┃ ┣ 📜PKG-00.toc
 ┃ ┃ ┃ ┃ ┣ 📜PYZ-00.pyz
 ┃ ┃ ┃ ┃ ┣ 📜PYZ-00.toc
 ┃ ┃ ┃ ┃ ┣ 📜Tree-00.toc
 ┃ ┃ ┃ ┃ ┣ 📜Tree-01.toc
 ┃ ┃ ┃ ┃ ┣ 📜Tree-02.toc
 ┃ ┃ ┃ ┃ ┣ 📜base_library.zip
 ┃ ┃ ┃ ┃ ┣ 📜main.exe.manifest
 ┃ ┃ ┃ ┃ ┣ 📜main.pkg
 ┃ ┃ ┃ ┃ ┣ 📜warn-main.txt
 ┃ ┃ ┃ ┃ ┗ 📜xref-main.html
 ┃ ┃ ┣ 📂dist
 ┃ ┃ ┃ ┗ 📜main.exe
 ┃ ┃ ┣ 📜Interval.py
 ┃ ┃ ┣ 📜KeyboardClass.py
 ┃ ┃ ┣ 📜Pause.png
 ┃ ┃ ┣ 📜Play.png
 ┃ ┃ ┣ 📜ProfileError.py
 ┃ ┃ ┣ 📜Training.py
 ┃ ┃ ┣ 📜TrainingText.csv
 ┃ ┃ ┣ 📜Word.py
 ┃ ┃ ┣ 📜Words0.json
 ┃ ┃ ┣ 📜Words1.json
 ┃ ┃ ┣ 📜Words2.json
 ┃ ┃ ┣ 📜Words3.json
 ┃ ┃ ┣ 📜keyboardEvent.py
 ┃ ┃ ┣ 📜main.py
 ┃ ┃ ┣ 📜main.spec
 ┃ ┃ ┣ 📜make.bat
 ┃ ┃ ┣ 📜packagesRequired.txt
 ┃ ┃ ┗ 📜user_profile.py
 ┣ 📂Notes
 ┃ ┣ 📂Images
 ┃ ┃ ┣ 📜.DS_Store
 ┃ ┃ ┣ 📜ConfMatrixTest2.jpeg
 ┃ ┃ ┣ 📜CorrGraph.png
 ┃ ┃ ┣ 📜CorrGraph2.png
 ┃ ┃ ┣ 📜DecisionsGraph.png
 ┃ ┃ ┣ 📜DistancesDict.png
 ┃ ┃ ┣ 📜EUCGraph.png
 ┃ ┃ ┣ 📜EUCGraph2.png
 ┃ ┃ ┣ 📜EucVs2D.png
 ┃ ┃ ┣ 📜FolderStruct.png
 ┃ ┃ ┣ 📜GantChartAll.png
 ┃ ┃ ┣ 📜HELLO KDS.png
 ┃ ┃ ┣ 📜IfLen1.png
 ┃ ┃ ┣ 📜KDS1.png
 ┃ ┃ ┣ 📜KDS1DTW.png
 ┃ ┃ ┣ 📜KDS2.png
 ┃ ┃ ┣ 📜KDS2DTW.png
 ┃ ┃ ┣ 📜KDSboth.png
 ┃ ┃ ┣ 📜KDSbothDTW.png
 ┃ ┃ ┣ 📜KeyboardEvent.png
 ┃ ┃ ┣ 📜KeyboardEventPreProc.png
 ┃ ┃ ┣ 📜MathsBackend.png
 ┃ ┃ ┣ 📜NewMaths.png
 ┃ ┃ ┣ 📜OOP.png
 ┃ ┃ ┣ 📜OldPlan.png
 ┃ ┃ ┣ 📜PairingWrong.png
 ┃ ┃ ┣ 📜PauseEx.png
 ┃ ┃ ┣ 📜PlagDec.jpeg
 ┃ ┃ ┣ 📜Play.png
 ┃ ┃ ┣ 📜PlayEx.png
 ┃ ┃ ┣ 📜SemanticsEx.png
 ┃ ┃ ┣ 📜SimplePairing.png
 ┃ ┃ ┣ 📜SystemPlan.png
 ┃ ┃ ┣ 📜Time.png
 ┃ ┃ ┣ 📜UncompressedData.png
 ┃ ┃ ┣ 📜ValidationProc.png
 ┃ ┃ ┣ 📜WordCheck.png
 ┃ ┃ ┗ 📜WordsChosenVsTime.png
 ┃ ┣ 📜.DS_Store
 ┃ ┣ 📜Dissertation Sauce2.aux
 ┃ ┣ 📜Dissertation Sauce2.bbl
 ┃ ┣ 📜Dissertation Sauce2.bcf
 ┃ ┣ 📜Dissertation Sauce2.blg
 ┃ ┣ 📜Dissertation Sauce2.log
 ┃ ┣ 📜Dissertation Sauce2.pdf
 ┃ ┣ 📜Dissertation Sauce2.run.xml
 ┃ ┣ 📜Dissertation Sauce2.synctex.gz
 ┃ ┣ 📜Dissertation Sauce2.tex
 ┃ ┣ 📜Dissertation Sauce2.toc
 ┃ ┣ 📜GantChartAll.gan
 ┃ ┣ 📜GantChartSem1.gan
 ┃ ┣ 📜GantChartSem1.png
 ┃ ┣ 📜GantChartSem2.gan
 ┃ ┣ 📜GantChartSem2.png
 ┃ ┣ 📜Interim Report.docx
 ┃ ┣ 📜Paper and demo notes.pdf
 ┃ ┗ 📜reference.bib
 ┣ 📜.gitignore
 ┗ 📜README.md
 </pre>

## Folder explanation
This section contains a description of the main folders inside the repository.

### TrainingTextCSV
Inside this [file](Code/Application/TrainingText.csv) is the training paragraph. This is taken from H. W. Dodge, The geology of Darling State Park. Montpelier: Vermont Geological Survey, 1967. This file is included twice, once in the demo system and once in the actual system.

### Code
Contains all of the code for the project including test code and actual code.

### Application
As explained above, this contains the source code along with the executable inside the dist folder. Included in this directory is a tester file which comprises of some tests that can be run.

### Demo System

Contained inside here is the source code for the demo system along with an executable. The modules needed are the same as above. The only difference between the two systems is that the demo contains print statements throughout which explain what is going on and the locking is turned off.

### Notes
This contains all things dissertation and notes along with it. The dissertation in pdf form, the interim report and all dissertation related files are stored here. As well as these important documents is a number of note files which I created along the way. The source of the dissertation is also here as I wrote it in LaTeX.

### tester
[Code/Application/tester.py](Code/Application/tester.py)
Contains all the code necessary to run the tests in the dissertation. Further packages are required for this. These are listed below:

| Package      | Version |
| ----------- | ----------- |
| fastdtw    | 0.3.4 |
| keyboard   | 0.13.5 |
| numpy      | 1.22.3 |
| pip        | 20.2.3 |
| scipy      | 1.8.0 |
| setuptools | 9.2.1 |
| matplotlib | any |
| sklearn | any |



