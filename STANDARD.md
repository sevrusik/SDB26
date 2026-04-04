# SDB-26 Standard Document

**The 2026 Synthetic Document Benchmark**  
**Version:** 1.0  
**Date:** April 2026  
**Author:** Ruslan Mishyn  
**Status:** Public Draft

---

## 1. Scope

This standard defines a methodology for evaluating the effectiveness of document verification systems against AI-generated and synthetically manipulated documentary evidence.

SDB-26 applies to:
- Identity document verification systems (KYC)
- Document authenticity verification in financial services
- Any system that accepts documentary evidence as input

SDB-26 does not evaluate:
- Biometric liveness detection
- Sanctions or PEP screening
- Transaction monitoring

---

## 2. Definitions

**Synthetic document:** Any document image produced by a generative AI model, including but not limited to diffusion models, GANs, and large multimodal models, whether or not subsequently post-processed.

**Screenshot attack:** The process of capturing a synthetic document via a screen capture device (mobile phone, tablet, desktop screenshot tool) to strip provenance metadata and C2PA signatures, producing a new file without AI generation markers.

**Bypass Rate (BR):** The percentage of synthetic documents in a given test set that receive an "approved," "genuine," or equivalent positive verdict from the system under test.

**Confidence Gap (CG):** The mean confidence score assigned by the system under test to synthetic documents that it incorrectly approves.

**Generator Sensitivity (GS):** The Bypass Rate calculated separately for each AI generation tool represented in the test corpus.

**System under test (SUT):** The document verification system, API, or model being evaluated against SDB-26.

**Ground truth:** The known classification of each document in the test corpus — synthetic or genuine — established at corpus creation.

---

## 3. Test Corpus Specification

### 3.1 Corpus Structure

The SDB-26 test corpus is organised into three levels of synthetic complexity.

#### Level 1 — Standard Generation

Documents produced by general-purpose image generation models without post-processing optimisation.

| Parameter | Specification |
|-----------|--------------|
| Generators | DALL-E 3, Midjourney v6, Stable Diffusion XL (standard config) |
| Document types | Passport (minimum 3 countries), National ID (minimum 2 countries) |
| Minimum samples | 30 per generator per document type |
| Post-processing | None permitted |
| Resolution | Minimum 512×512 pixels |
| Format | JPEG or PNG |

#### Level 2 — Advanced Diffusion

Documents produced by fine-tuned or specialised generation pipelines with metadata injection.

| Parameter | Specification |
|-----------|--------------|
| Generators | Fine-tuned diffusion models, specialised ID generation tools |
| Document types | Passport, National ID, Bank statement, Invoice |
| Minimum samples | 30 per generator per document type |
| Post-processing | Metadata injection permitted (camera model, timestamp, device info) |
| Resolution | Minimum 512×512 pixels |
| Format | JPEG with injected EXIF |

#### Level 3 — Screenshot Attack

Documents produced by any generation method, then captured via screenshot.

| Parameter | Specification |
|-----------|--------------|
| Source documents | Any Level 1 or Level 2 document |
| Capture method | Screen capture via mobile device (minimum 2 different devices) |
| Device types | iOS and Android represented |
| Minimum samples | 50 total |
| Post-processing | No additional processing after screenshot permitted |
| Format | JPEG (as produced by device camera roll) |

### 3.2 Genuine Document Control Set

Each SDB-26 evaluation must include a genuine document control set to measure False Positive Rate.

| Parameter | Specification |
|-----------|--------------|
| Document types | Same types as synthetic corpus |
| Minimum samples | Equal to synthetic corpus size |
| Source | Camera-captured originals with full EXIF |
| Verification | Ground truth verified by human review |

### 3.3 Corpus Integrity

- All documents in the corpus are assigned a unique identifier
- SHA-256 hash of each document is recorded at corpus creation
- Ground truth labels are stored separately from the corpus files
- Corpus version is recorded with each evaluation

---

## 4. Measurement Methodology

### 4.1 Bypass Rate (BR)

**Formula:**

```
BR = FN / (FN + TP) × 100
```

Where:
- FN = False Negatives (synthetic documents approved as genuine)
- TP = True Positives (synthetic documents correctly flagged)

**Reporting requirements:**
- BR must be reported per level (L1, L2, L3)
- BR must be reported per document type
- BR must be reported per generator (Generator Sensitivity)
- Overall BR across all levels must be reported

### 4.2 Confidence Gap (CG)

**Formula:**

```
CG = mean(confidence_score[i]) for all i where:
  verdict[i] = "genuine" AND ground_truth[i] = "synthetic"
```

**Reporting requirements:**
- CG must be reported as mean ± standard deviation
- CG must be reported per level
- If no false negatives exist at a level, CG is reported as N/A

### 4.3 Generator Sensitivity (GS)

**Formula:**

```
GS[generator] = BR calculated using only documents from that generator
```

**Reporting requirements:**
- GS must be reported for each generator represented in the corpus
- Results must be presented as a ranked table (highest to lowest BR)

### 4.4 False Positive Rate (FPR)

**Formula:**

```
FPR = FP / (FP + TN) × 100
```

Where:
- FP = False Positives (genuine documents flagged as synthetic)
- TN = True Negatives (genuine documents correctly approved)

**Reporting requirements:**
- FPR must be reported alongside BR
- A system optimised only for BR at the expense of FPR is not compliant with SDB-26 reporting standards

---

## 5. Evaluation Procedure

### 5.1 System Configuration

The system under test must be evaluated in its standard production configuration. Custom configurations or parameter adjustments specifically for the SDB-26 evaluation are not permitted unless disclosed.

### 5.2 Document Submission

Documents must be submitted to the system under test in the same format as they would be submitted in production use. No pre-processing of test documents is permitted unless the SUT applies the same pre-processing to all production documents.

### 5.3 Verdict Collection

The evaluation must collect:
- Binary verdict (genuine / synthetic / suspicious / insufficient quality)
- Confidence score (0.0 to 1.0 or 0 to 100)
- Processing time per document

### 5.4 Corpus Blinding

The system under test must not be trained or fine-tuned on SDB-26 corpus documents prior to evaluation. Evaluations conducted after training on corpus documents must be disclosed as such.

---

## 6. Reporting Format

Results must be reported using the standard JSON schema defined in [SCHEMA/results_schema.json](SCHEMA/results_schema.json).

Required fields:
- benchmark version
- system under test (name and version)
- evaluation date
- corpus version used
- results per level
- generator sensitivity table
- false positive rate
- evaluator (self-evaluated or third-party)

Optional fields:
- processing time statistics
- hardware configuration
- API mode (free / paid / enterprise)

---

## 7. Publication Standards

Organisations publishing SDB-26 results must:

1. Use the standard JSON schema
2. Disclose whether evaluation was self-conducted or third-party
3. Disclose the corpus version used
4. Not selectively report levels (all levels tested must be reported)
5. Include FPR alongside BR

Organisations may not:
- Claim "SDB-26 certified" without publishing full results
- Publish partial results without disclosing that other levels were not tested
- Modify the corpus and publish results as SDB-26 compliant

---

## 8. Versioning Policy

| Version | Change type | Description |
|---------|-------------|-------------|
| 1.x | Minor | Addition of new generators or document types to corpus |
| 2.0 | Major | Changes to metric definitions or measurement methodology |

Previous version results remain valid and comparable within the same major version.

Results from different major versions are not directly comparable and must be reported separately.

---

## 9. Governance

SDB-26 v1.0 is maintained by Ruslan Mishyn.

Contributions, corrections, and proposals for future versions are welcomed via GitHub pull request or email to sevrusik@gmail.com.

The benchmark governance model will be reviewed when the first external organisation publishes SDB-26 results. Independent governance is the long-term goal.

---

## 10. Legal

SDB-26 methodology is published under Creative Commons Attribution 4.0 International (CC BY 4.0).

The test corpus is not included in this license. Corpus access is provided to verified organisations under separate terms.

Use of the name "SDB-26" to describe non-compliant evaluations or modified methodologies is not permitted.

---

## Appendix A: Generator Classification Matrix

### Tier 1 — Общедоступные инструменты (Level 1 корпус)

*Доступны любому пользователю без специальных знаний*

| Инструмент | Тип | Сложность подделки | Детектируемость |
|-----------|-----|-------------------|-----------------|
| Midjourney v6 | Диффузионная модель | Средняя | FFT fingerprint |
| DALL-E 3 | Диффузионная модель | Средняя | Spectral artifacts |
| Stable Diffusion XL | Open source | Средняя | GAN/diffusion markers |
| Adobe Firefly | Коммерческая | Средняя | C2PA present |
| Canva AI | Коммерческая | Низкая | Visible artifacts |
| ChatGPT 4o (image) | Мультимодальная | Средняя | Pipeline markers |

**Характеристики Tier 1:**
- Видимые артефакты при форензическом анализе
- Отсутствует или базовый EXIF
- Стандартные спектральные сигнатуры
- Детектируется стандартными forensic инструментами

---

### Tier 2 — Специализированные инструменты (Level 2 корпус)

*Требуют технических знаний или специального доступа*

| Инструмент | Тип | Сложность подделки | Детектируемость |
|-----------|-----|-------------------|-----------------|
| Stable Diffusion + LoRA (ID trained) | Fine-tuned | Высокая | Residual artifacts |
| ComfyUI + custom workflow | Open source pipeline | Высокая | Pipeline mismatch |
| Flux.1 | Продвинутая диффузия | Высокая | Frequency anomalies |
| Специализированные ID генераторы | Закрытые инструменты | Очень высокая | PRNU analysis |
| FaceSwap + template | Гибридный метод | Высокая | Face-document mismatch |
| Inpainting (частичная замена) | Редактирование | Очень высокая | ELA analysis |

**Характеристики Tier 2:**
- Минимальные визуальные артефакты
- Инъецированные метаданные от реального устройства
- Убедительная структура файла
- Требует продвинутого forensic анализа

---

### Tier 3 — Продвинутые техники (Level 3 корпус)

*Структурно обходят стандартные защиты*

| Техника | Механизм обхода | Что обходит | Детектируемость |
|---------|----------------|-------------|-----------------|
| Screenshot Attack (iOS) | Новый файл без C2PA | C2PA, EXIF, AI markers | Moiré patterns, double compression |
| Screenshot Attack (Android) | Новый файл без C2PA | C2PA, EXIF, AI markers | Screen grid artifacts |
| Print & Rescan | Физический аналоговый разрыв | Все цифровые маркеры | Scanner noise patterns |
| Screen recording frame | Видео кадр | Метаданные | Compression artifacts |
| Virtual camera injection | Подмена потока | Liveness detection | Pipeline inconsistency |

**Характеристики Tier 3:**
- Никаких AI маркеров в метаданных
- Правдоподобный device fingerprint
- Полный обход C2PA
- Детектируется только физическим forensic анализом

---

### Матрица сложности подделки

```
Сложность      Tier  Инструмент              Время      Стоимость
──────────────────────────────────────────────────────────────────
Низкая         1     Canva AI                2 мин      Бесплатно
Низкая         1     ChatGPT 4o              2 мин      ~$0.10
Средняя        1     Midjourney v6           5 мин      ~$0.50
Средняя        1     DALL-E 3               5 мин      ~$0.08
Высокая        2     SD + LoRA               30 мин     Бесплатно
Высокая        2     Flux.1                  15 мин     ~$0.20
Очень высокая  2     ID специализированный   1 час      $5-50
Структурная    3     Screenshot Attack       1 мин      Бесплатно
Структурная    3     Print & Rescan          10 мин     ~$0.10
```

**Ключевой инсайт:** Самые опасные подделки — самые дешёвые. Screenshot Attack стоит $0, занимает 1 минуту, обходит C2PA полностью, и детектируется только физическим forensic анализом.

---

## Appendix B: Detection Methods Matrix

### Что каким методом детектируется

| Метод детекции | Tier 1 | Tier 2 | Tier 3 | Описание |
|---------------|--------|--------|--------|----------|
| **Template matching** | ⚠️ Частично | ❌ Нет | ❌ Нет | Проверка соответствия шаблону документа |
| **EXIF validation** | ⚠️ Частично | ⚠️ Частично | ❌ Нет | Проверка метаданных файла |
| **C2PA / provenance** | ✅ Да | ✅ Да | ❌ Нет | Цепочка происхождения файла |
| **Liveness detection** | ⚠️ Частично | ⚠️ Частично | ❌ Нет | Проверка живого присутствия |
| **Vision AI (Claude/GPT)** | ❌ Нет | ❌ Нет | ❌ Нет | Визуальный анализ содержимого |
| **GAN fingerprint** | ✅ Да | ⚠️ Частично | ⚠️ Частично | Отпечаток генеративной сети |
| **FFT spectral analysis** | ✅ Да | ✅ Да | ✅ Да | Анализ частотного домена |
| **PRNU sensor noise** | ✅ Да | ✅ Да | ✅ Да | Шумовая сигнатура сенсора |
| **ELA (Error Level Analysis)** | ✅ Да | ✅ Да | ⚠️ Частично | Анализ уровня ошибок сжатия |
| **Pipeline mismatch** | ✅ Да | ✅ Да | ⚠️ Частично | Несоответствие processing pipeline |
| **Moiré pattern detection** | ❌ Нет | ❌ Нет | ✅ Да | Интерференция экран-сенсор |
| **Double compression** | ❌ Нет | ❌ Нет | ✅ Да | Артефакты двойного сжатия |
| **Scanner stripe detection** | N/A | N/A | ✅ Да | FFT полосы от каретки сканера |

**Легенда:**
- ✅ Да — надёжно детектирует
- ⚠️ Частично — детектирует в части случаев
- ❌ Нет — не детектирует

---

### Критический вывод

```
Единственные методы детектирующие ВСЕ три уровня:
✅ FFT spectral analysis
✅ PRNU sensor noise analysis

Методы слепые ко ВСЕМ уровням:
❌ Vision AI (Claude 3 Haiku, GPT-4V)

Методы слепые к Level 3 (Screenshot Attack):
❌ Template matching
❌ EXIF validation  
❌ C2PA / provenance
❌ Liveness detection
❌ GAN fingerprint (частично)
```

**Практический вывод для комплаенс команд:**

Если ваш KYC стек не включает FFT спектральный анализ или PRNU анализ — у вас 0% защиты против Level 3 атак. Независимо от качества других компонентов.

---

### Рекомендуемый минимальный стек для production KYC (2026)

```
Layer 1: Template + EXIF validation    → базовая защита (Tier 1)
Layer 2: C2PA provenance check         → защита от несложных подделок
Layer 3: GAN/diffusion fingerprint     → защита от Tier 1-2
Layer 4: FFT + PRNU forensic physics   → защита от всех уровней включая L3
Layer 5: Human review для flagged      → финальная проверка
```

Отсутствие Layer 4 означает структурную слепоту к Screenshot Attack — наиболее доступной и распространённой технике в 2026 году.
