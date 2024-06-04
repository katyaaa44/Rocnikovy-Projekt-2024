WITH LastReservations AS (
    SELECT
        room_id,
        user_id,
        end_date,
        ROW_NUMBER() OVER(PARTITION BY room_id ORDER BY end_date DESC) AS rn
    FROM
        reservations
)
SELECT
    r.address AS room_address,
    u.name AS last_guest_name,
    lr.end_date AS checkout_date
FROM
    LastReservations lr
JOIN
    rooms r ON lr.room_id = r.id
JOIN
    users u ON lr.user_id = u.id
WHERE
    lr.rn = 1;

