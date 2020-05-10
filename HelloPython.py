import  traceanalyzer as tr

eedelay2=tr.Eedelay('iz.tr','33')
eedelay2.sample()#eedelay2.sample(1.5) for sampling with step=1.5
eedelay2.plot()
time=eedelay2.time_sample
eedelay=eedelay2.eedelay_sample
for instant in time:
    print(instant,' ',eedelay2)