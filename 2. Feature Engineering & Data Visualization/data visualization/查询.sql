SELECT `属性`, `弱点`, COUNT(*) as `数量`
FROM  pokemon.data
GROUP BY `属性`, `弱点`;

SELECT `属性`, AVG(`身高`) as `平均身高`, AVG(`体重`) as `平均体重`
FROM pokemon.data
GROUP BY `属性`;

SELECT `姓名`, `体重`
FROM pokemon.data
WHERE `体重` > 10;

SELECT `姓名`, `属性`, `弱点`, `身高`, `体重`, `特征`
FROM pokemon.data
WHERE `弱点` LIKE '%火%';

SELECT `姓名`, `身高`
FROM pokemon.data
WHERE `身高` = (SELECT MAX(`身高`) FROM pokemon.data)
OR `身高` = (SELECT MIN(`身高`) FROM characters);


SELECT 
    `姓名`,
    `身高`,
    `体重`,
    `体重` / `身高` AS `身高体重比率`,
    CASE
        WHEN `体重` / `身高` < 18.5 THEN '低于正常体重'
        WHEN `体重` / `身高` BETWEEN 18.5 AND 25 THEN '正常体重'
				 WHEN `体重` / `身高` BETWEEN 25 AND 30 THEN '超重'
				 WHEN `体重` / `身高` BETWEEN 30 AND 35 THEN '一类肥胖'
				 WHEN `体重` / `身高` BETWEEN 35 AND 40 THEN '二类肥胖'
        WHEN `体重` / `身高` > 20 THEN '三类肥胖'
        ELSE '其他'
    END AS `比率区间`
FROM 
     pokemon.data;
