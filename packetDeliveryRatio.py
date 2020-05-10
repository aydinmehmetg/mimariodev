#Paket Teslim Oranı
import traceanalyzer as tr
#Dosya okutma
pdr1=tr.Pdr('iz.tr','33')
pdr1.sample()
pdr1.plot('sr-') ,

time=pdr1.time_sample
pdr=pdr1.pdr_sample
idx=0
for instant in time:
    print(instant,' ',pdr[idx]) 
    idx+=1