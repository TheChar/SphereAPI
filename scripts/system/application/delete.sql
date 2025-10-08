DO $$
DECLARE app_id INT;
BEGIN
SELECT ApplicationID
    INTO app_id
    FROM Applications
    WHERE Title = %(Title)s;
--First unbind roles and routes
DELETE FROM RoleRoute
WHERE RoleID = (SELECT RoleID FROM Roles WHERE ApplicationID = app_id);
--Then remove user accounts for the app
DELETE FROM UserApplication
WHERE ApplicationID = app_id;
--Then remove roles
DELETE FROM Roles
WHERE ApplicationID = app_id;
--Then remove app
DELETE FROM Applications
WHERE ApplicationID = app_id;
--Then remove extra routes that aren't tied to an app
DELETE FROM Routes
WHERE NOT EXISTS (
    SELECT 1
    FROM RoleRoute
    WHERE Routes.RouteID = RoleRoute.RouteID
);
END $$;