%% Solver stagnant
clc; clear;

jewels = [1, 2, 3, 4, 4];

% solver stag
times1 = [ 0.490739107132, 94.6651880741, 900.34301281, 900.499109983, 900.450819016 ];
memory1 = [29.282304, 104.820736, 327.049216, 479.531008, 496.238592];

% Solver str
times2 = [0.010106086731, 0.342633962631, 4.6995370388, 42.8076069355, 18.7808990479];
memory2 = [11.788288, 14.852096, 28.483584, 110.637056, 99.5328];

% time
figure('Name', 'Time as a function of jewels')
plot(jewels, times1)
hold on
plot(jewels, times2)
legend('Solver 1', 'Solver 2')
xlabel('Jewels')
ylabel('Time [s]')
hold off

% memory usage