SELECT
    U.UserID AS UID,
    U.Username,
    U.HashedPassword,
    U.ExpireMins,
    jsonb_agg(UA.Data) AS AppData
FROM Users U
LEFT JOIN UserApplication UA ON U.UserID = UA.UserID
WHERE U.Username=%(username)s