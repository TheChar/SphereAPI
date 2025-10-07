SELECT U.UserID,
    U.Username,
    U.HashedPassword,
    U.Name,
    U.ExpireMinutes
FROM Users U
LEFT JOIN UserApplication UA ON UA.UserID = U.UserID
LEFT JOIN Roles R ON R.RoleID = UA.RoleID
LEFT JOIN Applications A ON UA.ApplicationID = A.ApplicationID
WHERE A.Title = %(AppTitle)s AND R.Title = %(RoleTitle)s;