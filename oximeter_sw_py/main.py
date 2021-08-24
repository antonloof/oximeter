from machine import Pin, ADC, Timer
from time import sleep

S_TO_BMP = 60

adc = ADC()
adc_c = adc.channel(pin="P18", attn=ADC.ATTN_11DB)

class IIRFilter:
    def __init__(self, a, b, new_sample_caller):
        assert len(a) == len(b), "you goofed up"
        self.a = a
        self.b = b
        self.x = [0] * len(filter_a)
        self.y = [0] * len(filter_a)
        self.i = 0
        self.new_sample_caller = new_sample_caller

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
        self.new_sample_caller(result)

def none_min(a,b):
    if a is None:
        return b
    if b is None:
        return a
    return min(a,b)

def none_max(a,b):
    if a is None:
        return b
    if b is None:
        return a
    return max(a,b)

class PeakCandidate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __gt__(self, other):
        return self.y > other.y

class PeakDetector:
    def __init__(self, callback, prominence):
        self.prominence = prominence
        self.callback = callback
        self.lowest_before_peak_candidate = None
        self.lowest_since_last_peak_candidate = None
        self.peak_candidate = None
        self.last_sample = None
        self.last_x = None
        self.last_diff = None


    def sample(self, sample, x):
        self.lowest_since_last_peak_candidate = none_min(self.lowest_since_last_peak_candidate, sample)
        if self.last_sample is None:
            self.last_sample = sample
            return

        diff = sample - self.last_sample
        if self.last_diff is None:
            self.last_diff = diff
            return

        if diff < 0 and self.last_diff > 0:
            self.peak_candidate = none_max(self.peak_candidate, PeakCandidate(self.last_x, self.last_sample))
            if self.peak_candidate.x == self.last_x:
                self.lowest_before_peak_candidate = none_min(self.lowest_before_peak_candidate, self.lowest_since_last_peak_candidate)
            self.lowest_since_last_peak_candidate = None

        elif self.peak_candidate is not None:
            if self.lowest_before_peak_candidate + self.prominence < self.peak_candidate.y:
                if self.lowest_since_last_peak_candidate + self.prominence < self.peak_candidate.y:
                    self.callback(self.peak_candidate.y, self.peak_candidate.x)
                    self.lowest_before_peak_candidate = None
                    self.peak_candidate = None

        self.last_sample = sample
        self.last_diff = diff
        self.last_x = x


class HeartBeatMeasurement:
    def __init__(self, points_avg, prominence):
        self.timer = Timer.Chrono()
        self.timer.start()

        self.periods_s = [0] * points_avg
        self.periods_i = 0
        self.periods_running_sum = 0
        self.last_peak = None

        self.has_sample = False
        self.new_sample_val = 0

        self.peak_detector = PeakDetector(self.got_peak, prominence=prominence)

    def got_peak(self, value, time_s):
        if self.last_peak is None:
            self.last_peak = time_s
            return

        period = time_s - self.last_peak
        self.periods_running_sum -= self.periods_s[self.periods_i]
        self.periods_running_sum += period
        self.periods_s[self.periods_i] = period
        self.periods_i += 1
        if self.periods_i >= len(self.periods_s):
            self.periods_i = 0

        print("avg:", S_TO_BMP/(self.periods_running_sum / len(self.periods_s)), "bpm. current:", S_TO_BMP/period, "bpm")
        self.last_peak = time_s

    def new_sample(self, val):
        self.new_sample_val = val
        self.has_sample = True

    def update(self):
        if not self.has_sample:
            return
        sample = self.new_sample_val
        self.has_sample = False
        self.peak_detector.sample(sample, self.timer.read())



filter_a = [1, -1.984355370350682, 0.984414127416097]
filter_b = [1, 0, -1]

heart_beater = HeartBeatMeasurement(points_avg=2, prominence=1000)
fil = IIRFilter(filter_a, filter_b, heart_beater.new_sample)
alarm = Timer.Alarm(handler=fil.sample, ms=1, periodic=True)

while 1:
    heart_beater.update()
