import os
from PIL import Image, ImageDraw, ImageFont

def generate_png():
    width = 1600
    height = 1040
    img = Image.new("RGBA", (width, height), (11, 17, 32, 255))
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("arial.ttf", 26)
        font_subtitle = ImageFont.truetype("arial.ttf", 13)
        font_header = ImageFont.truetype("arialbd.ttf", 14)
        font_body_bold = ImageFont.truetype("arialbd.ttf", 11)
        font_body = ImageFont.truetype("arial.ttf", 11)
        font_small = ImageFont.truetype("arial.ttf", 10)
    except:
        font_title = font_subtitle = font_header = font_body_bold = font_body = font_small = ImageFont.load_default()

    # Draw Title & Subtitle
    draw.text((800, 30), "PET AMBER · SERVER ENTITY-RELATIONSHIP DIAGRAM (ERD)", fill=(248, 250, 252), font=font_title, anchor="mt")
    draw.text((800, 64), "PostgreSQL 3NF Relational Architecture • Spring Data JPA / Kotlin • Crow's Foot Notation", fill=(148, 163, 184), font=font_subtitle, anchor="mt")
    draw.text((800, 86), "Authors: Roman Tissera (RomanHT) & Kristen Ekedal (KEKEdal) • Numbered Key Notation (FK1, FK2, UQ1..)", fill=(217, 119, 6), font=font_body_bold, anchor="mt")

    # Connectors
    # User -> PetReport
    draw.line([(370, 230), (720, 230)], fill=(56, 189, 248), width=3)
    draw.text((545, 212), "owns (1 : 0..*)", fill=(125, 211, 252), font=font_body_bold, anchor="mm")

    # User -> Squad (routed clear of notation key box)
    draw.line([(370, 330), (580, 330), (580, 540), (720, 540)], fill=(129, 140, 248), width=2)
    draw.text((475, 320), "joins (1 : 0..*)", fill=(165, 180, 252), font=font_body_bold, anchor="mm")

    # PetReport -> Sighting
    draw.line([(1020, 280), (1180, 280), (1180, 730), (1020, 730)], fill=(45, 212, 191), width=2)
    draw.text((1180, 505), "tracks (1 : 0..*)", fill=(94, 234, 212), font=font_body_bold, anchor="mm")

    # Sighting -> Corroboration
    draw.line([(720, 780), (370, 780)], fill=(192, 132, 252), width=2)
    draw.text((545, 765), "verifies (1 : 0..*)", fill=(216, 180, 254), font=font_body_bold, anchor="mm")

    # User -> Corroboration (routed on left flank)
    draw.line([(70, 360), (35, 360), (35, 750), (70, 750)], fill=(129, 140, 248), width=2)
    draw.text((22, 550), "confirms (1 : 0..*)", fill=(199, 210, 254), font=font_small, anchor="mm")

    # Helper function to draw an entity card
    def draw_card(x, y, w, h, header_bg, title, fields):
        draw.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=(15, 23, 42), outline=(51, 65, 85), width=2)
        draw.rounded_rectangle([x, y, x + w, y + 40], radius=8, fill=header_bg)
        draw.rectangle([x, y + 25, x + w, y + 40], fill=header_bg)
        draw.text((x + w // 2, y + 20), title, fill=(255, 255, 255), font=font_header, anchor="mm")

        cur_y = y + 55
        for tag, name, col_type in fields:
            if tag == "PK":
                draw.text((x + 10, cur_y), tag, fill=(56, 189, 248), font=font_body_bold)
            elif tag.startswith("UQ"):
                draw.text((x + 10, cur_y), tag, fill=(245, 158, 11), font=font_body_bold)
            elif tag.startswith("FK"):
                draw.text((x + 10, cur_y), tag, fill=(236, 72, 153), font=font_body_bold)
            elif tag == "ATT":
                draw.text((x + 10, cur_y), "*", fill=(56, 189, 248), font=font_body_bold)
            else:
                draw.text((x + 10, cur_y), "", fill=(148, 163, 184), font=font_body)

            draw.text((x + 42, cur_y), name, fill=(241, 245, 249), font=font_body_bold if tag else font_body)
            draw.text((x + w - 12, cur_y), col_type, fill=(148, 163, 184), font=font_body, anchor="ra")
            cur_y += 22

    # 1. USER_PROFILE (Numbered keys: PK un-numbered, UQ1, UQ2, UQ3)
    user_fields = [
        ("PK", "user_profile_id", "BIGINT IDENTITY"),
        ("UQ1", "external_key", "UUID NOT NULL"),
        ("UQ2", "oauth_key", "VARCHAR(255) NN"),
        ("UQ3", "email", "VARCHAR(255) NN"),
        ("", "display_name", "VARCHAR(100) NN"),
        ("", "avatar_url", "VARCHAR(1024)"),
        ("", "phone_number", "VARCHAR(30)"),
        ("", "created", "TIMESTAMPTZ NN")
    ]
    draw_card(70, 130, 300, 260, (30, 58, 138), "USER_PROFILE (user_profile)", user_fields)

    # 2. PET_REPORT (Numbered keys: PK un-numbered, UQ1, FK1)
    pet_fields = [
        ("PK", "pet_report_id", "BIGINT IDENTITY"),
        ("UQ1", "external_key", "UUID NOT NULL"),
        ("FK1", "owner_id", "BIGINT (CASCADE)"),
        ("", "pet_name", "VARCHAR(100) NN"),
        ("", "species / breed", "VARCHAR(50)/(100)"),
        ("", "color_markings", "VARCHAR(255) NN"),
        ("", "is_microchipped", "BOOLEAN NN"),
        ("ATT", "photo_url (Cloud)", "VARCHAR(1024)"),
        ("", "last_seen_timestamp", "TIMESTAMPTZ NN"),
        ("", "last_seen_coords", "DOUBLE PRECISION"),
        ("", "last_seen_address", "VARCHAR(255)"),
        ("", "status (Enum)", "ACTIVE|REUNITED"),
        ("", "created / updated", "TIMESTAMPTZ NN")
    ]
    draw_card(720, 115, 300, 355, (180, 83, 9), "PET_REPORT (pet_report)", pet_fields)

    # 3. SQUAD_MEMBERSHIP (Numbered keys: PK un-numbered, FK1, FK2, separated lines)
    squad_fields = [
        ("PK", "squad_membership_id", "BIGINT IDENTITY"),
        ("FK1", "user_id", "BIGINT UQ1 (CASCADE)"),
        ("FK2", "pet_report_id", "BIGINT UQ1 (CASCADE)"),
        ("", "joined / is_active", "TIMESTAMPTZ, BOOL")
    ]
    draw_card(720, 495, 300, 145, (67, 56, 202), "SQUAD_MEMBERSHIP (squad)", squad_fields)

    # 4. SIGHTING (Numbered keys: PK un-numbered, UQ1, FK1, FK2, separated lines)
    sighting_fields = [
        ("PK", "sighting_id", "BIGINT IDENTITY"),
        ("UQ1", "external_key", "UUID NOT NULL"),
        ("FK1", "pet_report_id", "BIGINT (CASCADE)"),
        ("FK2", "spotter_id", "BIGINT (RESTRICT)"),
        ("ATT", "photo_url (Evidence)", "VARCHAR(1024)"),
        ("", "sighting_timestamp", "TIMESTAMPTZ NN"),
        ("", "latitude, longitude", "DOUBLE PRECISION"),
        ("", "direction (Enum)", "COMPASS 8-WAY"),
        ("", "direction_notes", "VARCHAR(255)"),
        ("", "notes / created", "TEXT, TIMESTAMPTZ")
    ]
    draw_card(720, 660, 300, 280, (15, 118, 110), "SIGHTING (sighting)", sighting_fields)

    # 5. CORROBORATION (Numbered keys: PK un-numbered, FK1, FK2, separated lines)
    corrob_fields = [
        ("PK", "corroboration_id", "BIGINT IDENTITY"),
        ("FK1", "sighting_id", "BIGINT UQ1 (CASCADE)"),
        ("FK2", "user_id", "BIGINT UQ1 (CASCADE)"),
        ("", "is_confirmed", "BOOLEAN NN"),
        ("", "corroboration_notes", "VARCHAR(500)"),
        ("", "created", "TIMESTAMPTZ NN")
    ]
    draw_card(70, 680, 300, 200, (109, 40, 217), "CORROBORATION (corroboration)", corrob_fields)

    # ==================== LEGEND / NOTATION KEY ====================
    # Fully numbered keys: PK strictly un-numbered, FK1, FK2, UQ1, UQ2, UQ3
    draw.rounded_rectangle([70, 415, 560, 650], radius=8, fill=(30, 41, 59), outline=(71, 85, 105), width=1)
    draw.text((90, 428), "RELATIONAL ARCHITECTURE & NOTATION KEY", fill=(248, 250, 252), font=font_body_bold)
    draw.line([(90, 444), (540, 444)], fill=(71, 85, 105), width=1)

    draw.text((90, 454), "PK", fill=(56, 189, 248), font=font_body_bold)
    draw.text((125, 454), "Primary Key (Surrogate BIGINT IDENTITY - strictly un-numbered)", fill=(203, 213, 225), font=font_body)

    draw.text((90, 472), "FK1", fill=(236, 72, 153), font=font_body_bold)
    draw.text((125, 472), "Foreign Key 1 (Primary parent link: owner_id, pet_report_id, sighting_id)", fill=(203, 213, 225), font=font_body)

    draw.text((90, 490), "FK2", fill=(236, 72, 153), font=font_body_bold)
    draw.text((125, 490), "Foreign Key 2 (Secondary parent link: spotter_id, pet_report_id, user_id)", fill=(203, 213, 225), font=font_body)

    draw.text((90, 508), "UQ1", fill=(245, 158, 11), font=font_body_bold)
    draw.text((125, 508), "Unique Key 1 (UUID external_key / Composite unique pair)", fill=(203, 213, 225), font=font_body)

    draw.text((90, 526), "UQ2", fill=(245, 158, 11), font=font_body_bold)
    draw.text((125, 526), "Unique Key 2 (OAuth Google subject identifier: oauth_key)", fill=(203, 213, 225), font=font_body)

    draw.text((90, 544), "UQ3", fill=(245, 158, 11), font=font_body_bold)
    draw.text((125, 544), "Unique Key 3 (Unique user email address: email)", fill=(203, 213, 225), font=font_body)

    draw.line([(90, 560), (540, 560)], fill=(51, 65, 85), width=1)

    draw.text((90, 568), "Crow's Foot: ||--o{ = One to Zero-or-More (Strictly normalized 3NF)", fill=(148, 163, 184), font=font_small)
    draw.text((90, 584), "Option A: Direct Cloud Photo URLs on PetReport & Sighting", fill=(148, 163, 184), font=font_small)
    draw.text((90, 600), "Kotlin JPA: Mapped via @Entity, @Table, @Enumerated(STRING)", fill=(148, 163, 184), font=font_small)
    draw.text((90, 616), "Target Database: PostgreSQL 16+ (H2 in Postgres compatibility mode)", fill=(56, 189, 248), font=font_small)

    out_path = r"C:\Users\Tisse\deep-dive\java-kotlin\projects\pet-amber\docs\img\erd.png"
    img.save(out_path, "PNG")
    print(f"Generated {out_path}")

if __name__ == "__main__":
    generate_png()
