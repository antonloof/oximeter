from machine import Pin, ADC
from time import sleep

adc = ADC()
adc_c = adc.channel(pin="P20", attn=ADC.ATTN_11DB)

while 1:
    print(adc_c.value())
