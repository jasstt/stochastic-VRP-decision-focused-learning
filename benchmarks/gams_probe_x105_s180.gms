Set i / i1*i105 /;
Set s / s1*s180 /;

Scalar routeCapacity / 600 /;
Scalar riskWeight / 0.15 /;
Scalar cvarAlpha / 0.9 /;

Parameter demand(s,i);
demand(s,i) = 50 + mod(ord(i) + ord(s), 30);

Positive Variable load(i), short(i,s), surplus(i,s), eta, excess(s);
Variable scenarioLoss(s), z;

Equation objective, shortDef(i,s), surplusDef(i,s), capacityDef, lossDef(s), cvarDef(s);

shortDef(i,s).. short(i,s) =g= demand(s,i) - load(i);
surplusDef(i,s).. surplus(i,s) =g= load(i) - demand(s,i);
capacityDef.. sum(i, load(i)) =l= 14 * routeCapacity;
lossDef(s).. scenarioLoss(s) =e= sum(i, 3.0 * short(i,s) + 0.15 * surplus(i,s));
cvarDef(s).. excess(s) =g= scenarioLoss(s) - eta;
objective.. z =e= sum(s, scenarioLoss(s)) / card(s)
    + riskWeight * (eta + (1 / ((1 - cvarAlpha) * card(s))) * sum(s, excess(s)));

Model probe / all /;
Solve probe using LP minimizing z;

File out / gams_probe_x105_s180_result.csv /;
put out;
put "modelstat,solvestat,objective" /;
put probe.modelstat:0:0, ",", probe.solvestat:0:0, ",", z.l:0:8 /;
