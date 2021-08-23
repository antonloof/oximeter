data = []

with open("putty_filtered.txt") as f:
    for d in f.readlines():
        data.append(float(d))


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
        
    def __repr__(self):
        return f"x: {self.x} y: {self.y}"
        
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
        
        
    def sample(self, sample, i):
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
        self.last_x = i

def x(*args):
    print(*args)

pd = PeakDetector(x, 1000)
for i, d in enumerate(data):
    pd.sample(d, i)