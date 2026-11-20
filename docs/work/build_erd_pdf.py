import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#475569"))

        # Running Header on page 2
        if self._pageNumber > 1:
            self.drawString(36, 764, "PET AMBER · SERVER ENTITY-RELATIONSHIP SPECIFICATION")
            self.drawRightString(612 - 36, 764, "ROMAN TISSERA & KRISTEN EKEDAL")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.6)
            self.line(36, 758, 612 - 36, 758)

        # Running Footer on all pages
        self.setFont("Helvetica", 7.5)
        self.drawString(36, 18, "Spring Data JPA · PostgreSQL 3NF Multi-User Schema · Crow's Foot Notation (Option A · Numbered Keys)")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(612 - 36, 18, page_str)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(36, 26, 612 - 36, 26)
        self.restoreState()

def build_pdf(filename=r"C:\Users\Tisse\deep-dive\java-kotlin\projects\pet-amber\docs\pdf\Pet_Amber_Server_ERD_Specification.pdf"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    printable_width = 612 - 72  # 540 pt
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=28,
        bottomMargin=28
    )

    styles = getSampleStyleSheet()

    primary_color = colors.HexColor("#0F172A")
    amber_brand = colors.HexColor("#D97706")
    dark_blue = colors.HexColor("#1E3A8A")
    card_bg = colors.HexColor("#F8FAFC")
    border_color = colors.HexColor("#CBD5E1")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=colors.white
    )

    meta_right = ParagraphStyle(
        'MetaRight',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.5,
        textColor=colors.white,
        alignment=2
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=dark_blue,
        spaceBefore=4,
        spaceAfter=2,
        keepWithNext=True
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=5.6,
        leading=7.2,
        textColor=colors.HexColor("#38BDF8")
    )

    tbl_head = ParagraphStyle('TblHead', fontName='Helvetica-Bold', fontSize=7.2, leading=9, textColor=colors.white)
    tbl_cell = ParagraphStyle('TblCell', fontName='Helvetica', fontSize=6.8, leading=8.5, textColor=primary_color)
    tbl_cell_bold = ParagraphStyle('TblCellB', fontName='Helvetica-Bold', fontSize=6.8, leading=8.5, textColor=primary_color)

    dict_title = ParagraphStyle('DictTitle', fontName='Helvetica-Bold', fontSize=7.5, leading=9.5, textColor=dark_blue)
    dict_item = ParagraphStyle('DictItem', fontName='Helvetica', fontSize=6.4, leading=7.8, textColor=primary_color, leftIndent=6)

    story = []

    # ==================== PAGE 1 ====================
    banner_left = Paragraph("<b>PET AMBER</b><br/><font size=8.5><b>Server Entity-Relationship Diagram (ERD) Specification · Kotlin Spring Data JPA</b></font><br/>PostgreSQL 3NF Multi-User Relational Architecture · Option A · Numbered Keys (FK1, FK2, UQ1..)", title_style)
    banner_right = Paragraph("<b>Students:</b> Roman Tissera &amp; Kristen Ekedal<br/><b>Language:</b> 100% Idiomatic Kotlin<br/><b>Keys:</b> PK un-numbered, FK# &amp; UQ# numbered", meta_right)
    banner_tbl = Table([[banner_left, banner_right]], colWidths=[360, 180])
    banner_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), amber_brand),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(banner_tbl)
    story.append(Spacer(1, 3))

    section1_hdr = Table([
        [Paragraph("<b>1. Visual Entity-Relationship Diagram (ERD)</b>", h1_style),
         Paragraph("<font color='#0D9488'><b>✓ CROW'S FOOT 3NF · NUMBERED KEYS</b></font>", ParagraphStyle('HdrR', fontName='Helvetica-Bold', fontSize=8, alignment=2))]
    ], colWidths=[380, 160])
    section1_hdr.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(section1_hdr)
    story.append(Spacer(1, 2))

    # Embed ERD PNG
    png_path = r"C:\Users\Tisse\deep-dive\java-kotlin\projects\pet-amber\docs\img\erd.png"
    if os.path.exists(png_path):
        img = Image(png_path, width=540, height=270)
        story.append(img)
    story.append(Spacer(1, 4))

    # Relational Schema Matrix Table (Option A: 7 relationships)
    story.append(Paragraph("<b>2. Relational Schema Matrix &amp; Multi-User Ownership</b>", h1_style))
    matrix_data = [
        [
            Paragraph("<b>Primary Entity</b>", tbl_head),
            Paragraph("<b>Crow's Foot</b>", tbl_head),
            Paragraph("<b>Foreign Entity</b>", tbl_head),
            Paragraph("<b>Multiplicity</b>", tbl_head),
            Paragraph("<b>Integrity Rules, Multi-User Isolation &amp; Cascade Behaviors</b>", tbl_head)
        ],
        [
            Paragraph("USER_PROFILE", tbl_cell_bold),
            Paragraph("||--o{", tbl_cell_bold),
            Paragraph("PET_REPORT", tbl_cell_bold),
            Paragraph("1 to 0..*", tbl_cell),
            Paragraph("User owns zero or more pet alerts (FK1 owner_id). Deleting user profile purges their reports (ON DELETE CASCADE).", tbl_cell)
        ],
        [
            Paragraph("USER_PROFILE", tbl_cell_bold),
            Paragraph("||--o{", tbl_cell_bold),
            Paragraph("SQUAD_MEMBERSHIP", tbl_cell_bold),
            Paragraph("1 to 0..*", tbl_cell),
            Paragraph("User can join multiple search squads (FK1 user_id). Unique constraint UQ1(user_id, pet_report_id) prevents duplicates.", tbl_cell)
        ],
        [
            Paragraph("PET_REPORT", tbl_cell_bold),
            Paragraph("||--o{", tbl_cell_bold),
            Paragraph("SQUAD_MEMBERSHIP", tbl_cell_bold),
            Paragraph("1 to 0..*", tbl_cell),
            Paragraph("A report mobilizes a search squad (FK2 pet_report_id). Purging report cascades to squad memberships (CASCADE).", tbl_cell)
        ],
        [
            Paragraph("PET_REPORT", tbl_cell_bold),
            Paragraph("||--o{", tbl_cell_bold),
            Paragraph("SIGHTING", tbl_cell_bold),
            Paragraph("1 to 0..*", tbl_cell),
            Paragraph("A report maintains a chronological sighting trail (FK1 pet_report_id). Purging report cascades to sightings (CASCADE).", tbl_cell)
        ],
        [
            Paragraph("USER_PROFILE", tbl_cell_bold),
            Paragraph("||--o{", tbl_cell_bold),
            Paragraph("SIGHTING", tbl_cell_bold),
            Paragraph("1 to 0..*", tbl_cell),
            Paragraph("Any authenticated user can spot an animal (FK2 spotter_id). Spotter FK uses ON DELETE RESTRICT for non-repudiation.", tbl_cell)
        ],
        [
            Paragraph("SIGHTING", tbl_cell_bold),
            Paragraph("||--o{", tbl_cell_bold),
            Paragraph("CORROBORATION", tbl_cell_bold),
            Paragraph("1 to 0..*", tbl_cell),
            Paragraph("A sighting receives community upvotes (FK1 sighting_id). Unique constraint UQ1(sighting_id, user_id) stops vote spam.", tbl_cell)
        ],
        [
            Paragraph("USER_PROFILE", tbl_cell_bold),
            Paragraph("||--o{", tbl_cell_bold),
            Paragraph("CORROBORATION", tbl_cell_bold),
            Paragraph("1 to 0..*", tbl_cell),
            Paragraph("A user can corroborate sightings logged by neighbors (FK2 user_id). Purging user cascades corroborations (CASCADE).", tbl_cell)
        ]
    ]
    matrix_tbl = Table(matrix_data, colWidths=[80, 48, 92, 55, 265])
    matrix_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), dark_blue),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, card_bg])
    ]))
    story.append(matrix_tbl)

    # ==================== PAGE 2 ====================
    story.append(PageBreak())

    # Mermaid Code Block (Option A & Numbered Keys)
    story.append(Paragraph("<b>3. Mermaid ERD Source Code</b> &nbsp;&nbsp;<font size=7 color='#64748B'>(3NF Relational Grammar · Option A · Numbered Keys: PK un-numbered, FK#, UQ#)</font>", h1_style))
    
    code_col1 = """erDiagram
  USER_PROFILE ||--o{ PET_REPORT : "owns (1 : 0..*)"
  USER_PROFILE ||--o{ SQUAD_MEMBERSHIP : "joins (1 : 0..*)"
  PET_REPORT ||--o{ SQUAD_MEMBERSHIP : "mobilizes (1 : 0..*)"
  PET_REPORT ||--o{ SIGHTING : "tracks (1 : 0..*)"
  USER_PROFILE ||--o{ SIGHTING : "spots (1 : 0..*)"
  SIGHTING ||--o{ CORROBORATION : "verifies (1 : 0..*)"
  USER_PROFILE ||--o{ CORROBORATION : "confirms (1 : 0..*)"

  USER_PROFILE {
    BIGINT user_profile_id PK "IDENTITY"
    UUID external_key UQ1 "NOT NULL, UNIQUE"
    VARCHAR oauth_key UQ2 "Google sub NOT NULL, UNIQUE"
    VARCHAR display_name "NOT NULL"
    VARCHAR email UQ3 "NOT NULL, UNIQUE"
    VARCHAR avatar_url "NULL"
    VARCHAR phone_number "NULL"
    TIMESTAMPTZ created "NOT NULL DEFAULT CURRENT_TIMESTAMP"
  }
  PET_REPORT {
    BIGINT pet_report_id PK "IDENTITY"
    UUID external_key UQ1 "NOT NULL, UNIQUE"
    BIGINT owner_id FK1 "REFERENCES user_profile (CASCADE)"
    VARCHAR pet_name "NOT NULL"
    VARCHAR species "NOT NULL"
    VARCHAR breed "NULL"
    VARCHAR color_markings "NOT NULL"
    VARCHAR collar_description "NULL"
    BOOLEAN is_microchipped "NOT NULL DEFAULT FALSE"
    VARCHAR photo_url "NULL (Cloud Storage)"
    TIMESTAMPTZ last_seen_timestamp "NOT NULL"
    DOUBLE_PRECISION last_seen_latitude "NOT NULL"
    DOUBLE_PRECISION last_seen_longitude "NOT NULL"
    VARCHAR status "ACTIVE_SEARCH | REUNITED | CLOSED"
    TIMESTAMPTZ created "NOT NULL"
    TIMESTAMPTZ updated "NOT NULL"
  }"""

    code_col2 = """  SQUAD_MEMBERSHIP {
    BIGINT squad_membership_id PK "IDENTITY"
    BIGINT user_id FK1 "REFERENCES user_profile (CASCADE, UQ1)"
    BIGINT pet_report_id FK2 "REFERENCES pet_report (CASCADE, UQ1)"
    TIMESTAMPTZ joined "NOT NULL DEFAULT CURRENT_TIMESTAMP"
    BOOLEAN is_active "NOT NULL DEFAULT TRUE"
  }
  SIGHTING {
    BIGINT sighting_id PK "IDENTITY"
    UUID external_key UQ1 "NOT NULL, UNIQUE"
    BIGINT pet_report_id FK1 "REFERENCES pet_report (CASCADE)"
    BIGINT spotter_id FK2 "REFERENCES user_profile (RESTRICT)"
    VARCHAR photo_url "NULL (Evidence Image)"
    TIMESTAMPTZ sighting_timestamp "NOT NULL"
    DOUBLE_PRECISION latitude "NOT NULL"
    DOUBLE_PRECISION longitude "NOT NULL"
    VARCHAR direction "Enum: NORTH..STATIONARY"
    VARCHAR direction_notes "Free-form text"
    TEXT notes "NULL"
    TIMESTAMPTZ created "NOT NULL"
  }
  CORROBORATION {
    BIGINT corroboration_id PK "IDENTITY"
    BIGINT sighting_id FK1 "REFERENCES sighting (CASCADE, UQ1)"
    BIGINT user_id FK2 "REFERENCES user_profile (CASCADE, UQ1)"
    BOOLEAN is_confirmed "NOT NULL DEFAULT TRUE"
    VARCHAR corroboration_notes "NULL"
    TIMESTAMPTZ created "NOT NULL"
  }"""

    col1_p = [Paragraph(line.replace(" ", "&nbsp;"), code_style) for line in code_col1.split("\n")]
    col2_p = [Paragraph(line.replace(" ", "&nbsp;"), code_style) for line in code_col2.split("\n")]
    two_col_code = Table([[col1_p, col2_p]], colWidths=[270, 270])
    two_col_code.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0F172A")),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#334155")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(two_col_code)
    story.append(Spacer(1, 4))

    # Entity & Attribute Data Dictionary (3 columns, 5 entities)
    story.append(Paragraph("<b>4. Entity &amp; Attribute Data Dictionary</b> &nbsp;&nbsp;<font size=7 color='#64748B'>(Numbered: PK un-numbered, FK1/FK2, UQ1/UQ2/UQ3)</font>", h1_style))
    
    col1 = [
        Paragraph("<b>USER_PROFILE (user_profile)</b>", dict_title),
        Paragraph("• <b>PK user_profile_id:</b> BIGINT IDENTITY", dict_item),
        Paragraph("• <b>UQ1 external_key:</b> UUID NOT NULL UNIQUE", dict_item),
        Paragraph("• <b>UQ2 oauth_key:</b> VARCHAR(255) NN (Google sub)", dict_item),
        Paragraph("• <b>UQ3 email:</b> VARCHAR(255) NN UNIQUE", dict_item),
        Paragraph("• <b>display_name:</b> VARCHAR(100) NOT NULL", dict_item),
        Paragraph("• <b>avatar_url:</b> VARCHAR(1024) NULL", dict_item),
        Paragraph("• <b>phone_number:</b> VARCHAR(30) NULL", dict_item),
        Paragraph("• <b>created:</b> TIMESTAMPTZ DEFAULT NOW()", dict_item),
        Spacer(1, 4),
        Paragraph("<b>SQUAD_MEMBERSHIP (squad_membership)</b>", dict_title),
        Paragraph("• <b>PK squad_membership_id:</b> BIGINT IDENTITY", dict_item),
        Paragraph("• <b>FK1 user_id:</b> BIGINT NN (REFERENCES user_profile)", dict_item),
        Paragraph("• <b>FK2 pet_report_id:</b> BIGINT NN (REFERENCES pet_report)", dict_item),
        Paragraph("• <b>UQ1 uq_user_report:</b> UNIQUE(user_id, pet_report_id)", dict_item),
        Paragraph("• <b>joined:</b> TIMESTAMPTZ DEFAULT NOW()", dict_item),
        Paragraph("• <b>is_active:</b> BOOLEAN DEFAULT TRUE", dict_item),
    ]

    col2 = [
        Paragraph("<b>PET_REPORT (pet_report)</b>", dict_title),
        Paragraph("• <b>PK pet_report_id:</b> BIGINT IDENTITY", dict_item),
        Paragraph("• <b>UQ1 external_key:</b> UUID NOT NULL UNIQUE", dict_item),
        Paragraph("• <b>FK1 owner_id:</b> BIGINT NN (user_profile, CASCADE)", dict_item),
        Paragraph("• <b>pet_name:</b> VARCHAR(100) NOT NULL", dict_item),
        Paragraph("• <b>species / breed:</b> VARCHAR(50) NN / VARCHAR(100)", dict_item),
        Paragraph("• <b>color_markings:</b> VARCHAR(255) NOT NULL", dict_item),
        Paragraph("• <b>collar_description:</b> VARCHAR(255) NULL", dict_item),
        Paragraph("• <b>is_microchipped:</b> BOOLEAN DEFAULT FALSE", dict_item),
        Paragraph("• <b>photo_url:</b> VARCHAR(1024) NULL (Cloud Image)", dict_item),
        Paragraph("• <b>last_seen_timestamp:</b> TIMESTAMPTZ NOT NULL", dict_item),
        Paragraph("• <b>last_seen_coords:</b> DOUBLE PRECISION (lat/lng)", dict_item),
        Paragraph("• <b>last_seen_address:</b> VARCHAR(255) NULL", dict_item),
        Paragraph("• <b>status:</b> ACTIVE_SEARCH | REUNITED | CLOSED", dict_item),
        Paragraph("• <b>created / updated:</b> TIMESTAMPTZ NOT NULL", dict_item),
    ]

    col3 = [
        Paragraph("<b>SIGHTING (sighting)</b>", dict_title),
        Paragraph("• <b>PK sighting_id:</b> BIGINT IDENTITY", dict_item),
        Paragraph("• <b>UQ1 external_key:</b> UUID NOT NULL UNIQUE", dict_item),
        Paragraph("• <b>FK1 pet_report_id:</b> BIGINT NN (report, CASCADE)", dict_item),
        Paragraph("• <b>FK2 spotter_id:</b> BIGINT NN (user, RESTRICT)", dict_item),
        Paragraph("• <b>photo_url:</b> VARCHAR(1024) NULL (Evidence Photo)", dict_item),
        Paragraph("• <b>sighting_timestamp:</b> TIMESTAMPTZ NOT NULL", dict_item),
        Paragraph("• <b>latitude / longitude:</b> DOUBLE PRECISION", dict_item),
        Paragraph("• <b>location_description:</b> VARCHAR(255) NULL", dict_item),
        Paragraph("• <b>direction:</b> Enum (NORTH..STATIONARY)", dict_item),
        Paragraph("• <b>direction_notes:</b> VARCHAR(255) (free-form)", dict_item),
        Paragraph("• <b>notes / created:</b> TEXT, TIMESTAMPTZ", dict_item),
        Spacer(1, 4),
        Paragraph("<b>CORROBORATION (corroboration)</b>", dict_title),
        Paragraph("• <b>PK corroboration_id:</b> BIGINT IDENTITY", dict_item),
        Paragraph("• <b>FK1 sighting_id:</b> BIGINT NN (sighting, CASCADE)", dict_item),
        Paragraph("• <b>FK2 user_id:</b> BIGINT NN (user_profile, CASCADE)", dict_item),
        Paragraph("• <b>UQ1 uq_sighting_user:</b> UNIQUE(sighting_id, user_id)", dict_item),
        Paragraph("• <b>is_confirmed:</b> BOOLEAN DEFAULT TRUE", dict_item),
        Paragraph("• <b>corroboration_notes:</b> VARCHAR(500) NULL", dict_item),
        Paragraph("• <b>created:</b> TIMESTAMPTZ DEFAULT NOW()", dict_item),
    ]

    dict_table = Table([[col1, col2, col3]], colWidths=[180, 180, 180])
    dict_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
    ]))
    story.append(dict_table)
    story.append(Spacer(1, 3))

    iso_text = Paragraph(
        "<b>Multi-User Data Isolation &amp; Integrity Architecture:</b> Every pet alert, sighting, and squad action is bound to a verified Google OAuth 2.0 user profile (`user_profile_id`). Under Option A, pet profile photos and sighting evidence images are referenced as direct cloud storage URLs (`photo_url`), eliminating unnecessary join tables while maintaining clean REST payloads. Foreign keys and unique constraints are numbered individually (`FK1`, `FK2`, `UQ1`, `UQ2`, `UQ3`) across all entity definitions, while the primary key remains un-numbered (`PK`). Spotter submissions enforce non-repudiation with `ON DELETE RESTRICT`, while corroborations and squad memberships enforce database uniqueness (`UQ1`), completely eliminating duplicate votes and spam.",
        ParagraphStyle('Iso', fontName='Helvetica', fontSize=6.5, leading=8.5, textColor=colors.HexColor("#1E293B"))
    )
    iso_table = Table([[iso_text]], colWidths=[540])
    iso_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#3B82F6")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(iso_table)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {filename}")

if __name__ == "__main__":
    build_pdf()
