# AGP-Autopsy-Plugin

**Dataset** 

It is inside results folder.

**Installing** 

Open the Python module library folder using "Tools", "Python Plugins". Copy the module folder into there(which contains ForensicAF.py and SearchResults.xls) and Autopsy should identify and use it next time it loads modules.

**Running the Module** 

Step 1: Select tools->Run Ingest Module

<img width="1634" alt="python plugins" src="https://user-images.githubusercontent.com/54822246/132608878-9d8fee34-10a1-4cbc-bc51-d86bd17c8519.png">

Step 2: Select Artifact Genome Project

<img width="835" alt="usage2" src="https://user-images.githubusercontent.com/54822246/132609183-ccbb15e2-0077-4f29-baf8-432478db1fa3.png">

Step 3: Select whether you want to run it for file artifacts, or Registry Artifacts. And you can also select Whether you want to export files, that is the resulted files will be exported into report folder. Also you can select the number of levels you can traverse ( for ex. /path/1/2/3/4/ , you can traverse 2 levels that is options it tries /path/1/2/3/4 and 1/2/3/4 and 2/3/4) 

Step 4: After running, results should be available in html format

<img width="1635" alt="results" src="https://user-images.githubusercontent.com/54822246/132609492-ee548c48-854b-43e4-8c93-be3ab4051dd8.png">

<img width="1661" alt="results html 2" src="https://user-images.githubusercontent.com/54822246/132609536-8da00941-6726-4603-97ca-84ceb8562b6f.png">


Step 5: Check inside the module folder in python plugins, for the report and results.
