-- Department Top Three Salaries (https://leetcode.com/problems/department-top-three-salaries/description/)

SELECT dprt.name AS Department, empl.name AS employee, s.salary
FROM Employee AS empl
INNER JOIN Department AS dprt
ON empl.departmentId = dprt.id
INNER JOIN (
    SELECT name as new_name, salary
    FROM
    (
    SELECT name, salary, DENSE_RANK() OVER(PARTITION BY departmentId ORDER BY salary DESC) as rank
    FROM Employee
    )
    WHERE rank <= 3
) AS slr
ON empl.name = slr.new_name AND empl.salary = slr.salary
