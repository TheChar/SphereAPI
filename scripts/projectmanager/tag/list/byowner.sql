SELECT *
FROM Tags
WHERE Owner = %(OwnerID)s AND IsPublic = TRUE;