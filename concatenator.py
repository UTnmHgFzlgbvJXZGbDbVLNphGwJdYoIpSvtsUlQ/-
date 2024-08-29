import tkinter as tk
from PIL import Image
from lxml import etree
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
tk.Label(b,text='The path of the png of the destination level').pack(anchor='w',padx=5)
f=tk.Entry(b)
f.pack(fill='x',padx=5)
tk.Label(b,text='The path of the xml of the destination level').pack(anchor='w',padx=5)
g=tk.Entry(b)
g.pack(fill='x',padx=5)
def add():
 global c
 x=f'{c}'
 x='th'if len(x)==2and x[0]=='1'else'st'if x[-1]=='1'else'nd'if x[-1]=='2'else'rd'if x[-1]=='3'else'th'
 d.append(tk.Label(b,text=f'The path of the png of the {c}{x} source level'))
 d.append(tk.Entry(b))
 d.append(tk.Label(b,text=f'The path of the xml of the {c}{x} source level'))
 d.append(tk.Entry(b))
 d[-4].pack(anchor='w',padx=5)
 d[-3].pack(fill='x',padx=5)
 d[-2].pack(anchor='w',padx=5)
 d[-1].pack(fill='x',padx=5)
 c+=1
def delete():
 global c
 if len(d)!=8:
  for x in range(4):
   d.pop().destroy()
  c-=1
def generate():
 try:
  x,y,s,t=[],[],[],[]
  for z in d[1::4]:
   z=Image.open(z.get())
   x.append(z)
   z=z.size
   y.append(z[1])
  w,z=0,Image.new('RGB',[z[0],sum(y)])
  for u,v in zip(x,y):
   z.paste(u,[0,w])
   w+=v
  z.save(f.get(),'png')
  y.insert(0,0)
  w*=.4
  for x,z in zip(range(1,len(y)),d[3::4]):
   y[x]*=.4
   w-=y[x-1]+y[x]
   z=open(z.get(),'rb').read().replace(b'\r\n',b'\n').replace(b'\r',b'\n')
   for v in range(128,256):
    z=z.replace(bytes([v]),b'BYTE'+hex(v)[2:].encode())
   z=etree.fromstring(z)
   for v in z.findall('./Room'):
    s.append(etree.tostring(v))
   for v in z.findall('./Properties'):
    for u in v:
     t.append(etree.tostring(u))
   for v in z.findall('.//AbsoluteLocation'):
    u=v.get('value').split()
    v.set('value',f'{u[0]} {float(u[1])+w}')
   for v in z.findall('.//Object'):
    v.set('name',f"{x}x{v.get('name')}")
   for v in z.findall('.//Properties'):
    r=v.findall('.//Property[@name="PathIsGlobal"][@value="1"]')
    for u in v:
     q=u.get('name').strip('0123456789')
     if q in['ConnectedConverter','ConnectedObject',
     'ConnectedSpout','Parent']and u.get('value')!='SWAMPY_SPOUT':
      u.set('value',f"{x}x{u.get('value')}")
     elif r and q=='PathPos':
      q=u.get('value').split()
      u.set('value',f'{q[0]} {float(q[1])+w/.8}')
   u=[]
   for v in z:
    if v.tag=='Object':
     u.append(etree.tostring(v))
   y[x-1]=b''.join(u)
  y.insert(0,b'<Objects>\n  ')
  y[-1]=s[-1]
  y.append(b'  <Properties>\n    ')
  y+=t
  y.append(b'</Properties>\n</Objects>\n')
  x=etree.tostring(etree.fromstring(b''.join(y)),pretty_print=1).split(b'BYTE')
  for z in range(1,len(x)):
   x[z]=bytes([int(x[z][:2],16)])+x[z][2:]
  open(g.get(),'wb').write(b'<?xml version="1.0"?>\n'+b''.join(x))
  e['fg']='green'
  e.delete('1.0','end')
  e.insert('1.0','Success!')
 except BaseException as x:
  e['fg']='red'
  e.delete('1.0','end')
  e.insert('1.0',f'''{x.__class__.__name__}: {x} (Error code: {'8'.join([y.append(w)if w else
[oct(z.tb_lineno)[2:]for z in y]for y in[[x.__traceback__]]for z in y for w in[z.tb_next]][-1])+')'}''')
tk.Button(a,text='Generate',command=generate).pack(anchor='n',side='right',padx=5,pady=5)
tk.Button(a,text='Delete level',command=delete).pack(anchor='n',side='right',pady=5)
tk.Button(a,text='Add level',command=add).pack(anchor='n',side='right',padx=5,pady=5)
add()
add()
a.mainloop()
