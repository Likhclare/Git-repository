-- =========================
-- SEARCH CONTACTS (UPDATED)
-- =========================
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(
    id INT,
    name VARCHAR,
    email VARCHAR,
    phone VARCHAR,
    group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.id,
        c.name,
        c.email,
        p.phone,
        g.name
    FROM contacts c
    LEFT JOIN phones p ON c.id = p.contact_id
    LEFT JOIN groups g ON c.group_id = g.id
    WHERE 
        c.name ILIKE '%' || p_query || '%'
        OR c.email ILIKE '%' || p_query || '%'
        OR p.phone ILIKE '%' || p_query || '%';
END;
$$;


-- =========================
-- PAGINATION (UPDATED)
-- =========================
CREATE OR REPLACE FUNCTION get_contacts_paginated(
    p_limit INT,
    p_offset INT
)
RETURNS TABLE(
    id INT,
    name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.id,
        c.name,
        c.email,
        c.birthday,
        g.name
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    ORDER BY c.name
    LIMIT p_limit
    OFFSET p_offset;
END;
$$;