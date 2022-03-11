import re

headerStr = '''
Cookie: partner=www_baidu_com; privacy=1646901513; guid=525a26680b65dbdc7d66ac5731ba94d4; _ujz=MTE5ODA5MDY4MA%3D%3D; ps=needv%3D0; 51job=cuid%3D119809068%26%7C%26cusername%3DoCb1tjRgY6YJfZhC%252BaGbiHdHTJVz6A83g3hiq91DlS0%253D%26%7C%26cpassword%3D%26%7C%26cname%3DBqsrJLJyQv%252FpAXXFE9gutw%253D%253D%26%7C%26cemail%3DJ5%252BFrwLJnPDCk0J9ULel1WbaLINjrGFAS1NCfZJ%252B%252Bss%253D%26%7C%26cemailstatus%3D3%26%7C%26cnickname%3D%26%7C%26ccry%3D.0E32uEq7S%252Fps%26%7C%26cconfirmkey%3DsusZmAPbfBWbA%26%7C%26cautologin%3D1%26%7C%26cenglish%3D0%26%7C%26sex%3D0%26%7C%26cnamekey%3DsuwuP%252FdZxo6D.%26%7C%26to%3D456eb4d89dd23b760fe32bae830511ac6229b910%26%7C%26; slife=lowbrowser%3Dnot%26%7C%26lastlogindate%3D20220310%26%7C%26securetime%3DV2sGMwNhBWdeNVRqWGIBb1RlATY%253D; nsearch=jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D; search=jobarea%7E%60000000%7C%21ord_field%7E%600%7C%21recentSearch0%7E%60000000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%D3%CE%CF%B7%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21

'''
ret = ""
for i in headerStr:
    if i == '\n':
        i = "',\n'"
    ret += i
ret = re.sub(": ", "': '", ret)
print(ret[3: -3])


