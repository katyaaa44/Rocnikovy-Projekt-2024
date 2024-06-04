SELECT
    r.address AS room_address,
    rvd.end_date AS checkout_date,
    u.name AS last_guest_name
FROM
    rooms r
JOIN (
    SELECT
    	MAX(end_date) AS last_checkout,
        room_id
    FROM
        reservations
    GROUP BY
        room_id
) AS lr ON r.id = lr.room_id
JOIN reservations rvd ON rvd.room_id = r.id AND rvd.end_date = lr.last_checkout
JOIN users u ON u.id = rvd.user_id;

