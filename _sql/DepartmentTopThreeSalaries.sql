-- Department Top Three Salaries (https://leetcode.com/problems/department-top-three-salaries/description/)

WITH EmplDeps AS (
    SELECT dprt.name AS Department,
           empl.name as Employee,
           empl.salary AS Salary,
           DENSE_RANK() OVER(
            PARTITION BY departmentId ORDER BY salary DESC
            ) AS rank
    FROM Employee as empl
    INNER JOIN Department as dprt
    ON empl.departmentId = dprt.id
    ORDER BY Department, Salary DESC
),
SortedSalaries AS (
    SELECT Department, Employee, Salary
    FROM EmplDeps
    WHERE rank <= 3
)

SELECT *
FROM SortedSalaries
