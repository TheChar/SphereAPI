SELECT
    U.UserID AS UID,
    U.Username,
    U.HashedPassword,
    U.ExpireMinutes,
    jsonb_agg(UA.Data) AS AppData,
    R.Title,
    jsonb_agg(
        jsonb_build_object('Operation', RT.Operation, 'Route', RT.RouteName)
    ) AS Routes
FROM Users U
LEFT JOIN UserApplication UA ON U.UserID = UA.UserID
LEFT JOIN Applications A ON UA.ApplicationID = A.ApplicationID
LEFT JOIN Roles R ON UA.RoleID = R.RoleID
LEFT JOIN RoleRoute RR ON R.RoleID = RR.RoleID
LEFT JOIN Routes RT ON RR.RouteID = RT.RouteID
WHERE U.Username=%(Username)s AND A.Title = %(AppTitle)s
GROUP BY UID, R.Title