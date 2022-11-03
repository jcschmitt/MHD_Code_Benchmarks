coilset = 'coilset_ellipse_v0';
coil_current_array = [ 1 1 1 1 1 1 1 1 1 1];

rGuess = 10.0

 [rAxis, current_2p5_tesla] = find_magnetic_axis(coilset, coil_current_array, rGuess)

% <----Finished axis search
% <----Axis location: r = 9.997
% <----Coil current array for 2.5 T on-axis at phi=0 (Amps): 2504844.9646      2504844.9646      2504844.9646      2504844.9646      2504844.9646      2504844.9646      2504844.9646      2504844.9646      2504844.9646      2504844.9646
% rAxis =
%      9.997009667760162e+00
% current_2p5_tesla =
%   Columns 1 through 3
%      2.504844964565333e+06     2.504844964565333e+06     2.504844964565333e+06
%   Columns 4 through 6
%      2.504844964565333e+06     2.504844964565333e+06     2.504844964565333e+06
%   Columns 7 through 9
%      2.504844964565333e+06     2.504844964565333e+06     2.504844964565333e+06
%   Column 10
%      2.504844964565333e+06
