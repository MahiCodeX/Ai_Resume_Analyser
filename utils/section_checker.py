def check_sections(text):

    text = text.lower()

    sections = {
        "education": "Education section missing",
        "experience": "Experience section missing",
        "projects": "Projects section missing",
        "skills": "Skills section missing",
        "certification": "Certifications missing"
    }

    missing_sections = []

    for section in sections:
        if section not in text:
            missing_sections.append(sections[section])

    return missing_sections