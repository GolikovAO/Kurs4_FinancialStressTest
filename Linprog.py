from scipy.optimize import linprog
import pulp
import Organization
import TestWithoutForm

org = Organization.Organization('2310031475')
c = TestWithoutForm.ReworkList(org.Get2019DataFromExcel())
x = [0.05, 0.1, 0, 0.76, 0.4, 0.01, 0.02]
part = TestWithoutForm.CalcPart(c)

def linProg(c):
    x = []
    for i in range(0, 8):
        if (i==6):
            x.append(pulp.LpVariable('x' + str(i), lowBound=1, upBound=1))
        else:
            x.append(pulp.LpVariable('x' + str(i), lowBound=0.00, upBound=2.00))
    problem = pulp.LpProblem('0', pulp.LpMinimize)
    b = c[7] * (c[7] - c[6]) / (c[1] + c[0])
    print(b)
    problem += c[0]*x[0] + c[1]*x[1] + c[2]*x[2] + c[3]*x[3] + c[4]*x[4] + c[5]*x[5] + c[6]*x[6], "Функция цели"
    problem += (c[0] * x[0] + c[1] * x[1] + c[2] * x[2] + c[3] * x[3] + c[4] * x[4] + c[5] * x[5] + c[6] * x[6]) >= b
    problem += c[0]*x[0] * part[1] == c[1]*x[1]
    problem += c[0] * x[0] * part[2] == c[2] * x[2]
    problem += c[0] * x[0] * part[3] == c[3] * x[3]
    problem += c[0] * x[0] * part[4] == c[4] * x[4]
    problem += c[0] * x[0] * part[5] == c[5] * x[5]
    problem.solve()
    for variable in problem.variables():
        print(variable.name, "=", variable.varValue)
    print("Прибыль:")
    print(pulp.value(problem.objective))

linProg(c)

