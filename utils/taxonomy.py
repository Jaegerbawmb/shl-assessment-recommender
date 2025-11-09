from typing import List

TECH_KEYS = [
    'java','python','sql','javascript','c++','c#','golang','node','react','django','spring','rest','api',
    'docker','kubernetes','aws','azure','gcp','cloud','data','ml','ai','nlp','devops','backend','frontend',
    'developer','engineer','coding','programming','algorithms'
]
BEHAV_KEYS = [
    'communication','collaborat','stakeholder','team','leadership','adaptab','integrity','ownership',
    'drive','work ethic','attention to detail','openness','conscientious','agreeab','emotional','resilience'
]

def detect_mix(query: str) -> str:
    q = query.lower()
    tech = any(k in q for k in TECH_KEYS)
    beh = any(k in q for k in BEHAV_KEYS)
    if tech and beh:
        return 'mixed'
    if tech:
        return 'technical'
    if beh:
        return 'behavioral'
    return 'unknown'
