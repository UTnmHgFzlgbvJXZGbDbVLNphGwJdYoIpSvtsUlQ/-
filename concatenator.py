import tkinter as tk
from PIL import Image
a=tk.Tk()
a.title("Where's My Water? Level Concatenator")
a.resizable(1,0)
b=tk.Frame(a)
b.pack(fill='x')
c=1
d=[]
tk.Label(b,text='Output information').pack(anchor='w',padx=5)
e=tk.Text(b,height=4)
e.pack(fill='x',padx=5)
tk.Label(b,text='The png of the destination level').pack(anchor='w',padx=5)
f=tk.Entry(b)
f.pack(fill='x',padx=5)
tk.Label(b,text='The xml of the destination level').pack(anchor='w',padx=5)
g=tk.Entry(b)
g.pack(fill='x',padx=5)
def add():
 global c
 x=str(c)
 x='th'if len(x)==2and x[0]=='1'else'st'if x[-1]=='1'else'nd'if x[-1]=='2'else'rd'if x[-1]=='3'else'th'
 d.append(tk.Label(b,text='The png of the '+str(c)+x+' source level'))
 d.append(tk.Entry(b))
 d.append(tk.Label(b,text='The xml of the '+str(c)+x+' source level'))
 d.append(tk.Entry(b))
 d[-4].pack(anchor='w',padx=5)
 d[-3].pack(fill='x',padx=5)
 d[-2].pack(anchor='w',padx=5)
 d[-1].pack(fill='x',padx=5)
 c+=1
def delete():
 global c
 if len(d)==8:
  return
 for x in range(4):
  d[-1].destroy()
  d.pop()
 c-=1
def generate():
 try:
  x,y=zip(*[[y,y.size]for x in d[1::4]for y in[Image.open(x.get())]])
  z=list(zip(*y))[1]
  w,y,z=0,z,Image.new('RGB',[y[0][0],sum(z)])
  for u,v in zip(x,y):
   z.paste(u,[0,w])
   w+=v
  z.save(f.get(),'png')
  y=[0,*y]
  w*=0.4
  for x,z in zip(range(1,len(y)),d[3::4]):
   y[x]*=0.4
   w-=y[x-1]+y[x]
   z=open(z.get()).read()
   v=z.find('<Object ')-1
   while z[v]==' ':
    v-=1
   z=z[v+1:z.rfind('</Object>')+9].split('AbsoluteLocation')
   for t in range(1,len(z)):
    u=z[t].split('"',2)
    v=u[1].split()
    v[1]=str(float(v[1])+w)
    u[1]=' '.join(v)
    z[t]='"'.join(u)
   z='AbsoluteLocation'.join(z)
   for s in range(2):
    for t in[['<Object'],['ConnectedConverter','ConnectedObject','ConnectedSpout','Parent']][s]:
     z=z.split(t)
     for u in range(1,len(z)):
      v=z[u]
      if v[0]not in'0123456789" ':
       continue
      v=v.split('"',s+1)
      if v[-1].startswith('SWAMPY_SPOUT'):
       continue
      v[-1]=str(x)+'x'+v[-1]
      z[u]='"'.join(v)
     z=t.join(z)
   y[x-1]=z
  y.insert(0,'<?xml version="1.0"?>\n<Objects>')
  y[-1]='</Objects>'
  open(g.get(),'w').write('\n'.join(y))
  e['fg']='green'
  e.delete('1.0','end')
  e.insert('1.0','Success!')
 except BaseException as x:
  e['fg']='red'
  e.delete('1.0','end')
  e.insert('1.0',x.__class__.__name__+': '+str(x)+' (Error code: '+'8'.join([y.append(w)if w else
[oct(z.tb_lineno)[2:]for z in y]for y in[[x.__traceback__]]for z in y for w in[z.tb_next]][-1])+')')
tk.Button(a,text='Generate',command=generate).pack(anchor='n',side='right',padx=5,pady=5)
tk.Button(a,text='Delete level',command=delete).pack(anchor='n',side='right',pady=5)
tk.Button(a,text='Add level',command=add).pack(anchor='n',side='right',padx=5,pady=5)
add()
add()
a.mainloop()
