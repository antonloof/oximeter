from machine import Pin, ADC, Timer
from time import sleep


adc = ADC()
adc_c = adc.channel(pin="P18", attn=ADC.ATTN_11DB)
class IIRFilter:
    def __init__(self, a, b):
        assert len(a) == len(b), "you goofed up"
        self.a = a
        self.b = b
        self.x = [0] * len(filter_a)
        self.y = [0] * len(filter_a)
        self.i = 0

    def sample(self, *args):
        self.x[self.i] = adc_c.value()
        # lets gooo MAC it up
        result = 0
        for j in range(len(self.a)):
            result += self.x[self.i - j] * self.b[j]

        for j in range(1, len(self.a)):
            result -= self.y[self.i - j] * self.a[j]

        self.y[self.i] = result
        self.i += 1
        if self.i >= len(self.a):
            self.i = 0
        print(self.y[self.i])


filter_a = [1, -1.984355370350682, 0.984414127416097]
filter_b = [1, 0, -1]

filter = IIRFilter(filter_a, filter_b)
alarm = Timer.Alarm(handler=filter.sample, ms=1, periodic=True)

while 1:
    pass
