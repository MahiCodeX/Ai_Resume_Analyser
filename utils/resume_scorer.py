def calculate_score(skills, missing_sections, text):

    score = 0

    # Skill score
    skill_score = min(len(skills) * 5, 40)
    score += skill_score

    # Section score
    total_sections = 5
    present_sections = total_sections - len(missing_sections)

    section_score = (present_sections / total_sections) * 30
    score += section_score

    # Resume length score
    words = len(text.split())

    if words > 300:
        score += 20
    elif words > 150:
        score += 10
    else:
        score += 5

    # Keyword richness
    unique_words = len(set(text.split()))

    if unique_words > 200:
        score += 10
    else:
        score += 5

    return int(score)