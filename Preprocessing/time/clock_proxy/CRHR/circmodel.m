function z = circmodel(t, X)

%alp = 0.05*calstps(t*60*60 - tim)*5;%note this has been shut off
stepfac = 0.0001; % Originally stepfac = 0.0001
alp = stepfac*calstpsa(t*60*60);
intper = 24.0;
pa = 0.2618;
c = 33.75;
mu = 0.23;
k = 0.55;
cm = 0.4;
bet = 0.0075;
a = (intper/(0.99669*24.2))^2;
B = c*alp*(1-X(1))*(1-cm*X(2))*(1-cm*X(3));


y(1) = 60*(alp*(1-X(1)) - bet*X(1));
y(2) = pa*(X(3) + B);
y(3) = pa*(mu*(X(3) - (4/3)*X(3)^3) - X(2)*(a+k*B));

z = y';

end

