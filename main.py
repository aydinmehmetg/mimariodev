import matplotlib.pyplot as plt
import os
import awk
#get directory
directory=os.getcwd()

#idx as index
#event:-->+:enque|-:deque|r:reception[d:drop|c:collision
event_idx='$1'
#time
time_idx='$2'
#Sending Node
sn_idx='$3'
#Receiving Node
rc_idx='$4'
#packet type :--> cbr|tcp|ack|rtProto|...
ptype_idx='$5'
#packet size
psize_idx='$6'

#source addresse and port:--> Format:a.b (a:addresse and b: port)
sadd_idx='$10'
#destination addresse and port
dadd_idx='$11'

class Eedelay(object):
       
    
    #initialization
    def __init__(self,filename,receiver_node):
        """Initialises a Eedelay

        Arguments:
        filename -- the name of the trace file ex:out.tr
        receiver_node --the name of receiver node to compute EEdelay

        """

        if (filename[0]=='/'):
             self.filename=filename
             self.legend=filename+'--EEdelay'
        else:
            directory=os.getcwd()
            #filename with directory
            self.legend=filename+'--EEdelay'
            self.filename=directory+'/'+filename
        self.receiver_node=receiver_node
        
        #network parameters
        self.ptype1='tcp' #for tcp packet
        self.ptype2='cbr' #for cbr packet
        self.event='r'

        #data array
        self.eedelay_array=[0]
        self.time_array=[0]
        #sample
        self.eedelay_sample=[0]
        self.time_sample=[0]
        #global value
        self.value=0
        self._compute_eedelay()
        self._step=0
    
    def _compute_eedelay(self):
        """Compute the average of end to end delay in each simulation step and put it in EEdelay array
            end to end delay=Time/No.Sample
        """

        with awk.Reader(self.filename) as reader:
            oldtime=0.0
            time=0.0
            interval=0.0
            cum_interval=0.0
            samp=0
            #network parameter    
            for record in reader:
                #for receiver node
                if((record[event_idx]==self.event) and ((record[ptype_idx]==self.ptype1)or (record[ptype_idx]==self.ptype2)) and ((record[rc_idx]==self.receiver_node)) ):
                    time=float(record[time_idx])
                    interval=time-oldtime
                    cum_interval+=interval
                    oldtime=time
                    samp+=1
                    self.time_array.append(cum_interval)
                    self.eedelay_array.append(cum_interval/samp)
                    #setting value
                    self._value=(cum_interval/samp)
                    self.value=self._value
        
    #sampling fonction
    def sample(self,*step):
        """Sampling data, by default sampling step is 1 sec
        """
        try:
            stp=float(step[0])
        except:
            stp=0.0

        if stp==0.0:
            stp=1
        else:
            stp=stp
        self._step=stp
        oldtime=0
        self.time_sample=[0]
        self.eedelay_sample=[0]
        #index of sample
        idx=0
        for timesample in self.time_array:
            interval=timesample-oldtime
            idx+=1
            if interval>=self._step:
                oldtime=timesample
                self.time_sample.append(self.time_array[idx])
                self.eedelay_sample.append(self.eedelay_array[idx])
                
        #plot fonction
    def plot(self,*argv):
        """plot data

        Arguments:
        as matplotlib
        """
        #test sampling
        try:
            var=float(self.time_sample[3])
        except:
            var=-1
        if (var!=-1):
            #plot sample
            try:
                _arg=list(argv)
                args=_arg[0]
            except:
                args='s-'
            plt.plot(self.time_sample,self.eedelay_sample,args,label=self.legend)
        else:
            #plot array
            try:
                _arg=list(argv)
                args=_arg[0]
                plt.plot(self.time_array,self.eedelay_array,args,label=self.legend)
            except :
                plt.plot(self.time_array,self.eedelay_array,label=self.legend)
        plt.title('End-to-End delay')
        plt.xlabel('Time [s]')
        plt.ylabel('Average EEdelay [s]')
        plt.grid(True)
        plt.legend()
        plt.draw()
        plt.pause(1)
        #plt.close()
        
class Pdr(object):
    
    #initialization
    def __init__(self,filename,receiver_node):
        """Initialises a Pdr
        :Packet delivery ratio
        
        Arguments:
        filename -- the name of the trace file ex:out.tr
        receiver_node --the name of receiver node to compute a PDR

        """
        
        if (filename[0]=='/'):
             self.filename=filename
             self.legend=filename+'--PDR'
        else:
            directory=os.getcwd()
            #filename with directory
            self.legend=filename+'--PDR'
            self.filename=directory+'/'+filename

        self.receiver_node=receiver_node
        
        #network parameters
        self.ptype1='tcp' #for tcp packet
        self.ptype2='cbr' #for cbr packet
        
        #event
        self.received='r' #recevied event
        self.sent='+'     #sent event
    
        #data array
        self.pdr_array=[0]
        self.time_array=[0]

        self.sent_counter_array=[]
        self.delivery_counter_array=[]
        #sample
        self.pdr_sample=[0]
        self.time_sample=[0]
        #pdr value
        self.value=0
        self._step=0
        self._compute_pdr()
        
    #compute pdr
    def _compute_pdr(self):
        """Compute the packet delivery ratio in each simulation step and put it in EEdelay array
            PDR=No delivered Packet/No Sent Packet
        """
        with awk.Reader(self.filename) as reader:
            #old_time, time, interval and cum_interval initialization
            oldtime=0.0
            time=0.0
            interval=0.0        
            cum_interval=0.0

            #packet counter
            sent_counter=0
            delivery_counter=0
            
            #redefine pdr_array
            self.pdr_array=[]
            #redefine time_array
            self.time_array=[]

            for record in reader:
                #getting time
                time=float(record[time_idx])
                #interval computation
                interval=time-oldtime
                cum_interval+=interval
                oldtime=time

                self.time_array.append(cum_interval)
                #pdr computing
                if((record[event_idx]==self.received) and (record[ptype_idx]==self.ptype1 or record[ptype_idx]==self.ptype2)):
                    delivery_counter+=1
                    self.delivery_counter_array.append(delivery_counter)
                else:
                    self.delivery_counter_array.append(delivery_counter)

                if((record[event_idx]==self.sent) and (record[ptype_idx]==self.ptype1 or record[ptype_idx]==self.ptype2)):
                     sent_counter+=1
                     self.sent_counter_array.append(sent_counter)
                else:
                    self.sent_counter_array.append(sent_counter)
                if (delivery_counter==0):
                    self.pdr_array.append(0)
                else:
                    self.pdr_array.append(delivery_counter/sent_counter)
                    #compute pdr value
                    self.value=delivery_counter/sent_counter

    #sampling fonction
    def sample(self,*step):
        """Sampling data, by default sampling step is 1 sec
        """
        try:
            stp=float(step[0])
        except:
            stp=0.0

        if stp==0.0:
            stp=1
        else:
            stp=stp
        
        self._step=stp   
    
        #sampling value initialization
        self.pdr_sample=[0]
        self.time_sample=[0]

        oldtime=0
        idx=0
        for timesample in self.time_array:
            interval=timesample-oldtime
            idx+=1
            if interval>=self._step:
                oldtime=timesample
                
                self.time_sample.append(timesample)
                self.pdr_sample.append(self.pdr_array[idx])
                
    #plot fonction
    def plot(self,*argv):
        """plot data
        Arguments:
        as matplotlib
        """
        #test sampling
        try:
            var=float(self.time_sample[3])
        except:
            var=-1
        if (var!=-1):
            #plot sample
            try:
                _arg=list(argv)
                args=_arg[0]
            except:
                args='s-'
            plt.plot(self.time_sample,self.pdr_sample,args,label=self.legend)
        else:
            #plot array
            try:
                _arg=list(argv)
                args=_arg[0]
                plt.plot(self.time_array,self.pdr_array,args,label=self.legend)
            except :
                plt.plot(self.time_array,self.pdr_array,label=self.legend)
        plt.title('Packet Delivery Ratio [PDR]')
        plt.xlabel('Time [s]')
        plt.ylabel('PDR')
        plt.grid(True)
        plt.legend()
        plt.draw()
        plt.pause(1)
        #plt.close()
        
