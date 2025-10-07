SELECT A.ApplicationID,
    A.Title,
    jsonb_agg(R.Title)
FROM Applications A
LEFT JOIN Roles R ON A.ApplicationID = R.ApplicationID
WHERE A.Title = %(Title)s
GROUP BY A.ApplicationID;