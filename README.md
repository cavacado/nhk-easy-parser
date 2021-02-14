# Easy NHK in HTML
## Description:

If someone is having a habit of reading the japanese news from NHK every day, here is a script that I modified to download todays news from NHK Easy in a single clean `HTML`.

The `HTML` file will have:   
- ~~all 5 news for today in one file~~ 
- depending on `<mth>` specified, will parse the `<mth>`'s news 
- vertical text   
- right to left page flipping   
- furigana   

## Usage:

```shell
pip3 install <dependencies>
python3 nhk-easy.py <mth>

# where <mth> is the specified mth 
# year is calculated using the sys clock
```
## References:
- https://github.com/vebaev/NHKforKindle/blob/master/README.md
