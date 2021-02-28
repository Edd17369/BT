clear all
clc
v=50
N=1
M=3
M2=M+0.00001  

syms r t
%w2=eval(int((r^2)*((v-r)^2),r,0,v))
%vpa(eval(-inv(int(expm(-M*r)*(-1/w2)*(r^2)*(v-r)^2,r,0,v))),100)
%K=-eval(inv(int(expm(-M*r)*(-1/w2)*(r^2)*(v-r)^2,r,0,v)))

%%
f=((1+(N/M))*exp(M*t)-(N/M))
x=0:0.001:49.99;
y=subs(f,t,x);

figure(1)
plot(x,y)
hold on 
plot(out.simout)
legend('sol. real','sol. de simulation')
hold off
grid on