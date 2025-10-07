DO $$
BEGIN
IF EXISTS (SELECT RoleRouteID FROM RoleRoute WHERE RouteID = (SELECT RouteID FROM Routes WHERE Operation = %(Operation)s AND RouteName = %(RouteName)s))
THEN
RAISE EXCEPTION 'Route is being used by a role. Cannot delete route.';
END IF;

DELETE FROM Routes
WHERE Operation = %(Operation)s AND RouteName = %(RouteName)s;
END $$;