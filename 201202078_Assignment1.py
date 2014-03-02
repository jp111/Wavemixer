import wave
import struct
import pyaudio
import os,sys
import tkFileDialog
import signal
from Tkinter import *


class Application:
    chunk=1024
    def __init__(self, master,fl):
	self.plflag=0
	self.psflag=0
	self.pid=0
	#Frame.__init__(self, master)
	
	menubar=Menu(root)
	filemenu=Menu(menubar,tearoff=0)
	filemenu.add_command(label="Open", command=self.file_input)
	filemenu.add_command(label="Play", command=self.pl)
	filemenu.add_command(label="Close", command=root.quit)
	filemenu.add_separator()
	filemenu.add_command(label="Exit", command=root.quit)
	menubar.add_cascade(label="File", menu=filemenu)

	helpmenu=Menu(menubar,tearoff=0)
	helpmenu.add_command(label="Help",command=self.donothing)
	menubar.add_cascade(label="Help",menu=helpmenu)

	root.config(menu=menubar)

	if fl==0:
      		frame=LabelFrame(master,text="Wave1")
      		frame.pack(side=LEFT,fill=None,expand=True)
	elif fl==1:
		frame=LabelFrame(master,text="Wave2")
      		frame.pack(side=LEFT,fill=None,expand=True)
	else:
		frame=LabelFrame(master,text="Wave3")
      		frame.pack(side=LEFT,fill=None,expand=True)
		
	#Quit Button
	self.button = Button(frame, text="Select File", fg="black",command=self.file_input)
	self.button.pack(side=TOP)
	

	self.name=Label(frame,text='',)
        print self.name
	self.name.pack(side=TOP)

	#Amplitude Scale
	self.vara=DoubleVar()
	self.scale1=Scale(frame,label="Amplitude",variable=self.vara,orient=HORIZONTAL,from_=0.0,to=5.0,resolution=0.1)
	self.scale1.pack(side=TOP)
	
	#timeshift Scale
	self.varb=DoubleVar()
	self.scale2=Scale(frame,label="Time Shift",variable=self.varb,orient=HORIZONTAL,from_=-1.0,to=1.0,resolution=0.1)
	self.scale2.pack(side=TOP)

	#timescale Scale
	self.varc=DoubleVar()
	self.scale3=Scale(frame,label="Time Scaling",variable=self.varc,orient=HORIZONTAL,from_=0.0,to=8.0,resolution=0.01)
	self.scale3.pack(side=TOP)
	
	#Time Reversal
	self.checkvar1=IntVar()
	self.c1=Checkbutton(frame,text="Time Reversal",bg="light gray",variable=self.checkvar1,onvalue=1,offvalue=0,height=3,width=20)
	self.c1.pack(side=TOP)
	
	#Modulation
	self.checkvar2=IntVar()
	self.c2=Checkbutton(frame,text="Select for Modulation",bg="light gray",variable=self.checkvar2,onvalue=1,offvalue=0,height=3,width=20)
	self.c2.pack(side=TOP)
	
	#Mixing
	self.checkvar3=IntVar()
	self.c3=Checkbutton(frame,text="Select for Mixing",bg="light gray",variable=self.checkvar3,onvalue=1,offvalue=0,height=3,width=20)
	self.c3.pack(side=TOP)

	#Play Button
	self.play = Button(frame, bg="light gray",text="Play", command=self.fin)
	self.play.pack(side=BOTTOM)

	#Play Button
	self.pause = Button(frame, bg="light gray",text="Pause", command=self.pause)
	self.pause.pack(side=BOTTOM)



    #Functions 
    def donothing(self):
  	return

    def fin(self):
	#self.scaling()
	#print self.checkvar1.get()	
	music_file = wave.open(self.files, 'rb')
	self.type_channel = music_file.getnchannels()
	self.sample_rate = music_file.getframerate()
	self.sample_width = music_file.getsampwidth()
	self.num_frames = music_file.getnframes()
	self.raw_data = music_file.readframes( self.num_frames ) # Returns byte data
	music_file.close()
	## Formating raw_data into Integer data
	self.num_samples = self.num_frames * self.type_channel

	if self.sample_width == 1:
		fmt = "%iB" % self.num_samples # read unsigned chars
    	elif self.sample_width == 2:
        	fmt = "%ih" % self.num_samples # read signed 2 byte shorts
    	else:
       		raise ValueError("Only supports 8 and 16 bit audio formats.")

	self.formated_data = list(struct.unpack(fmt, self.raw_data)) 
	self.scaling()
	self.time_shift()
	self.tscale()
	if self.checkvar1.get()==1:
		self.time_reversal()
	self.pack_file()
	
	self.pl()
    def pl(self):
	if self.psflag==1:
		self.psflag=0
		self.plflag=1
		os.kill(self.pid,signal.SIGCONT)
	else:
		self.pid=os.fork()
		if self.pid==0:
			self.plflag=1
			self.psflag=0

			cur=os.getcwd()
			cur+=str("/output_file.wav")
			self.wf = wave.open(cur, 'rb')
        		self.p = pyaudio.PyAudio()
        		self.stream = self.p.open(
        		format = self.p.get_format_from_width(self.wf.getsampwidth()),
        	    	channels = self.wf.getnchannels(),
        	    	rate = self.wf.getframerate(),
            		output = True
        		)
		        data = self.wf.readframes(self.chunk)
	       	 	while data != '':
	       	     		self.stream.write(data)
	            		data = self.wf.readframes(self.chunk)

        		self.stream.close()
        		self.p.terminate()
			exit(0)
    
    
    def time_reversal(self):
		if self.type_channel == 1:
			self.formated_data.reverse()
		else:
			self.formated_data.reverse()
			for i in xrange(len(self.formated_data) - 1):
				temp = self.formated_data[i]
				self.formated_data[i] = self.formated_data[i+1]
				self.formated_data[i+1] = temp

    
    def file_input(self):
		## Input music file and its attributes
		self.files=tkFileDialog.askopenfilename()			
		self.name['text']=self.files
                music_file = wave.open(self.files, 'rb')

		self.type_channel = music_file.getnchannels()
		self.sample_rate = music_file.getframerate()
		self.sample_width = music_file.getsampwidth()
		self.num_frames = music_file.getnframes()

		self.raw_data = music_file.readframes( self.num_frames ) # Returns byte data
		music_file.close()

		## Formating raw_data into Integer data

		self.num_samples = self.num_frames * self.type_channel
                
                #mono
		if self.sample_width == 1: 
       			fmt = "%iB" % self.num_samples 
                #stereo
    		elif self.sample_width == 2:
        		fmt = "%ih" % self.num_samples 
    		else:
       	 		raise ValueError("Only supports 8 and 16 bit audio formats.")

		self.formated_data = list(struct.unpack(fmt, self.raw_data)) 
    def time_shift(self):
		#print self.sample_rate
		shift_frames=(self.varb.get())*(self.sample_rate)
		shift_frames=int(shift_frames)
		if((self.varb.get()) < 0):
			if(self.type_channel == 1):
				a=[]
				for i in range(0,shift_frames,-1):
					a.append(0)
				self.formated_data = a + self.formated_data
			else:
				a=[]
				for i in range(0,2*shift_frames,-1):
					a.append(0)
				self.formated_data = a + self.formated_data
		else:
			if(self.type_channel == 1):
				self.formated_data=self.formated_data[shift_frames::1]
			else:
				self.formated_data=self.formated_data[2*shift_frames::1]

		self.num_frames = len(self.formated_data)/self.type_channel

    def tscale(self):
                    a=[]
       		    sfactor=self.varc.get()
                    if(sfactor == 0):
                            sfactor=1
       
                    if self.type_channel == 1:  
                            k=int(len(self.formated_data)/sfactor)
                            for i in range(k):
                                    a.append(self.formated_data[int(sfactor*i) ])
                    else:
                            e_li=[]
                            o_li=[]
                            for i in range( len(self.formated_data) ):
                                    if(i%2 == 0):
                                            e_li.append(self.formated_data[i])
                                    else:
                                            o_li.append(self.formated_data[i])
                            k=int(len(e_li)/sfactor)
                            for i in range(k):
                                    a.append(e_li[ int(sfactor*i) ])
                                    a.append(o_li[ int(sfactor*i) ])
       
                    self.formated_data = a    
                    self.num_frames = len(self.formated_data)/self.type_channel
		
    def scaling(self):	
		max_amplification = 32767
		min_amplification = -32768

		for i in xrange(len(self.formated_data)):
			if self.formated_data[i] * (self.vara.get()) > max_amplification:
				self.formated_data[i] = max_amplification
			elif self.formated_data[i] * (self.vara.get()) < min_amplification:
				self.formated_data[i] = min_amplification
			else:
				self.formated_data[i] = self.formated_data[i] * (self.vara.get())
	
    def pack_file(self):
		if self.sample_width==1: 
			fmt="%iB" % self.num_frames*self.type_channel 
		else: 
			fmt="%ih" % self.num_frames*self.type_channel

		out_data=struct.pack(fmt,*(self.formated_data))

		out_music_file=wave.open("output_file.wav",'w')

		out_music_file.setframerate(self.sample_rate) 
		out_music_file.setnframes(self.num_frames) 
		out_music_file.setsampwidth(self.sample_width) 
		out_music_file.setnchannels(self.type_channel) 
		out_music_file.writeframes(out_data) 

		out_music_file.close()

   

    def pause(self):	
		self.plflag=0
		self.psflag=1
		os.kill(self.pid,signal.SIGSTOP)

    def close(self):
        self.stream.close()
        self.p.terminate()
    def onread(self):
		music_file = wave.open(self.files, 'rb')
		self.type_channel = music_file.getnchannels()
		self.sample_rate = music_file.getframerate()
		self.sample_width = music_file.getsampwidth()
		self.num_frames = music_file.getnframes()

		self.raw_data = music_file.readframes( self.num_frames ) # Returns byte data
		music_file.close()

		## Formating raw_data into Integer data

		self.num_samples = self.num_frames * self.type_channel

		if self.sample_width == 1: 
       			fmt = "%iB" % self.num_samples # read unsigned chars
    		elif self.sample_width == 2:
        		fmt = "%ih" % self.num_samples # read signed 2 byte shorts
    		else:
       	 		raise ValueError("Only supports 8 and 16 bit audio formats.")

		self.formated_data = list(struct.unpack(fmt, self.raw_data)) 
		self.scaling()
		self.time_shift()
		self.tscale()
		if self.checkvar1.get()==1:
			self.time_reversal()
		self.pack_file()
    def read(self):
	    	self.onread()
	    	music_file = wave.open(self.onread(), 'rb')
		type_channel = music_file.getnchannels()
		sample_rate = music_file.getframerate()
		sample_width = music_file.getsampwidth()
		num_frames = music_file.getnframes()

		raw_data = music_file.readframes(num_frames ) # Returns byte data
		music_file.close()

		## Formating raw_data into Integer data

		num_samples = num_frames * type_channel

		if sample_width == 1: 
       			fmt = "%iB" % num_samples # read unsigned chars
    		elif sample_width == 2:
        		fmt = "%ih" % num_samples # read signed 2 byte shorts
    		else:
       	 		raise ValueError("Only supports 8 and 16 bit audio formats.")

		formated_data = list(struct.unpack(fmt, raw_data)) 	
		return formated_data


root=Tk()

w = root.winfo_screenwidth()
h = root.winfo_screenheight()

x = 270
y = 60

root.geometry("%dx%d+%d+%d" % (w*2/3,h*4/5,x,y))
root.title("WaveMixer")

w=Label(root,text="Wave Mixer",width=10,height=2,font=30)
w.pack()
var=StringVar()

var.set('Please Select a file')

wave1=Application(root,0)
wave2=Application(root,1)
wave3=Application(root,2)

def readfile(file_name):
		music_file = wave.open(file_name, 'rb')
		type_channel = music_file.getnchannels()
		sample_rate = music_file.getframerate()
		sample_width = music_file.getsampwidth()
		num_frames = music_file.getnframes()

		raw_data = music_file.readframes(num_frames ) # Returns byte data
		music_file.close()

		## Formating raw_data into Integer data

		num_samples = num_frames * type_channel

		if sample_width == 1: 
       			fmt = "%iB" % num_samples # read unsigned chars
    		elif sample_width == 2:
        		fmt = "%ih" % num_samples # read signed 2 byte shorts
    		else:
       	 		raise ValueError("Only supports 8 and 16 bit audio formats.")

		formated_data = list(struct.unpack(fmt,raw_data))
		return formated_data


def record(): 
		 array=[]
                 chunk = 1024 
                 FORMAT = pyaudio.paInt16 
                 CHANNELS = 1 
                 RATE = 44100 
                 RECORD_SECONDS = 5 
                 p = pyaudio.PyAudio() 
                 stream = p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,output=True,frames_per_buffer=chunk) 
                 for i in range(0, 44100 / chunk * RECORD_SECONDS): 
                         data = stream.read(chunk) 
                         array.append(data) 
                 wf = wave.open("rec.wav", 'wb') 
                 wf.setnchannels(CHANNELS) 
                 wf.setsampwidth(p.get_sample_size(FORMAT)) 
                 wf.setframerate(RATE) 
                 wf.writeframes(b''.join(array)) 
                 wf.close() 
                 stream.stop_stream() 
                 stream.close() 
                 p.terminate() 	
def pl():
	chunk=1024
	#print "here"
	cur=os.getcwd()
	cur+=str("/output.wav")
	wf = wave.open(cur, 'rb')
        p = pyaudio.PyAudio()
        stream = p.open(
            format = p.get_format_from_width(wf.getsampwidth()),
            channels = wf.getnchannels(),
            rate = wf.getframerate(),
            output = True
        )
        data =wf.readframes(chunk)	
        while data != '':
            stream.write(data)
            data = wf.readframes(chunk)
	stream.close()
        p.terminate()

def rpl():
	chunk=1024
	cur=os.getcwd()
	cur+=str("/rec.wav")
	wf = wave.open(cur, 'rb')
        p = pyaudio.PyAudio()
        stream = p.open(
            format = p.get_format_from_width(wf.getsampwidth()),
            channels = wf.getnchannels(),
            rate = wf.getframerate(),
            output = True
        )
        data =wf.readframes(chunk)	
        while data != '':
            stream.write(data)
            data = wf.readframes(chunk)
	stream.close()
        p.terminate()
def modulate():
	SHRT_MIN=-32767 - 1
	SHRT_MAX=32767
	fl1=0
	fl2=0
	fl3=0
	if wave1.checkvar2.get()==1:		
		fl1=1
	if wave2.checkvar2.get()==1:
		fl2=1
	if wave3.checkvar2.get()==1:
		fl3=1
	if (fl1==1 & fl2==1) or (fl2==1 & fl3==1) or (fl1==1 & fl3==1):	
		if (fl1==1 & fl2==1):
			wave1.onread()
			cur=os.getcwd()
			cur+=str("/output_file.wav")
			data=readfile(cur)
			fi = wave.open(cur,"rb")
			wave2.onread()
			cur=os.getcwd()
			cur+=str("/output_file.wav")
			data2=readfile(cur)
			fi2 = wave.open(cur,"rb")
			#print "hi"
		elif (fl1==1 & fl3==1):
			wave1.onread()
			cur=os.getcwd()
			cur+=str("/output_file.wav")
			data=readfile(cur)
			fi = wave.open(cur,"rb")
			wave3.onread()
			cur=os.getcwd()
			cur+=str("/output_file.wav")
			data2=readfile(cur)
			fi2 = wave.open(cur,"rb")
		elif (fl2==1 & fl3==1):
			wave2.onread()
			cur=os.getcwd()
			cur+=str("/output_file.wav")
			data=readfile(cur)
			fi = wave.open(cur,"rb")
			wave3.onread()
			cur=os.getcwd()
			cur+=str("/output_file.wav")
			data2=readfile(cur)
			fi2 = wave.open(cur,"rb")
		fo=wave.open("output.wav","w")
		fo.setparams(fi.getparams())
		width=fi.getsampwidth()
		width2=fi2.getsampwidth()	
		if width>width2:
			width=width2
		fmts=(None, "=B", "=h", None, "=l")
		fmt=fmts[width]
		dcs=(None, 128, 0, None, 0)
		dc=dcs[width]
		if fi.getnframes()<fi2.getnframes():
			maxi=fi.getnframes()
			flag=1		
		else:
			maxi=fi2.getnframes()
			flag=2
		amp=[]
		
                #print flag
		for i in range(maxi):
			if flag==1 and i>=fi2.getnframes():
				if data[i]<SHRT_MIN: 
					iframe=SHRT_MIN
				elif data[i]>SHRT_MAX:
					iframe=SHRT_MAX
				else:
					iframe=data[i]
			elif flag==2 and i>=fi.getnframes():
				if data2[i]<SHRT_MIN:
					iframe=SHRT_MIN
				elif data2[i]>SHRT_MAX:
					iframe=SHRT_MAX
				else:
					iframe=data2[i]
			else:
				if data2[i]*data[i]<SHRT_MIN:
					iframe=SHRT_MIN
				elif data2[i]*data[i]>SHRT_MAX:
					iframe=SHRT_MAX
				else:
					iframe=data2[i]*data[i]
			iframe-=dc
			oframe=iframe/2;
			oframe+=dc
			oframe=struct.pack(fmt, oframe)
			fo.writeframes(oframe)
		fi.close()
		fo.close()
		pl()
	elif (fl1==1 & fl2==1 & fl3==1):
		wave1.onread()
		cur=os.getcwd()
		cur+="output_file.wav"
		data=readfile(cur)
		fi = wave.open(cur,"rb")
		
		wave2.onread()
		cur=os.getcwd()
		cur+="output_file.wav"
		data2=readfile(cur)
		fi2 = wave.open(cur,"rb")
		
		wave3.onread()
		cur=os.getcwd()
		cur+="output_file.wav"
		data3=readfile(cur)	
		fi3 = wave.open(cur,"rb")
		fo = wave.open("output.wav","w")
		fo.setparams(fi.getparams())
		width=fi.getsampwidth()
		width2=fi2.getsampwidth()
		width3=fi3.getsampwidth()	
		if width>width2:
			width=width2
		if width>width3:
			width=width3
		fmts=(None, "=B", "=h", None, "=l")
		fmt=fmts[width]
		dcs=(None, 128, 0, None, 0)
		dc=dcs[width]
		if fi.getnframes()<fi2.getnframes():
			maxi=fi.getnframes()
			flag=1		
		else:
			maxi=fi2.getnframes()
			flag=2
		if fi3.getnframes()<maxi:
			maxi=fi3.getnframes()
			flag=3
		amp=[]
		for i in range(maxi):
			if flag==1 and i>=fi2.getnframes():
				if data[i]<SHRT_MIN: 
					iframe=SHRT_MIN
				elif data[i]>SHRT_MAX:
					iframe=SHRT_MAX
				else:
					iframe=data[i]
			elif flag==2 and i>=fi.getnframes():
				if data2[i]<SHRT_MIN:
					iframe=SHRT_MIN
				elif data2[i]>SHRT_MAX:
					iframe=SHRT_MAX
				else:
					iframe=data2[i]
			elif flag==3 and i>=fi3.getnframes():
				if data3[i]<SHRT_MIN:
					iframe=SHRT_MIN
				elif data3[i]>SHRT_MAX:
					iframe=SHRT_MAX
				else:
					iframe=data3[i]
			else:
				if data2[i]*data[i]*data3[i]<SHRT_MIN:
					iframe=SHRT_MIN
				elif data2[i]*data[i]*data3[i]>SHRT_MAX:
					iframe=SHRT_MAX
				else:
					iframe=data2[i]*data[i]*data3[i]
			#	print int(iframe)
			iframe-=dc
			oframe=iframe/2;
			oframe+=dc
			oframe=struct.pack(fmt, oframe)
			fo.writeframes(oframe)
		fi.close()
		fo.close()
		pl()
		

def mixing():
	SHRT_MIN=-32767 - 1
	SHRT_MAX=32767
	fl1=0
	fl2=0
	fl3=0
	
	if wave1.checkvar3.get()==1:		
		fl1=1
	if wave2.checkvar3.get()==1:
		fl2=1
	if wave3.checkvar3.get()==1:
		fl3=1
	if (fl1==1 & fl2==1) or (fl2==1 & fl3==1) or (fl1==1 & fl3==1):	
		if (fl1==1 & fl2==1):
			wave1.onread()
			cur=os.getcwd()
			cur+=str("/output_file.wav")
			data=readfile(cur)
			fi = wave.open(cur,"rb")
			wave2.onread()
			cur=os.getcwd()
			cur+=str("/output_file.wav")
			data2=readfile(cur)
			fi2 = wave.open(cur,"rb")
		elif (fl1==1 & fl3==1):
			wave1.onread()
			cur=os.getcwd()
			cur+=str("/output_file.wav")
			data=readfile(cur)
			fi = wave.open(cur,"rb")
			wave3.onread()
			cur=os.getcwd()
			cur+=str("/output_file.wav")
			data2=readfile(cur)
			fi2 = wave.open(cur,"rb")
		elif (fl2==1 & fl3==1):
			wave2.onread()
			cur=os.getcwd()
			cur+=str("/output_file.wav")
			data=readfile(cur)
			fi = wave.open(cur,"rb")
			wave3.onread()
			cur=os.getcwd()
			cur+=str("/output_file.wav")
			data2=readfile(cur)
			fi2 = wave.open(cur,"rb")
		fo = wave.open("output.wav","w")
		fo.setparams(fi.getparams())
		width=fi.getsampwidth()
		width2=fi2.getsampwidth()	
		if width<width2:
			width=width2
		fmts=(None, "=B", "=h", None, "=l")
		fmt=fmts[width]
		dcs=(None, 128, 0, None, 0)
		dc=dcs[width]
		if fi.getnframes()>fi2.getnframes():
			maxi=fi.getnframes()
			flag=1		
		else:
			maxi=fi2.getnframes()
			flag=2
		amp=[]
		#print flag
		for i in range(maxi):
			if flag==1 and i>=fi2.getnframes():
				if data[i]<SHRT_MIN: 
					iframe=SHRT_MIN
				elif data[i]>SHRT_MAX:
					iframe=SHRT_MAX
				else:
					iframe=data[i]
			elif flag==2 and i>=fi.getnframes():
				if data2[i]<SHRT_MIN:
					iframe=SHRT_MIN
				elif data2[i]>SHRT_MAX:
					iframe=SHRT_MAX
				else:
					iframe=data2[i]
			else:
				if data2[i]+data[i]<SHRT_MIN:
					iframe=SHRT_MIN
				elif data2[i]+data[i]>SHRT_MAX:
					iframe=SHRT_MAX
				else:
					iframe=data2[i]+data[i]
			iframe-=dc
			oframe=iframe/2;
			oframe+=dc
			oframe=struct.pack(fmt, oframe)
			fo.writeframes(oframe)
		fi.close()
		fo.close()
		pl()
	elif (fl1==1 & fl2==1 & fl3==1):
		wave1.onread()
		cur=os.getcwd()
		cur+="output_file.wav"
		data=readfile(cur)
		fi = wave.open(cur,"rb")
		
		wave2.onread()
		cur=os.getcwd()
		cur+="output_file.wav"
		data2=readfile(cur)
		fi2 = wave.open(cur,"rb")
		
		wave3.onread()
		cur=os.getcwd()
		cur+="output_file.wav"
		data3=readfile(cur)	
		fi3 = wave.open(cur,"rb")
		fo = wave.open("output.wav","w")
		fo.setparams(fi.getparams())
		width=fi.getsampwidth()
		width2=fi2.getsampwidth()
		width3=fi3.getsampwidth()	
		if width<width2:
			width=width2
		if width<width3:
			width=width3
		fmts=(None, "=B", "=h", None, "=l")
		fmt=fmts[width]
		dcs=(None, 128, 0, None, 0)
		dc=dcs[width]
		if fi.getnframes()>fi2.getnframes():
			maxi=fi.getnframes()
			flag=1		
		else:
			maxi=fi2.getnframes()
			flag=2
		if fi3.getnframes()>maxi:
			maxi=fi3.getnframes()
			flag=3
		amp=[]
		for i in range(maxi):
			if flag==1 and i>=fi2.getnframes():
				if data[i]<SHRT_MIN: 
					iframe=SHRT_MIN
				elif data[i]>SHRT_MAX:
					iframe=SHRT_MAX
				else:
					iframe=data[i]
			elif flag==2 and i>=fi.getnframes():
				if data2[i]<SHRT_MIN:
					iframe=SHRT_MIN
				elif data2[i]>SHRT_MAX:
					iframe=SHRT_MAX
				else:
					iframe=data2[i]
			elif flag==3 and i>=fi3.getnframes():
				if data3[i]<SHRT_MIN:
					iframe=SHRT_MIN
				elif data3[i]>SHRT_MAX:
					iframe=SHRT_MAX
				else:
					iframe=data3[i]
			else:
				if data2[i]+data[i]+data3[i]<SHRT_MIN:
					iframe=SHRT_MIN
				elif data2[i]+data[i]+data3[i]>SHRT_MAX:
					iframe=SHRT_MAX
				else:
					iframe=data2[i]+data[i]+data3[i]
			#	print int(iframe)
			iframe-=dc
			oframe=iframe/2;
			oframe+=dc
			oframe=struct.pack(fmt, oframe)
			fo.writeframes(oframe)
		fi.close()
		fo.close()
		pl()



		
#MOdulate AND Play Button
mod=Button(root, text="Modulate And Play",fg="black", command=modulate,bg="Slategray")
mod.place(x=150,y=580,anchor=CENTER)

#Mix AND Play Button
mix=Button(root,text="Mix And Play",fg="black", command=mixing,bg="Slategray")
mix.place(x=760,y=580,anchor=CENTER)

#Record
rec=Button(root,text="Start Recording",fg="black",command=record,bg="Slategray")
rec.place(x=460,y=565,anchor=CENTER)

#Recording play
rec=Button(root,text="Play Recording",fg="black",command=rpl,bg="Slategray")
rec.place(x=460,y=595,anchor=CENTER)


root.mainloop()
root.destroy()

