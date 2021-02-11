from django.shortcuts import render
from django.http import HttpResponse
import speech_recognition as sr
from collections import defaultdict
import subprocess
import time
# Create your views here.
capitals={'who I am':'My boss Iqbal sir',"name|who are you":"sumbul",
          "Maharashtra":"Mumbai","Jharkhand":"Ranchi","Telangana":"Hyderabad", "Tamilnadu":"Chennai", "Karnataka":"Bengaluru", "Bihar":"Patna",'punjab|hariyana':'Chandigarh'
          ,'Jammu and Kasmir':'srinagar',"India":"Delhi","punjab|Haryana":"chandigarh",
          'hi|hello|hai|hey':'Hi!',"how are you|What's up":'I am Fine'
          ,'notepad':r"C:\\Windows\\System32\\notepad.exe",
          'VLC':r"C:\Program Files\VideoLAN\VLC\vlc.exe", 'Paint':r"C:\Windows\System32\mspaint.exe"}
dic=defaultdict(list)
def speech_to_text(request):
    d = defaultdict(int)
    stopwords=['i','am','is','are']
    r = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            print('speech Anything')
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio,language='en-us',show_all=False)
                print(text)
            # if text == 'close':
            #     return HttpResponse("Okay,bye")
                keys = capitals.keys()
                for i in keys:
                    for char in i.split('|'):
                        for c in char.split(' '):
                            if c.lower() in text.lower() and c.lower() not in stopwords:
                                d[i] += 1
                print(capitals[max(d,key=lambda x:d[x])])


                if 'open' in text:
                    dic[text.split(" ")[-1].upper()]=subprocess.Popen(capitals[max(d,key=lambda x:d[x])])
                    print(dic)
                    proc=""
                    text=""

                 #   return render(request,'index1.html',{'ans':capitals[max(d,key=lambda x:d[x])].split('\\')[-1]})
                if 'close' in text:
                    try:
                        val=dic[text.split(' ')[-1].upper()]
                        print(dic)
                        outs, errs = val.communicate(timeout=0)
                        dic.pop(val)
                        text=""
                    except subprocess.TimeoutExpired:
                        val.kill()
                        outs, errs = val.communicate()
                        dic.pop(val)
                    return render(request, 'index1.html', {'ans':'closed'})
                return render(request,'index1.html',{"ans":capitals[max(d,key=lambda x:d[x])]})
            except:
                #return render(request,'index1.html',{'ans':''})
                pass
        #return render(request,'index1.html',{'ans':'Sorry , please speak clearly'})

def main(request):
    return render(request,'index1.html')