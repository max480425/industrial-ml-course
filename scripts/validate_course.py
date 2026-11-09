#!/usr/bin/env python3
"""
scripts/validate_course.py
Industrial Machine Learning & Predictive Maintenance Course

Comprehensive validation script verifying course data integrity:
1. Every lesson in syllabus.json has a corresponding JSON file in src/data/lessons/.
2. Every lesson JSON contains non-empty title_en, title_pl, sections, visual_widget,
   colab_notebook, and quiz.
3. Every {{term:id}} used in any lesson exists in src/data/glossary.json.
4. Every .ipynb file referenced by a lesson exists in public/notebooks/ and parses
   cleanly with nbformat.read().
"""

import sys
import json
import re
from pathlib import Path
import nbformat

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SYLLABUS_FILE = PROJECT_ROOT / "src" / "data" / "syllabus.json"
GLOSSARY_FILE = PROJECT_ROOT / "src" / "data" / "glossary.json"
LESSONS_DIR = PROJECT_ROOT / "src" / "data" / "lessons"
NOTEBOOKS_DIR = PROJECT_ROOT / "public" / "notebooks"

VALID_SANDBOX_TYPES = {
    "signal_filter_sandbox",
    "scaling_outlier_sandbox",
    "cost_matrix_sandbox",
    "clustering_sandbox",
    "fft_anomaly_sandbox",
    "cnn_iou_sandbox",
    "drift_latency_sandbox",
}

class CourseValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.syllabus = []
        self.glossary_terms = {}
        self.lesson_files = {}

    def log_error(self, category, msg):
        self.errors.append(f"[{category}] ERROR: {msg}")

    def log_warning(self, category, msg):
        self.warnings.append(f"[{category}] WARNING: {msg}")

    def load_base_data(self):
        # 1. Load syllabus
        if not SYLLABUS_FILE.exists():
            self.log_error("SYLLABUS", f"File not found: {SYLLABUS_FILE}")
            return False
        try:
            with open(SYLLABUS_FILE, "r", encoding="utf-8") as f:
                self.syllabus = json.load(f)
        except Exception as e:
            self.log_error("SYLLABUS", f"Failed to parse {SYLLABUS_FILE}: {e}")
            return False

        # 2. Load glossary
        if not GLOSSARY_FILE.exists():
            self.log_error("GLOSSARY", f"File not found: {GLOSSARY_FILE}")
            return False
        try:
            with open(GLOSSARY_FILE, "r", encoding="utf-8") as f:
                glossary_list = json.load(f)
                self.glossary_terms = {item["id"]: item for item in glossary_list}
        except Exception as e:
            self.log_error("GLOSSARY", f"Failed to parse {GLOSSARY_FILE}: {e}")
            return False

        # 3. Check lessons directory
        if not LESSONS_DIR.exists() or not LESSONS_DIR.is_dir():
            self.log_error("LESSONS", f"Directory not found: {LESSONS_DIR}")
            return False

        return True

    def validate_syllabus_to_lesson_files(self):
        """Rule 1: Every lesson in syllabus.json has a corresponding JSON file in src/data/lessons/"""
        total_lessons = 0
        matched_lessons = 0

        for mod in self.syllabus:
            mod_id = mod.get("id", "?")
            for les in mod.get("lessons", []):
                total_lessons += 1
                les_id = les.get("id")
                if not les_id:
                    self.log_error("SYLLABUS", f"Lesson in module {mod_id} is missing an 'id'")
                    continue

                lesson_file = LESSONS_DIR / f"{les_id}.json"
                if not lesson_file.exists():
                    self.log_error(
                        "LESSON_FILE_MISSING",
                        f"Lesson '{les_id}' defined in syllabus.json has no file: {lesson_file}"
                    )
                else:
                    try:
                        with open(lesson_file, "r", encoding="utf-8") as f:
                            self.lesson_files[les_id] = json.load(f)
                            matched_lessons += 1
                    except Exception as e:
                        self.log_error(
                            "LESSON_FILE_CORRUPT",
                            f"Failed to read/parse JSON in {lesson_file}: {e}"
                        )

        print(f"  ✓ Syllabus check: {matched_lessons}/{total_lessons} lessons have matching JSON files.")

    def validate_lesson_attributes(self):
        """
        Rule 2: Every lesson JSON contains non-empty:
        title_en, title_pl, sections, visual_widget, colab_notebook, and quiz.
        """
        required_keys = [
            ("title_en", str),
            ("title_pl", str),
            ("sections", list),
            ("visual_widget", str),
            ("colab_notebook", str),
            ("quiz", list),
        ]

        valid_count = 0

        for les_id, data in self.lesson_files.items():
            has_error = False
            for key, expected_type in required_keys:
                val = data.get(key)
                if val is None:
                    self.log_error(
                        "ATTRIBUTE_MISSING",
                        f"Lesson '{les_id}' is missing required key '{key}'"
                    )
                    has_error = True
                elif not isinstance(val, expected_type):
                    self.log_error(
                        "ATTRIBUTE_TYPE",
                        f"Lesson '{les_id}' key '{key}' must be {expected_type.__name__}, got {type(val).__name__}"
                    )
                    has_error = True
                elif isinstance(val, (str, list)) and len(val) == 0:
                    self.log_error(
                        "ATTRIBUTE_EMPTY",
                        f"Lesson '{les_id}' has empty '{key}'"
                    )
                    has_error = True

            # Check visual_widget against valid sandboxes
            vw = data.get("visual_widget")
            if vw and vw not in VALID_SANDBOX_TYPES:
                self.log_warning(
                    "SANDBOX_TYPE",
                    f"Lesson '{les_id}' specifies visual_widget '{vw}', expected one of {VALID_SANDBOX_TYPES}"
                )

            # Check colab_notebook extension
            nb_name = data.get("colab_notebook")
            if nb_name and not nb_name.endswith(".ipynb"):
                self.log_error(
                    "NOTEBOOK_NAME",
                    f"Lesson '{les_id}' colab_notebook '{nb_name}' must end with .ipynb"
                )
                has_error = True

            if not has_error:
                valid_count += 1

        print(f"  ✓ Attribute check: {valid_count}/{len(self.lesson_files)} lesson JSONs passed all schema requirements.")

    def validate_term_references(self):
        """Rule 3: Every {{term:id}} used in any lesson exists in src/data/glossary.json."""
        pattern = re.compile(r"\{\{term:([a-zA-Z0-9_-]+)(?:\|[^}]+)?\}\}")
        checked_terms = set()
        missing_terms = {}

        def scan_text(text, les_id, field_name):
            if not isinstance(text, str):
                return
            matches = pattern.findall(text)
            for term_id in matches:
                checked_terms.add(term_id)
                if term_id not in self.glossary_terms:
                    if term_id not in missing_terms:
                        missing_terms[term_id] = []
                    missing_terms[term_id].append(f"{les_id}:{field_name}")

        def recursive_scan(obj, les_id, prefix=""):
            if isinstance(obj, str):
                scan_text(obj, les_id, prefix)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    recursive_scan(item, les_id, f"{prefix}[{i}]")
            elif isinstance(obj, dict):
                for k, v in obj.items():
                    recursive_scan(v, les_id, f"{prefix}.{k}" if prefix else k)

        for les_id, data in self.lesson_files.items():
            recursive_scan(data.get("sections", []), les_id, "sections")
            scan_text(data.get("title_en", ""), les_id, "title_en")
            scan_text(data.get("title_pl", ""), les_id, "title_pl")
            scan_text(data.get("summary_en", ""), les_id, "summary_en")
            scan_text(data.get("summary_pl", ""), les_id, "summary_pl")

        if missing_terms:
            for term_id, occurrences in missing_terms.items():
                self.log_error(
                    "GLOSSARY_TERM_MISSING",
                    f"Term '{{{{term:{term_id}}}}}' used in {occurrences} is not defined in glossary.json"
                )
        else:
            print(f"  ✓ Glossary check: All {len(checked_terms)} unique {{{{term:id}}}} tags exist in glossary.json ({len(self.glossary_terms)} defined).")

    def validate_notebook_files(self):
        """
        Rule 4: Every .ipynb file referenced by a lesson exists in public/notebooks/
        and parses cleanly with nbformat.read().
        """
        checked_notebooks = set()
        valid_notebooks = 0

        for les_id, data in self.lesson_files.items():
            nb_name = data.get("colab_notebook")
            if not nb_name:
                continue
            if nb_name in checked_notebooks:
                continue

            checked_notebooks.add(nb_name)
            nb_path = NOTEBOOKS_DIR / nb_name

            if not nb_path.exists():
                self.log_error(
                    "NOTEBOOK_FILE_MISSING",
                    f"Notebook '{nb_name}' referenced by lesson '{les_id}' does not exist in {NOTEBOOKS_DIR}"
                )
                continue

            try:
                with open(nb_path, "r", encoding="utf-8") as f:
                    nb_obj = nbformat.read(f, as_version=4)

                cells = nb_obj.get("cells", [])
                if len(cells) < 2:
                    self.log_error(
                        "NOTEBOOK_TOO_SHORT",
                        f"Notebook '{nb_name}' has fewer than 2 cells ({len(cells)} found)."
                    )
                    continue

                valid_notebooks += 1
            except Exception as e:
                self.log_error(
                    "NOTEBOOK_PARSE_FAILED",
                    f"Notebook '{nb_name}' failed nbformat.read validation: {e}"
                )

        print(f"  ✓ Notebook check: {valid_notebooks}/{len(checked_notebooks)} notebooks verified and parsed cleanly with nbformat v4.")

    def run(self):
        print("=" * 70)
        print("  Industrial ML Course Integrity Validator")
        print("=" * 70)

        if not self.load_base_data():
            print("\n❌ Critical base data missing. Aborting validation.")
            self.report()
            return False

        self.validate_syllabus_to_lesson_files()
        self.validate_lesson_attributes()
        self.validate_term_references()
        self.validate_notebook_files()

        return self.report()

    def report(self):
        print("-" * 70)
        if self.warnings:
            print(f"⚠️  {len(self.warnings)} warning(s) found:")
            for w in self.warnings:
                print(f"   {w}")

        if self.errors:
            print(f"\n❌ VALIDATION FAILED with {len(self.errors)} error(s):")
            for e in self.errors:
                print(f"   {e}")
            return False
        else:
            print("\n🎉 ALL CHECKS PASSED: Course curriculum and notebooks are 100% valid!")
            return True

def main():
    validator = CourseValidator()
    success = validator.run()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
