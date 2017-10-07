# NHKforKindle

## Description:

If someone is having a habit of reading the japanese news from NHK every day, here is a script that I modified to download todays news from NHK Easy in a single clean HTML and than convert it to MOBI format for your Kindle.

Here are the scripts, download the files in a folder and ~~start it with bash file kindle.sh~~. You will need to have in the same folder Kindlegen (https://www.amazon.com/gp/feature.html?docId=1000765211) and also Python3 installed. 
(If you are in Windows OS probably you will have to run manually the python file and then kindlegen with the created .opf file.) 

The MOBI file will have:   
- ~~all 5 news for today in one file~~ 
- depending on `<mth>` specified, will parse the `<mth>`'s news 
- vertical text   
- right to left page flipping   
- furigana   
- correct word recognising for the Kindle japanese dictionaries (if you have paperwhite) 
- shell scripting TODO

## MODIFIED THE CODE FROM THIS REPO: 
(https://github.com/vebaev/NHKforKindle/blob/master/README.md)

Changed it to parse monthly instead of daily
does not support shell script yet, will do so soon

TO USE:

```shell
python3 nhk-easy.py <mth>

# where <mth> is the specified mth 
# year is calculated using the sys clock
```

output of the program should create a dir where the script was ran.

eg: if you ran the python3 script in `~` (home dir for linux/macOS), it should create a folder `yyyy_mm` and would create 2 other files inside the dir with the extensions `.opf` and `.html` respectively.

In order to convert it into a `.mobi` file, you would need `kindlegen`, im not going to explain the how to here, search the interwebs for more information.