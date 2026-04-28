-- =========================
-- UPSERT CONTACT (UPDATED)
-- =========================
CREATE OR REPLACE PROCEDURE upsert_contact(
    p_name VARCHAR,
    p_email VARCHAR,
    p_birthday DATE,
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INT;
    v_group_id INT;
BEGIN
    -- Get or create group
    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;

    IF v_group_id IS NULL THEN
        INSERT INTO groups(name) VALUES (p_group_name) RETURNING id INTO v_group_id;
    END IF;

    -- Check if contact exists
    SELECT id INTO v_contact_id FROM contacts WHERE name = p_name;

    IF v_contact_id IS NOT NULL THEN
        UPDATE contacts
        SET email = p_email,
            birthday = p_birthday,
            group_id = v_group_id
        WHERE id = v_contact_id;
    ELSE
        INSERT INTO contacts(name, email, birthday, group_id)
        VALUES (p_name, p_email, p_birthday, v_group_id)
        RETURNING id INTO v_contact_id;
    END IF;
END;
$$;


-- =========================
-- ADD PHONE (NEW)
-- =========================
CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INT;
BEGIN
    SELECT id INTO v_contact_id FROM contacts WHERE name = p_contact_name;

    IF v_contact_id IS NULL THEN
        RAISE NOTICE 'Contact not found';
        RETURN;
    END IF;

    INSERT INTO phones(contact_id, phone, type)
    VALUES (v_contact_id, p_phone, p_type);
END;
$$;


-- =========================
-- MOVE TO GROUP (NEW)
-- =========================
CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_group_id INT;
BEGIN
    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;

    IF v_group_id IS NULL THEN
        INSERT INTO groups(name) VALUES (p_group_name) RETURNING id INTO v_group_id;
    END IF;

    UPDATE contacts
    SET group_id = v_group_id
    WHERE name = p_contact_name;
END;
$$;


-- =========================
-- DELETE CONTACT
-- =========================
CREATE OR REPLACE PROCEDURE delete_contact_proc(
    p_value TEXT,
    p_type TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_type = 'name' THEN
        DELETE FROM contacts WHERE name = p_value;
    ELSIF p_type = 'phone' THEN
        DELETE FROM contacts
        WHERE id IN (
            SELECT contact_id FROM phones WHERE phone = p_value
        );
    ELSE
        RAISE NOTICE 'Invalid delete type';
    END IF;
END;
$$;