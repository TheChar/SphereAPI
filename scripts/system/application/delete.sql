WITH AppID AS (
    SELECT ApplicationID AS AID
    FROM Applications
    WHERE Title = %(Title)s;
)
--First unbind roles and routes
DELETE FROM RoleRoute
WHERE RoleID = (SELECT RoleID FROM Roles WHERE ApplicationID = (SELECT AID FROM AppID));
--Then remove user accounts for the app
DELETE FROM UserApplication
WHERE ApplicationID = (SELECT AID FROM AppID);
--Then remove roles
DELETE FROM Roles
WHERE ApplicationID = (SELECT AID FROM AppID);
--Then remove app
DELETE FROM Applications
WHERE ApplicationID = (SELECT AID FROM AppID);
--Then remove extra routes that aren't tied to an app
DELETE FROM Routes
WHERE NOT EXISTS (
    SELECT 1
    FROM RoleRoute
    WHERE Routes.RouteID = RoleRoute.RouteID
);