# database
База данных для сервиса по бронированию жилья, созданная с помощью SQLAlchemy (Python) и заполненнная с помощью библиотеки Faker  
Логическая модель:  
![3f18f1b9-30e9-4270-b9d2-150aceab7610](https://github.com/user-attachments/assets/36d7022b-7d48-4965-9cf4-1211159044e7)  
Вот некоторые SQL запросы:  
SELECT h.*  
FROM  
  housings h  
JOIN  
  addresses a ON h.address_id = a.address_id  
WHERE  
  a.city = 'New York'  
ORDER BY  
  h.number_of_rooms DESC;  
![image](https://github.com/user-attachments/assets/d9d4bb95-35d7-4b01-9de8-12c302927ca5)  

SELECT h.*  
FROM  
  housings h
JOIN
  reviews r ON h.housing_id = r.housing_id
GROUP BY 
  h.housing_id
HAVING AVG(r.grade) > 4;
![image](https://github.com/user-attachments/assets/5fad8438-3ae9-45b7-bbbe-474606078908)

WITH city_avg_rating AS (
  SELECT
    a.city,
    h.housing_id,
    AVG(r.grade) OVER (PARTITION BY a.city) AS avg_city_rating,
    r.grade
  FROM
    reviews r
  JOIN
    housings h ON r.housing_id = h.housing_id
  JOIN
    addresses a ON h.address_id = a.address_id
)
SELECT
  city,
  housing_id,
  grade,
  avg_city_rating,
  RANK() OVER (PARTITION BY city ORDER BY grade DESC) AS housing_rank_in_city,
  PERCENT_RANK() OVER (PARTITION BY city ORDER BY grade) AS housing_percentile_in_city
FROM
  city_avg_rating
ORDER BY
  avg_city_rating DESC, housing_rank_in_city;
![image](https://github.com/user-attachments/assets/f8d94136-8704-4859-ab69-20c5a17633b1)


