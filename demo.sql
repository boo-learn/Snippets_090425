SELECT
    "snippet"."id",
    ...
FROM "snippet"
INNER JOIN "auth_user" ON (
    "snippet"."user_id" = "auth_user"."id"
    )

SELECT * FROM "snippet";

SELECT * FROM "comment"
WHERE "comment"."snippet_id" IN (1, 2, 3, ...); -- Здесь будут ID всех сниппетов из первого запроса