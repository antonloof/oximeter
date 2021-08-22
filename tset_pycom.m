clc, close all, clear all

d = importdata("putty_log.txt");
system("python test_filter.py > outfrompy.txt")
d_from_py = importdata("outfrompy.txt");

good_samples_start = 90000;
good_samples_stop = 110000;
data = d(good_samples_start:good_samples_stop);

fs = 1000;

[z,p,k] = butter(1, [0.5, 3] / (fs / 2));
[sos, g] = zp2sos(z,p,k);
filtered_data = sosfilt(sos, data);

plot(filtered_data)
figure
plot(d_from_py)
