import json,subprocess,sys
key,src=sys.argv[1],sys.argv[2]
R=json.load(open(f'map_{key}.json'))['ranges']
expr="+".join(f"between(t,{a:.4f},{b-0.001:.4f})" for a,b in R)
fc=f"[0:v]select='{expr}',setpts=N/(30*TB),format=yuv420p[v];[0:a]aresample=48000,pan=stereo|c0=c0|c1=c0,asetnsamples=n=1600,aselect='{expr}',asetpts=N/SR/TB,highpass=f=80,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]"
open(f'fc_base_{key}.txt','w').write(fc)
subprocess.run(["ffmpeg","-y","-v","error","-i","/mnt/user-data/uploads/Alston Wealth Videos/"+src,"-filter_complex_script",f"fc_base_{key}.txt","-map","[v]","-map","[a]","-c:v","libx264","-preset","veryfast","-crf","16","-r","30","-c:a","aac","-b:a","192k",f"base_{key}.mp4"],check=True)
print("BASE",key)
