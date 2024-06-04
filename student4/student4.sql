WITH LatestReservation AS (
    SELECT
        room_id,
        MAX(end_date) AS last_checkout
    FROM
        reservations
    GROUP BY
        room_id
),
LatestReviews AS (
    SELECT
        r.room_id,
        rv.rating
    FROM
        reviews rv
    JOIN
        reservations r ON rv.reservation_id = r.id
    JOIN
        (SELECT
            room_id,
            MAX(end_date) AS last_checkout
        FROM
            reservations
        GROUP BY
            room_id) lr ON r.room_id = lr.room_id AND r.end_date = lr.last_checkout
)
SELECT
    r.address AS room_address,
    u.name AS owner_name,
    lr.last_checkout AS latest_checkout_date,
    lrv.rating AS latest_review_rating,
    (SELECT COUNT(*) FROM reservations WHERE room_id = r.id) AS total_reservations,
    (SELECT AVG(price) FROM reservations WHERE room_id = r.id) AS average_price
FROM
    rooms r
JOIN
    users u ON r.owner_id = u.id
JOIN
    LatestReservation lr ON r.id = lr.room_id
LEFT JOIN
    LatestReviews lrv ON r.id = lrv.room_id
ORDER BY
    r.address;

