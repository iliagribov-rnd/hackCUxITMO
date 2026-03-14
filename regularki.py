import re
import pandas as pd

# =========================================================
# Приоритет классов для разрешения пересечений
# =========================================================
CLASS_PRIORITY = {
    "Email": 1,
    "СНИЛС клиента": 2,
    "Номер банковского счета": 3,
    "Сведения об ИНН": 4,
    "Водительское удостоверение": 5,
    "Разрешение на работу / визу": 6,
    "CVV/CVC": 7,
    "ПИН код": 8,
    "Одноразовые коды": 9,
}

def digits_only(s: str) -> str:
    """Оставляет только цифры."""
    return re.sub(r"\D", "", s)

def normalize_spaces(s: str) -> str:
    """Заменяет множественные пробелы одним и убирает краевые."""
    return re.sub(r"\s+", " ", s.strip())

# =========================================================
# Валидаторы (проверяют длину цифрового содержимого)
# =========================================================
def validate_email(s: str) -> bool:
    s = s.strip()
    if "@" not in s:
        return False
    parts = s.split("@")
    if len(parts) != 2:
        return False
    if "." not in parts[1]:
        return False
    return True

def validate_snils(s: str) -> bool:
    return len(digits_only(s)) == 11

def validate_bank_account(s: str) -> bool:
    return len(digits_only(s)) == 20

def validate_inn(s: str) -> bool:
    return len(digits_only(s)) in (10, 12)

def validate_driver_license(s: str) -> bool:
    return len(digits_only(s)) == 10

def validate_work_permit_or_visa(s: str) -> bool:
    return len(digits_only(s)) == 9

def validate_cvv(s: str) -> bool:
    return bool(re.fullmatch(r"\d{3,4}", s.strip()))

def validate_pin(s: str) -> bool:
    return bool(re.fullmatch(r"\d{4}", s.strip()))

def validate_otp(s: str) -> bool:
    return bool(re.fullmatch(r"\d{4,8}", s.strip()))

VALIDATORS = {
    "Email": validate_email,
    "СНИЛС клиента": validate_snils,
    "Номер банковского счета": validate_bank_account,
    "Сведения об ИНН": validate_inn,
    "Водительское удостоверение": validate_driver_license,
    "Разрешение на работу / визу": validate_work_permit_or_visa,
    "CVV/CVC": validate_cvv,
    "ПИН код": validate_pin,
    "Одноразовые коды": validate_otp,
}

# =========================================================
# Регулярные выражения (искомая сущность всегда в группе 1)
# =========================================================
PATTERNS = {
    "Email": [
        re.compile(
            r"(?<![\w.+-])([A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,})(?![\w.-])",
            flags=re.I
        ),
    ],
    "СНИЛС клиента": [
        re.compile(r"(?<!\d)(\d{3}-\d{3}-\d{3}\s\d{2})(?!\d)"),
        re.compile(r"(?<!\d)(\d{3}-\d{3}-\d{3}-\d{2})(?!\d)"),
        re.compile(r"(?i)(?:снилс)\D{0,20}((?:\d[\s\-]?){11})"),
    ],
    "Номер банковского счета": [
        re.compile(
            r"(?i)(?:расч[её]тн(?:ый|ого)?\s+сч[её]т|банковск(?:ий|ого)?\s+сч[её]т|номер\s+сч[её]та|р/с)\D{0,25}((?:\d[\s\-]?){20})"
        ),
        re.compile(r"(?<!\d)(\d{20})(?!\d)"),
    ],
    "Сведения об ИНН": [
        re.compile(r"(?i)(?:инн)\D{0,20}((?:\d[\s\-]?){10,12})"),
        re.compile(r"(?i)(?:идентификационн\w*\s+номер\s+налогоплательщика)\D{0,20}((?:\d[\s\-]?){10,12})"),
    ],
    "Водительское удостоверение": [
        re.compile(
            r"(?i)(?:водительск\w*\s+удостоверени\w*|номер\s+прав|права)\D{0,25}((?:\d{2}[\s\-]?\d{2}[\s\-]?\d{6})|\d{10})"
        ),
    ],
    "Разрешение на работу / визу": [
        re.compile(r"(?i)(?:разрешени\w*\s+на\s+работу)\D{0,25}((?:\d{2}[\s\-]?\d{7})|\d{9})"),
        re.compile(r"(?i)(?:виз\w*|visa)\D{0,25}((?:\d{2}[\s\-]?\d{7})|\d{9})"),
    ],
    "CVV/CVC": [
        re.compile(r"(?i)(?:cvv|cvc|код\s+безопасности|security\s*code)\D{0,15}(\d{3,4})(?!\d)"),
    ],
    "ПИН код": [
        re.compile(r"(?i)(?:пин[\s\-]?код|pin[\s\-]?code|pin)\D{0,15}(\d{4})(?!\d)"),
    ],
    "Одноразовые коды": [
        re.compile(r"(?i)(?:одноразов\w*\s+код|код\s+подтверждени\w*|sms[\s\-]?код|смс[\s\-]?код|verification\s*code|otp)\D{0,20}(\d{4,8})(?!\d)"),
    ],
}

# =========================================================
# Вспомогательные функции обработки кандидатов
# =========================================================
def is_overlap(a_start, a_end, b_start, b_end):
    return max(a_start, b_start) < min(a_end, b_end)

def clean_entity_for_validation(entity: str) -> str:
    return normalize_spaces(entity)

def extract_candidates(text: str):
    """Собирает все непересекающиеся кандидаты, прошедшие валидацию."""
    candidates = []
    for label, pattern_list in PATTERNS.items():
        for pattern in pattern_list:
            for match in pattern.finditer(text):
                if match.lastindex is None:
                    continue
                start, end = match.start(1), match.end(1)
                entity = text[start:end]
                entity_clean = clean_entity_for_validation(entity)
                validator = VALIDATORS.get(label, lambda x: True)
                if not validator(entity_clean):
                    continue
                candidates.append({
                    "start": start,
                    "end": end,
                    "label": label,
                    "priority": CLASS_PRIORITY[label],
                    "length": end - start,
                })
    return candidates

def resolve_overlaps(candidates):
    """
    Убирает пересекающиеся сущности, оставляя:
    - самую левую
    - при равном старте – самую длинную
    - при равной длине – с наивысшим приоритетом
    """
    if not candidates:
        return []
    candidates = sorted(candidates, key=lambda x: (x["start"], -x["length"], x["priority"]))
    result = []
    for cand in candidates:
        keep = True
        for prev in result:
            if is_overlap(cand["start"], cand["end"], prev["start"], prev["end"]):
                keep = False
                break
        if keep:
            result.append(cand)
    result = sorted(result, key=lambda x: (x["start"], x["end"], x["label"]))
    return [(x["start"], x["end"], x["label"]) for x in result]

def extract_regex_entities(text: str):
    """Главная функция извлечения для одного текста."""
    if not isinstance(text, str) or not text:
        return []
    candidates = extract_candidates(text)
    return resolve_overlaps(candidates)

# =========================================================
# Основная функция для DataFrame
# =========================================================
def build_regex_predictions(df: pd.DataFrame, text_col: str = "text") -> pd.DataFrame:
    """
    Принимает DataFrame с колонкой text_col.
    Возвращает DataFrame с колонками:
        id          — порядковый номер строки
        Prediction  — список кортежей (start, end, label)
    """
    if text_col not in df.columns:
        raise ValueError(f"В DataFrame нет колонки '{text_col}'")

    work_df = df.reset_index(drop=True).copy()
    predictions = []
    for i, text in enumerate(work_df[text_col].tolist()):
        spans = extract_regex_entities(text)
        predictions.append({
            "id": i,
            "Prediction": spans
        })
    return pd.DataFrame(predictions)


# if __name__ == "__main__":
#     # Пример DataFrame
#     data = {
#         "text": [
#             "Мой email: example@mail.ru и снилс 123-456-789 01",
#             "Пин код 1234, cvv 567, номер счета 40817810099910012345",
#         ]
#     }
#     df = pd.DataFrame(data)
#     result_df = build_regex_predictions(df, text_col="text")
#     print(result_df)
#     # result_df.to_csv("regex_predictions.csv", index=False)