%% Parameter space generator 
% 6/25/2019
% Yenchia Feng

% parameter ranges 
p1 = 0.3:0.01:0.4;
p2 = 2.5:0.01:2.6;
p3 = 1.4:0.02:1.6;
p4 = 0.9:0.03:1.2;

[P1,P2,P3,P4] = ndgrid(p1,p2,p3,p4);

N = length(p1)*length(p2)*length(p3)*length(p4);
Pcombo = zeros(4,N);

for i=1:N
    
    Pcombo(:,i) = [P1(i) P2(i) P3(i) P4(i)];
    
end
