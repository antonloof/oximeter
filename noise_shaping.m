clc, close all, clear all

fs = 1000;
d = importdata("raw_data.txt");
%d = d(50000:75000);
t = (0:(length(d)-1))/fs;

[b1,a1] = butter(2, [0.1, 10]/(fs/2));
%filtered = bandpass(d, [0.25,25], fs);
filtered = filter(b1, a1, d);


hold on
plot(t, d)
plot(t, filtered)
legend(["original", "filtered"])
[ignore, times] = findpeaks(filtered, t, "MinPeakProminence", 30);
figure
findpeaks(filtered, t, "MinPeakProminence", 30);
figure
hold on
plot(times(1:end-1), movmean(60./diff(times), 2))
plot(times(1:end-1), movmean(60./diff(times), 3))
plot(times(1:end-1), movmean(60./diff(times), 4))
plot(times(1:end-1), movmean(60./diff(times), 5))
format long


