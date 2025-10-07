WITH RID AS (
    SELECT RoleID AS RID,
        Title
    FROM Roles 
    WHERE ApplicationID = (SELECT ApplicationID FROM Applications WHERE Title = %(AppTitle)s)
)

--Check not last role for application
IF COUNT((SELECT RID FROM RID)) <= 1 THEN
    RAISE EXCEPTION 'This is the last role for %. You cannot remove it.', %(AppTitle)s;
END IF;
--Check no user has role
IF EXISTS (SELECT UserApplicationID FROM UserApplication WHERE RoleID = (SELECT RID FROM RID WHERE Title = %(RoleTitle)s)) THEN
    RAISE EXCEPTION 'A user has this role. It cannot be removed';
END IF;
--Delete role route connections
DELETE FROM RoleRoute
WHERE RoleID = (SELECT RID FROM RID WHERE Title = %(RoleTitle)s);
--Delete role
DELETE FROM Roles
WHERE RoleID = (SELECT RID FROM RID WHERE Title = %(RoleTitle)s);
--Delete untethered routes
DELETE FROM Routes
WHERE NOT EXISTS (
    SELECT 1
    FROM RoleRoute
    WHERE Routes.RouteID = RoleRoute.RouteID
);